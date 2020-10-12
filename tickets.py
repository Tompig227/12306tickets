from stations import stations
from prettytable import PrettyTable
from selenium import webdriver
import datetime
import requests
import json
import re
import time
header = ["车次","出发站","到达站","出发时间","到达时间","历时","商务座","一等座","二等座","高级软卧","软卧","动卧","硬卧","软座","硬座","无座"]
def get_tickets(froms,tos,date):
    froms = stations[froms]
    tos = stations[tos]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('https://www.12306.cn/index/index.html')
    time.sleep(3)
    Cookie = browser.get_cookies()
    strr = ''
    for c in Cookie:
        strr += c['name']
        strr += '='
        strr += c['value']
        strr += ';'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'Cookie':strr
        }
    print(headers)
    browser.quit()
    request_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,froms,tos)
    response = json.loads(requests.get(request_url,headers=headers).text)
    result = response['data']['result']
    new_list = []
    for item in result:
        if not '列车停运' in item:
            new_list.append(item)
        else:
            pass
    return new_list

def get_info():
    fw = input("请输入出发地>>>")
    tw = input("请输入目的地>>>")
    st = input("请输入出发时间；格式：(年-月-日)(默认为今日日期)>>>>")
    if st == '':
        st = datetime.date.today()
        return fw,tw,st
    else:
        today = datetime.date.today()
        date = str(today).split('-')
        list = st.split('-')
        if int(list[0]) < int(date[0]) or int(list[0]) > int(date[0]):
            exit("输入的年份不在我的查询范围之内")
        else:
            if int(list[1]) < int(date[1]) or int(list[1]) > int(date[1])+1:
                exit("你输入的月份不在我的查询范围之内")
            else:
                if int(list[2]) < int(date[2]):
                    exit("你输入的日期不在我的查询范围之内")
                else:
                    if int(list[1]) < 10 and int(list[1][0]) != 0:
                        list[1] = '0' + list[1]
                    if int(list[2]) < 10 and int(list[2][0]) != 0:
                        list[2] = '0' + list[2]
                    return fw,tw,list[0] + '-' + list[1] + '-' + list[2]

def decrypt(string):
    string = ''.join(string)
    reg = re.compile('.*?\|预订\|.*?\|(.*?)\|.*?\|.*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|.*?\|.*?\|.*?\|.*')
    result = re.findall(reg,string)[0]
    return result

if __name__ == '__main__':
    pt = PrettyTable()
    pt.field_names = header
    [fw,tw,st]=get_info()
    trainlist=get_tickets(fw,tw,st)
    new_dict = {v: k for k, v in stations.items()}
    for item in trainlist:
        result=list(decrypt(item))
        result[1] = new_dict[result[1]]
        result[2] = new_dict[result[2]]
        results = [result[0],result[1],result[2],result[3],result[4],result[5],result[-1],result[-2],result[-3],result[-12],result[-10],result[-6],result[-5],result[-8],result[-4],result[-7]]
        pt.add_row(results)
    print(pt)
