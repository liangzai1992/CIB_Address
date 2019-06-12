import json
import codecs
import os
import urllib
import sys
import time
from urllib.request import urlopen, quote
import csv
import math
import xlrd
import traceback
class WrongCityException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message
class Over400Exception(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message
class ChangeAKException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message
tag_list = ['美食', '酒店', '购物', '生活服务', '丽人', '旅游景点', '休闲娱乐', '运动健身', '教育培训', '文化传媒', '医疗', '汽车服务', '交通设施', '金融', '房地产', '公司企业', '政府机构']

def initial_AK_pond():   #初始化ak 池 0 为有额度 1为额度已经用完 保存成数组格式
    global ak_dic
    ak_dic = {}
    ak_dic = {
        "mKOV9991B7N98C46kUeNRUXScM067Xys": 0,
        "hvZ5O0of19Alfl7HShUWyOVlFiD8WYWG": 0,
        "5tlPS97zCcgTjbk6gy6AnLVG4p2jtg7u": 0,
        "GEC7Zek74HysO1AKCx1iG6bOXCzTWE6z": 0,
        "9HnBVwKEC01DMgxmINhOSGMt5q1M8kyr": 0,
        "SB3KV3mGWLQ3ncHEk7QfiRNCYHFMYtav": 0,
        "CDjmH9V1ZFfhv9qX2KzGvCrf8UVdUu99": 0,
        "y0j1hsIBRInpjyXub9dFLwsHjnTx73m4": 0,
        "YrwNoo8bNA2Nzfj7pldFXaXVz7iyEPXZ": 0,
        "jGDQ054Yx7n9MNFewodPgykG9UlvlYNa": 0,
        "c5AA39AFSpEAtDCRWWCRhoG5htUrUWvD": 0,
        "lN8FZ9Y8dXeGVdv7aTKvdcnkpXUuMcpQ": 0,
        "zer4hmUsf2Cppl2Z3ozkRMrGx6phGMVf": 0,
        "KdaCBLpAZrUApkiVqjYFSheusOwf2bhh": 0,
        "gwThbIBPPOlUYBQIMUhIP5haNLLkG3Nx": 0,
    }
    
def exchange_AK():
    for line in ak_dic.items():
        if line[1] == 0:
            return line[0]
    print("ak池的额度全部用完了")
    return None

class LocaDiv(object):
    def __init__(self, loc_all, square_size = 0.05, box = 0):  #square_size 为切分的小矩形框的大小 以经纬度为单位 例如0.03
        self.loc_all = loc_all
        self.square_size = square_size
        self.box = box
        if self.box != 0:   #如果有输入 划分格数 按照就按照划分格数来进行
            self.type = 1
        elif self.square_size:  #其次如果没有填入划分格数时按照 square size来进行
            self.type = 2
        else:
            self.type = 3

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / self.square_size)):  # 0.1为网格大小，可更改
            lat_list.append(lat_sw + self.square_size * i)  # 0.05
        lat_list.append(lat_ne)
        # print("lat_list", lat_list)
        return lat_list

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / self.square_size)):  # 0.1为网格大小，可更改
            lng_list.append(lng_sw + self.square_size * i)  # 0.1为网格大小，可更改
        lng_list.append(lng_ne)
        # print("lng_list", lng_list)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        if self.type == 2:
            l1 = self.lat_all()
            l2 = self.lng_all()
            ls = []
            for i in range(len(l1)-1):
                for j in range(len(l2)-1):
                    a = str(l1[i]) + "," + str(l2[j])
                    b = str(l1[i+1]) + "," + str(l2[j+1])
                    ls.append(a+","+b)
            return ls
        elif self.type == 1:   #如果填入了分成多少格
            lat_sw = float(self.loc_all.split(',')[0])
            lat_ne = float(self.loc_all.split(',')[2])
            lng_sw = float(self.loc_all.split(',')[1])
            lng_ne = float(self.loc_all.split(',')[3])
            lat_long = lat_ne - lat_sw
            lng_long = lng_ne - lng_sw
            slice = math.sqrt(self.box)  #获取切成box块需要对于经度或者纬度的切分块数 例如4块对应 经度切两份
            lat_per = lat_long / slice
            lng_per = lng_long / slice
            ls = []
            for i in range(int(slice)):
                lat_1 = lat_sw + i * lat_per
                lat_2 = lat_sw + (i + 1) * lat_per
                for j in range(int(slice)):
                    lng_1 = lng_sw + j * lng_per
                    lng_2 = lng_sw + (j+1) * lng_per
                    ls.append(str(lat_1) + "," + str(lng_1)+","+str(lat_2)+","+str(lng_2))
            return ls

def read_error(ak):
    data = xlrd.open_workbook("/Users/ake/Downloads/公司/郑州/郑州error.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(nrows):
        bounds = table.row_values(i)[0]
        key = table.row_values(i)[1]
        city = table.row_values(i)[2]
        print(bounds,key,city)
        loc = LocaDiv(bounds, square_size= 0.015,box = 9)  #将城市用最西南 和 最东北的经纬度划分 0.02为划分的矩形大小  4为切分块数  如果切分块数指定的话 矩形大小自动忽略 切分块数请输入 正整数的平方 4 9 25 36...
        locs_to_use = loc.ls_row()  #生成划分完毕后的 bounds
        print("总共有", len(locs_to_use), "个矩形框")
        for loc_to_use in locs_to_use:  # 遍历每个小矩形框
            print(loc_to_use)
            if key != "其他":
                sum = 0
                for i in range(20):  # 最多20条
                    print("第", i, "条", key)
                    try:
                        flag = BaiDuAPI(key, loc_to_use, ak, i, city)  # 调用百度地图API
                        if flag == False:  # 如果flag 为False 意味着这一次掉用哪个API结果为空，跳出第一层循环
                            break
                    except WrongCityException as e:
                        print("捕获到 城市不对异常", e)
                        break_flag = True
                        break
                    except Over400Exception as e:
                        print("捕获到 大于400个消息异常", e)
                        if sum == 0:  # 第一次遇到问题写入
                            writing_str = "超过400个数量错误 在 " + loc_to_use + " " + key + "出了错误"
                            error_list.write(writing_str)
                            error_list.write("\n")
                            error_list.flush()
                            sum += 1
                        continue
                    except ChangeAKException as e:  # 捕捉AK额度不够的异常
                        print("捕获到AK额度不够的异常")
                        ak_dic[ak] = 1  # 将当前AK的状态设置为 已经跑完  P.S 1为已经跑完 0 为还有剩余额度
                        ak = exchange_AK()  # 换一个AK
                        print("已经更换AK", ak)
                        print("-----------------等待3s-------------------")
                        time.sleep(3)
                        if ak == None:  # 如果调用ak 之后为None 证明ak池的额度全部用完 错误文件记录当前运行结束时的状态
                            error_list.write("在这里停止了:" + loc_to_use + "爬取大区域为" + bounds)
                            error_list.write("\n")
                            error_list.flush()
                            return None
                        else:
                            continue
            elif key == "其他":
                for x in tag_list:
                    key = x
                    sum = 0
                    for i in range(20):  # 最多20条
                        print("第", i, "条", key)
                        try:
                            flag = BaiDuAPI(key, loc_to_use, ak, i, city)  # 调用百度地图API
                            if flag == False:  # 如果flag 为False 意味着这一次掉用哪个API结果为空，跳出第一层循环
                                break
                        except WrongCityException as e:
                            print("捕获到 城市不对异常", e)
                            break_flag = True
                            break
                        except Over400Exception as e:
                            print("捕获到 大于400个消息异常", e)
                            if sum == 0:  # 第一次遇到问题写入
                                writing_str = "超过400个数量错误 在 " + loc_to_use + " " + key + "出了错误"
                                error_list.write(writing_str)
                                error_list.write("\n")
                                error_list.flush()
                                sum += 1
                            continue
                        except ChangeAKException as e:  # 捕捉AK额度不够的异常
                            print("捕获到AK额度不够的异常")
                            ak_dic[ak] = 1  # 将当前AK的状态设置为 已经跑完  P.S 1为已经跑完 0 为还有剩余额度
                            ak = exchange_AK()  # 换一个AK
                            print("已经更换AK", ak)
                            print("-----------------等待3s-------------------")
                            time.sleep(3)
                            if ak == None:  # 如果调用ak 之后为None 证明ak池的额度全部用完 错误文件记录当前运行结束时的状态
                                error_list.write("在这里停止了:" + loc_to_use + "爬取大区域为" + bounds)
                                error_list.write("\n")
                                error_list.flush()
                                return None
                            else:
                                continue
                        except Exception as e:
                            error_list.write("其他异常:" + loc_to_use + "爬取大区域为"+ bounds)
                            error_list.write("\n")
                            error_list.write(traceback.format_exc()+"\n")
                            error_list.flush()

def BaiDuAPI(key,bounds,ak,page_num,city):
    flag = True
    url = "http://api.map.baidu.com/place/v2/search"
    output = 'json'
    ak = ak
    keys = quote(key)
    url_send = url + "?query=%s&bounds=%s&output=json&ak=%s&page_size=20&page_num=%s" % (keys, bounds, ak, page_num)
    req = urlopen(url_send)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    temp = json.loads(res)
    print(temp)
    if temp['status'] == 301 or temp['status'] == 302 or temp['status'] == 401 or temp['status'] == 402:
        print("换AK异常")
        raise ChangeAKException("要换AK了")
        return flag
    if temp['results'] == [] or temp['status'] == 1:
        flag = False
    elif  temp['results'][0]['name'] == city:
        pass
    elif temp['results'][0]['city'] != city :   #如果爬取信息不在想要获得的城市之中
        raise WrongCityException("城市不对")
        return flag
    elif temp['total'] == 400 :
        for line in temp['results']:
            name = line.get('name','')
            lat = line['location'].get('lat','')
            lng = line['location'].get('lng','')  
            address = line.get('address','')  
            city = line.get('city','')
            area = line.get('area','')
            try: 
                company_data.write(str(name)+"^"+str(key)+"^"+str(lat)+"^"+str(lng)+"^"+str(address)+"^"+str(city)+"^"+str(area)+"\n")
                company_data.flush()
            except Exception as e:
                pass
        flag = True
        raise Over400Exception("总个数超过400")  #抛出超过400的错误需要调整矩形框大小
    else:
        for line in temp['results']:
            name = line.get('name','') #如果没有name键，就默认为空值
            lat = line['location'].get('lat','')
            lng = line['location'].get('lng','')  
            address = line.get('address','')  
            city = line.get('city','')
            area = line.get('area','')
            try: 
                company_data.write(str(name)+"^"+str(key)+"^"+str(lat)+"^"+str(lng)+"^"+str(address)+"^"+str(city)+"^"+str(area)+"\n")
                company_data.flush()
            except Exception as e:
                pass
        flag = True
    return flag


if __name__ == "__main__":
    # bounds = '30.8, 120.9, 31.53, 122.12'
    # loc = LocaDiv(bounds, square_size= 0.05,box = 4)  #将城市用最西南 和 最东北的经纬度划分 0.02为划分的矩形大小  4为切分块数  如果切分块数指定的话 矩形大小自动忽略 切分块数请输入 正整数的平方 4 9 25 36...
    # locs_to_use = loc.ls_row()  #生成划分完毕后的 bounds
    # print("总共有", len(locs_to_use), "个矩形框")
    initial_AK_pond()
    global company_data
    company_data = open("/Users/ake/Downloads/公司/郑州/郑州_错误_地址.txt",'a+',encoding='utf8')
    global error_list
    error_list = open("/Users/ake/Downloads/公司/错误_地址error.txt",'a+',encoding='utf8')
    ak = exchange_AK()
    read_error(ak)
