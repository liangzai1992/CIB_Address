import xlrd
import numpy as np

def pattern_roadnum(public_address,district_key,line3):
    decrease_num_list=[]
    for num in public_address[line3[1]][district_key][line3[5]].keys():
        temp=[]
        decrease_num=abs(int(num)-int(line3[6]))
        temp.append(decrease_num)
        temp.append(num)
        temp.append(public_address[line3[1]][district_key][line3[5]][num])
        decrease_num_list.append(temp)
    min_num=10000000000
    for decrease_number in decrease_num_list:
        min_num=min(decrease_number[0],min_num)
    for decrease_number in decrease_num_list:
        if min_num==decrease_number[0]:
            pattern_addr.write(line3[0]+'^'+line3[1]+'^'+district_key+'^'+line3[3]+'^'+line3[4]+'^'+line3[5]+'^'+
                               line3[6]+'^'+line3[7]+'^'+line3[8]+'^'+str(decrease_number[2][0])+'^'+str(decrease_number[2][1])
                               +'^'+decrease_number[1]+'^'+' '+'\n')
            break

def pattern_averoadnum(public_address,district_key,line3):
    lat_list=[]
    lnt_list=[]
    for num in public_address[line3[1]][district_key][line3[5]].values():
        lat_list.append(float(num[0]))
        lnt_list.append(float(num[1]))
    mean_lat=np.mean(lat_list)
    mean_lnt=np.mean(lnt_list)
    pattern_addr.write(line3[0]+'^'+line3[1]+'^'+district_key+'^'+line3[3]+'^'+line3[4]+'^'+line3[5]+'^'+
    line3[6]+'^'+line3[7]+'^'+line3[8]+'^'+str(mean_lat)+'^'+str(mean_lnt)
    +'^'+' '+'^'+' '+'\n')
 
if __name__=="__main__":
    cust_homeaddr=open("D:\\地址清洗项目\\上海路库\\shanghai_standardaddr.txt",encoding="utf-8-ig")
    plot_publicaddr=xlrd.open_workbook("D:\\地址清洗项目\\上海路库\\上海小区匹配数据.xlsx")
    publicaddr=xlrd.open_workbook("D:\\地址清洗项目\\上海路库\\上海地址匹配数据1.xlsx")
    publiccity=open("D:\\地址清洗项目\\上海路库\\外部城市库.txt",encoding="utf-8-ig")
    publicdistrict=open("D:\\地址清洗项目\\上海路库\\外部区库.txt",encoding="utf-8-ig")
    publicroad=open("D:\\地址清洗项目\\上海路库\\外部路库.txt",encoding="utf-8-ig")
    pattern_addr=open("D:\\地址清洗项目\\上海路库\\最终匹配情况.txt","w",encoding="utf-8-ig")
    cust_list=[]
    plot_list=[]
    
    table_plot_publicaddr=plot_publicaddr.sheets()[0]
    nrows_plot_publicaddr=table_plot_publicaddr.nrows
    table_publicaddr=publicaddr.sheets()[0]
    nrows_publicaddr=table_publicaddr.nrows
    ###################读取外部小区地址###############################
    for line1 in range(nrows_plot_publicaddr):
        plot_temp=[]
        plot_temp.append(str(table_plot_publicaddr.row_values(line1)[0]))
        plot_temp.append(str(table_plot_publicaddr.row_values(line1)[1]))
        plot_temp.append(str(table_plot_publicaddr.row_values(line1)[2]))
        plot_temp.append(str(table_plot_publicaddr.row_values(line1)[3]))
        plot_list.append(plot_temp)
    ####################初始化外部地址字典##############################
    public_address={}
    for city in publiccity:
        city=city.replace("\n","")
        public_address[city]={}
        publicdistrict.seek(0,0)
        for district in publicdistrict:
            district=district.replace("\n","")
            public_address[city][district]={}
            publicroad.seek(0,0)
            for road in publicroad:
                road=road.split("\t")
                if road[0]==district:
                    road_name=road[1].replace("\n","")
                    public_address[city][district][road_name]={}
######################外部地址字典赋值###############################################
    for line2 in range(nrows_publicaddr):
        lat_lnt=[]
        lat_lnt.append(str(table_publicaddr.row_values(line2)[4]))
        lat_lnt.append(str(table_publicaddr.row_values(line2)[5]))
        public_address[str(table_publicaddr.row_values(line2)[0])][str(table_publicaddr.row_values(line2)[1])][str(table_publicaddr.row_values(line2)[2])][str(table_publicaddr.row_values(line2)[3])]=lat_lnt
############################匹配规则##################################################
    for line3 in cust_homeaddr:
        line3=line3.split(",")
        plot_name=[plot for plot in plot_list if plot[1]==line3[7] and plot[1]!='']
        if plot_name:
            pattern_addr.write(line3[0]+'^'+line3[1]+'^'+line3[2]+'^'+line3[3]+'^'+line3[4]+'^'+
                               line3[5]+'^'+line3[6]+'^'+line3[7]+'^'+line3[8]+'^'+
                               plot_name[0][2]+'^'+plot_name[0][3]+'^'+line3[6]+'^'+plot_name[0][0]+'\n')
        elif public_address.get(line3[1]) and public_address[line3[1]].get(line3[2]) and public_address[line3[1]][line3[2]].get(line3[5]) and public_address[line3[1]][line3[2]][line3[5]].get(line3[6]):
            lat_lnt_name=public_address[line3[1]][line3[2]][line3[5]][line3[6]]
            pattern_addr.write(line3[0]+'^'+line3[1]+'^'+line3[2]+'^'+line3[3]+'^'+line3[4]+'^'+
                               line3[5]+'^'+line3[6]+'^'+line3[7]+'^'+line3[8]+'^'+
                               str(lat_lnt_name[0])+'^'+str(lat_lnt_name[1])+'^'+line3[6]+'^'+' '+'\n')
        elif public_address.get(line3[1]) and public_address[line3[1]].get(line3[2]) and public_address[line3[1]][line3[2]].get(line3[5]):
            if line3[6]!='':
                pattern_roadnum(public_address,line3[2],line3)
            else:
                pattern_averoadnum(public_address,line3[2],line3)
        elif public_address.get(line3[1]):
            flag=0
            for district_key in public_address[line3[1]].keys():
                for road_key in public_address[line3[1]][district_key].keys():
                    if road_key==line3[5]:
                        if line3[6]!='':
                            pattern_roadnum(public_address,district_key,line3)
                        else:
                            pattern_averoadnum(public_address,district_key,line3)
                        flag=1
                        break
                else:
                    continue
                break
            if flag==0:
                pattern_addr.write(line3[0]+'^'+line3[1]+'^'+line3[2]+'^'+line3[3]+'^'+line3[4]+'^'+
                               line3[5]+'^'+line3[6]+'^'+line3[7]+'^'+line3[8]+'^'+' '+'^'+' '+
                               '^'+' '+'^'+' '+'\n')
        else:
            pattern_addr.write(line3[0]+'^'+line3[1]+'^'+line3[2]+'^'+line3[3]+'^'+line3[4]+'^'+
                               line3[5]+'^'+line3[6]+'^'+line3[7]+'^'+line3[8]+'^'+' '+'^'+' '+
                               '^'+' '+'^'+' '+'\n')            


        



    

       