import requests
import bs4
from bs4 import BeautifulSoup


def get_urltext(url):
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('*' * 10 + ' Exceptions ' + '*' * 10)
        return ""


def fill_funds_list(flist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        funds = []
        for td in tr.children:
            value = td.string
            if value is not None:
                funds.append(value)
            else:
                for span in td.children:
                    funds.append(span.string)
        flist.append(funds)


def print_funds_list(flist, num):
    tplt = "{0:^8}\t{1:{4}^14}\t{2:^6}\t{3:^6}\t"
    print(tplt.format("基金代码", "基金名称", "净值", "近一年收益率", chr(12288)))
    for i in range(num):
        l = flist[i]
        print(tplt.format(l[0], l[1], l[2], l[9], chr(12288)))


from openpyxl.styles import numbers
from openpyxl import Workbook


def write_to_file(flist):
    wb = Workbook()
    ws = wb.active
    xlsx_header = ["序号", "基金代码", "基金名称", "净值", "日期", "日增长率", "近1周",
                   "近1月", "近3月", "近6月", "近1年", "近2年", "近3年", "今年来", "成立来"]
    ws.append(xlsx_header)
    number = 1
    for i in flist:
        xlsx_content = []
        xlsx_content.append(number)
        number += 1
        xlsx_content.extend(i)
        # xlsx_content.append(i[9])
        ws.append(xlsx_content)
    wb.save("funds.xlsx")

    # with open('funds_spider.csv','wb',newline='',encoding='utf-8') as f:
    # 	writer = csv.writer(f)
    # 	csv_header= ["序号","基金代码", "基金名称", "净值", "近一年收益率"]
    # 	writer.writerow(csv_header)
    # 	number = 1

    # 	for i in flist:
    # 		csv_content=[]
    # 		csv_content.append(number)
    # 		number+=1
    # 		csv_content.extend(i[:3])
    # 		csv_content.append(i[9])
    # 		writer.writerow(csv_content)


def main():
    funds_url = 'http://fund.eastmoney.com/trade/gp.html'
    funds_list = []
    html = get_urltext(funds_url)
    fill_funds_list(funds_list, html)
    print_funds_list(funds_list, 20)
    write_to_file(funds_list)


if __name__ == '__main__':
    main()
