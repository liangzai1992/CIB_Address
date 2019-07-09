import re
import xlrd

if __name__ == "__main__":
    road_file = open("D:\\上海_公司_标准路_1.txt",'w',encoding='utf8')
    data = xlrd.open_workbook("D:\\上海_公司_标准路.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows
    road_pattern=re.compile(".*?[^路]\((.*?)\)")
    road_pattern_1=re.compile("(.*?(路|大道|街))")
    road_pattern_2=re.compile("(.+)")
    num_leftpattern=re.compile(".*?(路|大道|街)(.+)")
    num_pattern=re.compile(".*?(\d+)")
    first_ten_pattern=re.compile("(十)[^一二三四五六七八九]")
    first_ten_1_pattern=re.compile("(十)[一二三四五六七八九]")
    middle_ten_pattern=re.compile(".*?[一二三四五六七八九](十)[一二三四五六七八九]")
    last_ten_pattern=re.compile(".*?[一二三四五六七八九](十)[^一二三四五六七八九]")
    for i in range(nrows):
        temp=str(table.row_values(i)[3]).strip()
        road_name=' '
        road_match=road_pattern.match(temp)
        if road_match:
            road_name=road_match.group(1)
        else:
            road_match_1=road_pattern_1.match(temp)
            if road_match_1:
                road_name=road_match_1.group(1)
            else:
                road_match_2=road_pattern_2.match(temp)
                if road_match_2:
                    road_name=road_match_2.group(1) 
        temp=str(table.row_values(i)[4]).strip()
        num_left=' '
        num_leftmatch=num_leftpattern.match(temp)
        if num_leftmatch:
            num_left=num_leftmatch.group(2)
        num_str=' '
        if num_left != ' ':
            first_ten=first_ten_pattern.match(num_left)
            first_ten_1=first_ten_1_pattern.match(num_left)
            middle_ten=middle_ten_pattern.match(num_left)
            last_ten=last_ten_pattern.match(num_left)
        
            if first_ten:
                num_left=num_left.replace("十","10")
            elif first_ten_1:
                num_left=num_left.replace("十","1")
            elif middle_ten:
                num_left=num_left.replace("十","")
            elif last_ten:
                num_left=num_left.replace("十","0")
            num_left=num_left.replace("一","1")
            num_left=num_left.replace("二","2")
            num_left=num_left.replace("三","3")
            num_left=num_left.replace("四","4")
            num_left=num_left.replace("五","5")
            num_left=num_left.replace("六","6")
            num_left=num_left.replace("七","7")
            num_left=num_left.replace("八","8")
            num_left=num_left.replace("九","9")
            match_num=num_pattern.match(num_left)
            if match_num:
                num_str=match_num.group(1)
        road_file.write(str(table.row_values(i)[0]).strip()+'^'+str(table.row_values(i)[1]).strip()+'^'+
                        str(table.row_values(i)[2]).strip()+'^'+str(table.row_values(i)[4]).strip()+'^'+str(table.row_values(i)[5]).strip()+'^'+
                        str(table.row_values(i)[6]).strip()+'^'+road_name+'^'+num_str+'\n')
    road_file.close()