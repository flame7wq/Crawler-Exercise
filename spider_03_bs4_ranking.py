from bs4 import BeautifulSoup
import requests
import bs4


def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('*' * 10 + ' Exceptions ' + '*' * 10)
        return ""


def fill_uni_list(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        utdlist = []
        for td in tr.children:
            td = str(td).replace('<!-- -->', '')
            td = td.replace('\n', '')
            td = BeautifulSoup(td, 'html.parser')
            value = td.string
            if value is None:
                value_soup = BeautifulSoup(str(td.find('a')), 'html.parser')
                value = value_soup.string
            value = value.replace(' ', '')
            utdlist.append(value)
        ulist.append(utdlist)


def print_uni_list(ulists, number):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}\t{4:^10}"
    print(tplt.format("排名", "学校", "总分", chr(12288), "地区"))
    for i in range(number):
        u = ulists[i]
        print(tplt.format(u[0], u[1], u[4], chr(12288), u[2]))


def main():
    uinfo = []
    ranking_url = 'https://www.shanghairanking.cn/rankings/bcur/2020'
    url_text = get_html(ranking_url)
    fill_uni_list(uinfo, url_text)
    print_uni_list(uinfo, 20)


if __name__ == '__main__':
    main()
