import re
import xlrd
import openpyxl
from openpyxl.utils import get_column_letter

def txt_to_xlsx(filename, outfile): # txt转xlsx
    fr = open(filename, 'r+', encoding='utf8')
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Sheet1'
    row = 0
    for line in fr:
        row += 1
        line = line.strip()
        line = line.split('^')
        col = 0
        for j in range(len(line)):
            col += 1
            ws.cell(column=col, row=row, value=line[j].format(get_column_letter(col)))
    wb.save(outfile)

if __name__ == "__main__":
    new_txt = '/Users/Shar/Desktop/Sheets/上海_公司_补充_标准.txt'
    new_sheet = '/Users/Shar/Desktop/Sheets/上海_公司_补充_标准.xlsx'
    std_file = open(new_txt, 'w', encoding='utf8')
    data = xlrd.open_workbook("/Users/Shar/Desktop/Sheets/上海公司地址补充.xlsx")
    #data = xlrd.open_workbook("/Users/Shar/Desktop/Sheets/Debug.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows
    # district_pattern = re.compile(".*?区(.*)") # 把‘区’后面的内容取出来
    # city_pattern = re.compile(".*?市(.*)") # 把‘市’后面的内容取出来
    village_pattern = re.compile(".+?[路街巷号镇村](.+?[镇村]).*?") # 若为xx路xx村，取出中间的xx村的内容
    village_pattern_1 = re.compile(".+?\d+(.+?[镇村]).*?")  # 若为 数字xx村，取出中间的xx村的内容
    village_pattern_2 = re.compile("(.*?[镇村]).*?") # xxx村|镇,取出第一个 村|镇 及之前的内容
    village_pattern_clear = re.compile(".*?[号弄区路](.*?)") # 去除村前面的多余信息
    parenthesis_pattern = re.compile(".*?\((.*?)\)") # xxx(xx), 取出括号里的内容
    parenthesis_out_pattern = re.compile("(.*?)\(.*?\)") # 截取括号外的内容
    road_pattern = re.compile(".+?[区镇村](.+?[路道])") # xxx路|道， 取出在第一个 路|道 及 区|镇|村| 之间的内容
    road_pattern_hat = re.compile(".+?[区镇村](.+?[街巷])")  # xxx街|巷， 取出在第一个 街|巷 及 区|镇|村| 之间的内容
    road_pattern_1 = re.compile(".+?与(.+?[路街道巷])") # 若出现了两个路名交叉口，取后面的路名
    road_pattern_11 = re.compile("(.+?[路道])") # xxx路|道， 取出第一个 路|道 及之前的内容
    road_pattern_12 = re.compile("(.*?[^\d][街巷弄])") # xxx街|巷|弄,取出第一个 街|巷|弄 及之前的内容，且之前的内容不能有数字
    road_pattern_2 = re.compile("(.*？)[^\d+]") # 取出第一个数字前的所有内容
    road_pattern_clear = re.compile(".*?\d+(.*？)") # 去除公交车号（81路）
    num_left_pattern = re.compile(".+?[路村道街巷镇](.+)") # 取出 路|村|道|街|巷 后面的内容
    num_pattern = re.compile(".*?(\d+)(号|弄|幢|临|-|$)") # 取出数字，且后面不跟‘米’
    first_ten_pattern = re.compile("(十)[^一二三四五六七八九]")
    first_ten_1_pattern = re.compile("(十)[一二三四五六七八九]")
    middle_ten_pattern = re.compile(".*?[一二三四五六七八九](十)[一二三四五六七八九]")
    last_ten_pattern = re.compile(".*?[一二三四五六七八九](十)[^一二三四五六七八九]")
    count = 0
    for i in range(nrows):
        count = count + 1
        temp = str(table.row_values(i)[4]).strip()
        city = str(table.row_values(i)[2]).strip()
        district = str(table.row_values(i)[3]).strip()
        village_name = ' '
        road_name = ' '
        num_str = ' '
        # 如果地址信息不为空
        if not temp.isspace():

            # 去掉区市信息
            if city in temp:
                temp = temp[len(city):]
            if district in temp:
                temp = temp[len(district):]

            # # 把‘区’后面的内容取出来，如果没有区，就把‘市’后面的内容取出来
            # district_match = district_pattern.match(temp)
            # if district_match:
            #     temp = district_match.group(1)
            # else:
            #     city_match = city_pattern.match(temp)
            #     if city_match:
            #         temp = city_match.group(1)

            # temp里的市、区内容已被去除
            # 将剩下的内容分为括号里和括号外
            temp_out_match = parenthesis_out_pattern.match(temp)
            if temp_out_match:
                temp_out = temp_out_match.group(1)
            else:
                temp_out = temp

            # 括号外内容，如果有‘村|镇’的信息，提取出来
            village_match = village_pattern.match(temp_out)
            village_match_1 = village_pattern_1.match(temp_out)
            village_match_2 = village_pattern_2.match(temp_out)
            if village_match:
                village_name = village_match.group(1)
            elif village_match_1:
                village_name = village_match_1.group(1)
            elif village_match_2:
                village_name = village_match_2.group(1)

            # 若出现了 xx村|镇|区xx路|道，取xx路|道作为路名
            # 若出现了 xx村|镇|区xx街|巷，取xx街|巷作为路名
            # 如果没有，但是出现了 xx路|道，则将这个作为路名
            # 还是没有，则检索关键字 xx街|巷|弄， 且前面要没有数字，将这个作为路名

            # 如果以上都没有，则检索关键字 xx镇|村， 且前面要没有数字，将这个作为路名
            road_match = road_pattern.match(temp_out)
            road_match_hat = road_pattern_hat.match(temp_out)
            road_match_1 = road_pattern_1.match(temp_out)
            road_match_11 = road_pattern_11.match(temp_out)
            road_match_12 = road_pattern_12.match(temp_out)
            if road_match:
                road_name = road_match.group(1)
            elif road_match_hat:
                road_name = road_match_hat.group(1)
            elif road_match_1:
                road_name = road_match_1.group(1)
            elif road_match_11:
                road_name = road_match_11.group(1)
            elif road_match_12:
                road_name = road_match_12.group(1)
            # 若未能提取出，就看括号里的字段
            # 如果 村|镇 信息为空，则先看 村|镇 信息
            # 重复上面五个过程提取路名
            # 所有的情况不符合，则取数字前的整个字段作为路名
            else:
                parenthesis_match = parenthesis_pattern.match(temp)
                if parenthesis_match:
                    temp_in= parenthesis_match.group(1)
                    if village_name == ' ':
                        village_match = village_pattern.match(temp_out)
                        village_match_1 = village_pattern_1.match(temp_out)
                        village_match_2 = village_pattern_2.match(temp_out)
                        if village_match:
                            village_name = village_match.group(1)
                        elif village_match_1:
                            village_name = village_match_1.group(1)
                        elif village_match_2:
                            village_name = village_match_2.group(1)

                    road_match = road_pattern.match(temp_in)
                    road_match_hat = road_pattern_hat.match(temp_in)
                    road_match_1 = road_pattern_1.match(temp_in)
                    road_match_11 = road_pattern_11.match(temp_in)
                    road_match_12 = road_pattern_12.match(temp_in)
                    if road_match:
                        road_name = road_match.group(1)
                    elif road_match_hat:
                        road_name = road_match_hat.group(1)
                    elif road_match_1:
                        road_name = road_match_1.group(1)
                    elif road_match_11:
                        road_name = road_match_11.group(1)
                    elif road_match_12:
                        road_name = road_match_12.group(1)
                else:
                    road_match_2 = road_pattern_2.match(temp)
                    if road_match_2:
                        road_name = road_match_2.group(1)

            if village_name == '新村' or village_name == '府村':
                village_name = ' '
            village_match_clear = village_pattern_clear.match(village_name)
            if village_match_clear:
                village_name = village_match_clear.group(1)
            road_match_clear = road_pattern_clear.match(road_name)
            if road_match_clear:
                road_name = ' '


            # 从temp里取出号
            # 把 路|村|道|街|巷|弄 后面的内容取出来
            num_left = ' '
            num_left_match = num_left_pattern.match(temp)
            if num_left_match:
                num_left = num_left_match.group(1)
            # 取出来的内容进行文字->阿拉伯数字的转换
            if num_left != ' ':
                first_ten = first_ten_pattern.match(num_left)
                first_ten_1 = first_ten_1_pattern.match(num_left)
                middle_ten = middle_ten_pattern.match(num_left)
                last_ten = last_ten_pattern.match(num_left)

                if first_ten:
                    num_left = num_left.replace("十", "10")
                elif first_ten_1:
                    num_left = num_left.replace("十", "1")
                elif middle_ten:
                    num_left = num_left.replace("十", "")
                elif last_ten:
                    num_left = num_left.replace("十", "0")

                num_left = num_left.replace("一", "1")
                num_left = num_left.replace("二", "2")
                num_left = num_left.replace("三", "3")
                num_left = num_left.replace("四", "4")
                num_left = num_left.replace("五", "5")
                num_left = num_left.replace("六", "6")
                num_left = num_left.replace("七", "7")
                num_left = num_left.replace("八", "8")
                num_left = num_left.replace("九", "9")
                num_left = num_left.replace("〇", "0")

                # 转换好以后的字段，取出第一个数字前的所有内容
                match_num = num_pattern.match(num_left)
                if match_num:
                    num_str = match_num.group(1)
        else:
            pass
        print(str(count) + "   " + temp + "              " + village_name + "              " + road_name + "           " + num_str)
        std_file.write(str(table.row_values(i)[0]).strip() + '^' + str(table.row_values(i)[1]).strip() + '^' +
                        str(table.row_values(i)[2]).strip() + '^' + str(table.row_values(i)[3]).strip() + '^' +
                        str(table.row_values(i)[4]).strip() + '^' + str(table.row_values(i)[5]).strip() + '^' +
                        str(table.row_values(i)[6]).strip() + '^' + village_name + '^' + road_name + '^' + num_str + '\n')
    print("Successfully saved to " + new_txt)
    txt_to_xlsx(new_txt, new_sheet)
    print("Successfully converted to " + new_sheet)
    print("-------------------------------------ALL JOBS DONE-----------------------------------")
    std_file.close()