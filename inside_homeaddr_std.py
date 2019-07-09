import codecs
import os
import sys
import re


def read_address():
    global city
    global district
    global town
    global road
    global plot
    global cust_address

    city = open("D:\\地址清洗项目\\上海路库\\shanghai_city.txt", encoding='uft-8-sig')
    district = open("D:\\地址清洗项目\\上海路库\\shanghai_district.txt", encoding='uft-8-sig')
    town = open("D:\\地址清洗项目\\上海路库\\shanghai_town.txt", encoding='uft-8-sig')
    road = open("D:\\地址清洗项目\\上海路库\\shanghai_road.txt", encoding='uft-8-sig')
    plot = open("D:\\地址清洗项目\\上海路库\\shanghai_plot.txt", encoding='uft-8-sig')
    cust_address = open("D:\\地址清洗项目\\上海路库\\SHANGHAI_RESIDENT_TSM_APPDATA.txt", encoding='uft-8-sig')

    global city_list
    global district_list
    global town_list
    global road_list
    global plot_list
    global cust_address_list

    city_list = []
    district_list = []
    town_list = []
    road_list = []
    plot_list = []
    cust_address_list = []

    for line in city:
        city_list.append(line.replace("\n", ""))
    for line in district:
        district_list.append(line.replace("\n", ""))
    for line in town:
        town_list.append(line.replace("\n", ""))
    for line in road:
        road_list.append(line.replace("\n", ""))
    for line in plot:
        plot_list.append(line.replace("\n", ""))
    for line in cust_address:
        line = line.split(",")
        temp = []
        temp.append(line[0])
        temp.append(line[1] + line[2] + line[3] + line[4].replace("\n", ""))
        cust_address_list.append(temp)
    city.close()
    district.close()
    town.close()
    road.close()
    plot.close()
    cust_address.close()


def Match_And_Cut():
    town_pattern = re.compile("(.*?(镇|街道))[^路]")
    village_pattern = re.compile("(.*?村)[^路]")
    road_pattern = re.compile("(.*?(大道|路|街))")
    num_pattern = re.compile(".*?(\d*?)[号弄幢栋组室-]")

    for line in cust_address_list:
        temp = line[1]

        city_str = " "
        for line1 in city_list:
            loc_city = temp.rfind(line1)
            if loc_city != -1:
                city_str = city_list[0]
                temp = temp[loc_city + len(line1):]
                break

        district_str = " "
        for line2 in district_list:
            loc_district = temp.rfind(line2)
            if loc_district != -1:
                loc_district_type = line2.find("区")
                if loc_district_type != -1:
                    district_str = line2
                else:
                    loc_country = line2.find("县")
                    if loc_country != -1:
                        district_str = line2[:loc_country] + "区"
                    else:
                        district_str = line2 + "区"
                temp = temp[loc_district + len(line2):]
                break
        ########################################################################
        town_str = " "
        match_town = town_pattern.match(temp)
        if match_town:
            town_tempstr = match_town.group(1)
            for town_name in town_list:
                if town_tempstr.find(town_name) != -1:
                    town_str = town_name
                    break
            loc_town = temp.find(town_tempstr)
            temp = temp[loc_town + len(town_tempstr):]

        match_roadaddr = " "
        road_name_list = []
        match_road = road_pattern.match(temp)
        if match_road:
            match_roadtempaddr = match_road.group(1)
            road_name_list = [road_name for road_name in road_list if match_roadtempaddr.find(road_name) != -1]
            if road_name_list:
                match_roadaddr = max(road_name_list, key=len)
            else:
                match_roadaddr = match_roadtempaddr
            loc_road = temp.find(match_roadtempaddr)
            temp = temp[loc_road + len(match_roadtempaddr):]

        village_str = " "
        plot_str = " "
        village_name_list = []
        match_village = village_pattern.match(temp)
        if match_village:
            village_tempstr = match_village.group(1)
            village_name_list = [line3 for line3 in plot_list if village_tempstr.find(line3) != -1]
            if village_name_list:
                plot_str = max(village_name_list, key=len)
            else:
                village_str = village_tempstr
            loc_village = temp.find(village_tempstr)
            temp = temp[loc_village + len(village_tempstr):]

        match_numaddr = " "
        match_num = num_pattern.match(temp)
        if match_num:
            match_numaddr = match_num.group(1)
            loc_num = temp.find(match_numaddr)
            temp = temp[loc_num + len(match_numaddr):]

        plot_name_list = []
        plot_name_list = [line4 for line4 in plot_list if temp.find(line4) != -1]
        if plot_name_list:
            plot_str = max(plot_name_list, key=len)
            loc_plot = temp.find(plot_str)
            temp = temp[loc_plot + len(plot_str):]

        standard_addr.write(line[0].strip() + "," + city_str.strip() + "," + district_str.strip() + "," \
                            + town_str.strip() + "," + village_str.strip() + "," \
                            + match_roadaddr.strip() + "," + match_numaddr.strip() + "," \
                            + plot_str.strip() + "," + line[1].strip() + "," + temp + "\n")
    standard_addr.close()


if __name__ == "__main__":
    global standard_addr
    standard_addr = open("D:\\地址清洗项目\\上海路库\\shanghai_standardaddr.txt", "a+", encoding="utf8")
    read_address()
    Match_And_Cut()
