import json
import re
import codecs
import os
import urllib
import sys
import time
from urllib.request import urlopen, quote
import xlrd
import csv
import traceback
class NoneAKException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message
def initial_AK_pond():   #初始化ak 池 0 为有额度 1为额度已经用完 保存成数组格式
    global ak_dic
    ak_dic = {}
    ak_dic = {
        "UKg9gDjYcHMB5hSFMi1HxuQz18f041t1": 0,
        "kIzerPbQFAhs01H85XRNvngmXU73RF8L": 0,
        "mKOV9991B7N98C46kUeNRUXScM067Xys": 0,
        "hvZ5O0of19Alfl7HShUWyOVlFiD8WYWG": 0,
        "5tlPS97zCcgTjbk6gy6AnLVG4p2jtg7u": 0,
        "WsBD1YKmVGBG9TGcpoewf3f05f8wqbQH": 0,
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
        "yHHqlqI0pLycBZVlMRjCFtQ8HSyMVWgv": 0,
        "cON4dGCQZyz5IqglB7dYcbCPyrYxoxu1": 0,
    }
def exchange_AK():
    for line in ak_dic.items():
        if line[1] == 0:
            return line[0]
    print("ak池的额度全部用完了")
    return None

def reverseLng(name,lng, lat,ak):   #经纬度反向解析   经度在前 纬度在后
    add_list = []
    url = "http://api.map.baidu.com/geocoder/v2/"
    output = 'json'
    ak = ak
    url_send = url + "?callback=renderReverse&location=%s,%s&output=json&pois=1&latest_admin=1&ak=%s" % (lat, lng, ak)
    req = urlopen(url_send)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    print(res)
    if str(res[:29]) == 'renderReverse&&renderReverse(':
        temp = json.loads(res[29:-1])
        district = temp['result']['addressComponent'].get('district',' ')
        formatted_address = temp['result'].get('formatted_address',' ')
        street = temp['result']['addressComponent'].get('street',' ')  #获取小区所在街道 用于建立标准路库
        city = temp['result']['addressComponent'].get('city',' ')
        road_file.write(name+"^"+city + "^" + district + "^" + street+"^"+formatted_address+"^"+lat+"^"+lng+"\n")  #写入文件
        print(street+"已完成")
        road_file.flush()
    else:
        temp = json.loads(res)
        if temp['status'] == 301 or temp['status'] == 302 or temp['status'] == 401 or temp['status'] == 402:
            print("捕获到AK额度不够的异常")
            ak_dic[ak] = 1  # 将当前AK的状态设置为已经跑完  P.S 1为已经跑完 0 为还有剩余额度
            ak = exchange_AK()  # 换一个AK
            print("已经更换AK", ak)
            if ak == None:  # 如果调用ak 之后为None 证明ak池的额度全部用完 错误文件记录当前运行结束时的状态
                print("配额全部用完啦！")
                raise NoneAKException("AK用完了") 
            print("-----------------等待3s-------------------")
            time.sleep(3)
            reverseLng(name,lng,lat,apartment,ak)
        else:
            raise Exception
        
            
def reverseLng1(name,lng, lat,apartment,ak):   #经纬度反向解析   经度在前 纬度在后
    add_list = []
    url = "http://api.map.baidu.com/geocoder/v2/"
    output = 'json'
    ak = ak
    url_send = url + "?callback=renderReverse&location=%s,%s&output=json&pois=1&latest_admin=1&ak=%s" % (lat, lng, ak)
    req = urlopen(url_send)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    print(res)
    if str(res[:29]) == 'renderReverse&&renderReverse(':
        temp = json.loads(res[29:-1])
        district = temp['result']['addressComponent'].get('district',' ')
        formatted_address = temp['result'].get('formatted_address',' ')
        street = temp['result']['addressComponent'].get('street',' ')  #获取小区所在街道 用于建立标准路库
        #city = temp['result']['addressComponent'].get('city','')
        road_file.write(apartment+"^"+name+"^"+ district + "^" + street+"^"+formatted_address+"^"+lat+"^"+lng+"\n")  #写入文件
        print(street+"已完成")
        road_file.flush()
    else:
        temp = json.loads(res)
        if temp['status'] == 301 or temp['status'] == 302 or temp['status'] == 401 or temp['status'] == 402:
            print("捕获到AK额度不够的异常")
            ak_dic[ak] = 1  # 将当前AK的状态设置为 已经跑完  P.S 1为已经跑完 0 为还有剩余额度
            ak = exchange_AK()  # 换一个AK
            print("已经更换AK", ak)
            if ak == None:  # 如果调用ak 之后为None 证明ak池的额度全部用完 错误文件记录当前运行结束时的状态
                print("配额全部用完啦！")
                raise NoneAKException("AK用完了") 
            print("-----------------等待3s-------------------")
            time.sleep(3)
            reverseLng1(name,lng,lat,apartment,ak)
        else:
            raise Exception
            
def read_Company_Info(ak):  #读取所有商家信息
    data = xlrd.open_workbook("D:\\广州公司1.xlsx")  # 文件名以及路径
    list_lat_lnt=[]
    global save_list
    save_list = open("D:\\已经爬取公司经纬度.txt",'a+',encoding='utf-8-sig')
    save_list.seek(0,0)   #光标置于文件开始处
    list_lat_lnt=[line.replace("\n", "") for line in save_list]
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(nrows):
        lat_lnt=str(table.row_values(i)[3]).strip()+","+str(table.row_values(i)[2]).strip()+","+str(table.row_values(i)[0]).strip()
        if lat_lnt in list_lat_lnt:
            print(lat_lnt+"已经搜索过")
            continue
        try:
            reverseLng(str(table.row_values(i)[0]).strip(),str(table.row_values(i)[3]).strip(),str(table.row_values(i)[2]).strip(),ak)
        except NoneAKException as e:  # 捕捉AK额度不够的异常
            break
        except Exception as e:
            error_list.write("其他异常:爬取区域为"+lat_lnt+"\n")
            error_list.write(traceback.format_exc()+"\n")
            error_list.flush()
        save_list.write(lat_lnt +"\n")  #写入爬取经纬度和公司主键
        save_list.flush()
    save_list.close()
    
def read_Appartment_Info(ak):#读取所有小区信息
    file = open("D:\\长春_安居客路库.txt", encoding='utf-8-sig')
    list_lat_lnt=[]
    global save_plot
    save_plot = open("D:\\已经爬取小区经纬度.txt",'a+',encoding='utf-8-sig')
    save_plot.seek(0,0)
    list_lat_lnt=[line.replace("\n", "") for line in save_plot]
    data = json.load(file)
    for line in data['result']:
        lat_lnt = line['lng'].strip()+","+line['lat'].strip()+","+line['name'].strip()
        if lat_lnt in list_lat_lnt:
            print(lat_lnt, "已经搜索过")
            continue
        try:
            #reverseLng(name,line['lng'],line['lat'],ak)
            road_file.write(line['name'].strip()+"^"+line['name'].strip()+"^"+line['district'].strip()+ "^" +line['street'].strip()+"^"+line['formatted_address'].strip()+"^"+line['lat'].strip()+"^"+line['lng'].strip()+"\n")
            road_file.flush()
            for i in line['add_list']:
                reverseLng1(i['name'].strip(),i['lng'].strip(), i['lat'].strip(),line['name'].strip(), ak)
        except NoneAKException as e:  # 捕捉AK额度不够的异常
            break
        except Exception as e:
            error_list.write("其他异常:爬取区域为"+lat_lnt+"\n")
            error_list.write(traceback.format_exc()+"\n")
            error_list.flush()
        save_plot.write(lat_lnt+"\n")
        save_plot.flush()
    save_plot.close()
    
if __name__ == "__main__":
    global road_file
    global error_list
    road_file = open("D:\\All_roads.txt",'a+',encoding='utf8')
    error_list = open("D:\\error_list.txt",'a+',encoding='utf8')
    ak = 'WsBD1YKmVGBG9TGcpoewf3f05f8wqbQH'
    initial_AK_pond()
    read_Appartment_Info(ak)  #先将安居客路库信息 跑完
    #read_Company_Info(ak)   #再跑所有商家信息
    road_file.close()
    error_list.close()