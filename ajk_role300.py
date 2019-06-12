import csv
import re
import json
from urllib.request import urlopen, quote

def list_name(keyname, value1, dict1=None):  # 将一条数据压缩成字典格式
    dict1 = dict(zip(keyname, value1))
    return dict1

def reverseLng(lng, lat,ak):   #经纬度反向解析
    add_list = []
    url = "http://api.map.baidu.com/geocoder/v2/"
    output = 'json'
    ak = ak
    url_send = url + "?callback=renderReverse&location=%s,%s&output=json&pois=1&latest_admin=1&ak=%s&radius=300" % (lat, lng, ak)
    req = urlopen(url_send)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    temp = json.loads(res[29:-1])
    city = temp['result']['addressComponent']['city']
    district = temp['result']['addressComponent']['district']
    formatted_address = temp['result']['formatted_address']
    pois = temp['result']['pois']
    street = temp['result']['addressComponent']['street']  #获取小区所在街道 用于建立标准路库
    for line in pois:
        model = []
        model.append(line['addr'])
        model.append(line['distance'])
        model.append(line['name'])
        lng = str(line['point']['x'])
        lat = str(line['point']['y'])
        model.append(lat)
        model.append(lng)
        add_list.append(model)
    return add_list, city, district, formatted_address,street

def run(road,city,ak):
    file = open(road)
    road_split = road.split("\\")
    road2 = ""
    for i in road_split[:-1]:
        road2 += i + "\\"
    road_data = road2 + "%s_安居客路库.txt" % (city)
    road_data2 = road2 + "%s_安居客路库_error.txt" % (city)
    error_file = open(road_data2, 'a+')
    fileObject = open(road_data, 'w+')
    start_string = '{"result":['
    fileObject.write(start_string)
    key1 = ['name', 'origin_address','lat','lng','finished_time', 'price']
    sum = 0  #计数器
    lengeth = len(file.readlines())   #获取总共有多少行 由于本行语句会致使for循环无法运行  所以要重复打开一次
    file = open(road)
    for line in file:
        try:
            line = line.split('&')
            a1 = {}
            arr = list_name(key1, line, a1)   #将基础数据存入json串
            arr['price'] = line[5].replace("\n", "")
            arr['count'] = sum
            name = line[0]
            lat = line[2]
            lng = line[3]
            # 获取当前经纬度下，半径300m范围之内的所有路信息add_list， 和所处地区district 例如：浦东新区 和 百度API中的地址信息 address
        except Exception as e:
            print(name,"这一行出问题啦! 去文件当中看看?")
            break
        try:
            add_list, city, district, formatted_address,street = reverseLng(lng, lat,ak)
        except Exception as e:
            print("百度地图API没解析出来 ", name, "已写入错误文件", road_data2)
            error_file.write(name)
            error_file.write("\n")
            error_file.flush()
            continue
        arr['formatted_address'] = formatted_address
        arr['city'] = city
        arr['district'] = district
        arr['street'] = street
        key2 = ['add','distance','name','lat', 'lng']
        add_save_list = []
        for add in add_list:
            a2 = {}
            arr2 = list_name(key2, add, a2)
            arr2['count'] = sum
            add_save_list.append(arr2)
        arr['add_list'] = add_save_list   #将该小区300m范围内路库信息加入json串中
        arr = json.dumps(arr, ensure_ascii=False)
        fileObject.write(arr)
        print(name,"处理成功")
        if sum < lengeth - 1:  #如果不是最后一行数据，两条json之间要加 ","  如果是最后一行 不要加 ","
            fileObject.write(",")
            fileObject.write('\n')
            sum += 1
        else:
            sum += 1
    fileObject.flush()
    fileObject.write(']}')
    fileObject.close()


if __name__ == "__main__":
    road = "/Users/ake/Downloads/python/安居客小区数据/兰州/兰州.txt"  #前期已经爬取下来的小区信息
    city = '兰州' #用于生成路库文件
    ak = 'yHHqlqI0pLycBZVlMRjCFtQ8HSyMVWgv'  #百度地图API的ak，建议一个人自己注册一个
    run(road, city, ak)
