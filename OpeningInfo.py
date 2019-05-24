import requests, re, pandas as pd
from lxml import etree

token = "xxxxxxxxxxxxxxxxx"
xq = "2019-2020-1"
url = "http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksJxjhBs.do"
cookies = {"JSESSIONID": "xxxxxxxxxxxxxxxxx"}
headers = {"Host": "zhjw.cic.tsinghua.edu.cn",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.7,zh-HK;q=0.6,en-US;q=0.4,en;q=0.3,ja;q=0.1",
           "Accept-Encoding": "gzip, deflate", "Referer": "http://zhjw.cic.tsinghua.edu.cn/xkBks.vxkBksJxjhBs.do",
           "Content-Type": "application/x-www-form-urlencoded", "Content-Length": "311", "DNT": "1",
           "Connection": "keep-alive",
           "Upgrade-Insecure-Requests": "1", "Pragma": "no-cache", "Cache-Control": "no-cache"}


def get_info(page=1):
    max_page = -1
    rs = []
    columns = []
    data_dict = {"goPageNumber": page, "m": "kkxxSearch", "p_kcflm": "", "p_kch": "", "p_kcm": "", "p_kctsm": "",
                 "p_kkdwnm": "", "p_rxklxm": "", "p_skjc": "", "p_skxq": "", "p_sort.asc1": "true",
                 "p_sort.asc2": "true",
                 "p_sort.p1": "", "p_sort.p2": "", "p_ssnj": "", "p_xkwzsm": "", "p_xnxq": xq,
                 "p_zjjsxm": "",
                 "page": page, "pathContent": "%D2%BB%BC%B6%BF%CE%BF%AA%BF%CE%D0%C5%CF%A2", "showtitle": "",
                 "token": token}
    while max_page < 0 or page < max_page:
        try:
            data_dict['page'] = page
            res = requests.post(url, data=data_dict, headers=headers, cookies=cookies)
            doc: etree._Element = etree.HTML(res.text)
            rs += [
                [''.join(td.itertext()).replace("链接加入了课程分类代码用于区分本研", '').replace('\r', '').replace('\n', '').replace(
                    '\t', '').replace(' ', '') for td in tr.getchildren()] for tr in
                doc.xpath("/html/body/div[1]/form/div/div/div/div/div[4]/table/tr")[1:]]
            if max_page == -1:
                tr = doc.xpath("/html/body/div[1]/form/div/div/div/div/div[4]/table/tr")[0]
                columns = [
                    ''.join(td.itertext()).replace("链接加入了课程分类代码用于区分本研", '').replace('\r', '').replace('\n', '').replace(
                        '\t', '').replace(' ', '') for td in tr.getchildren()]
                max_page = int(re.compile(r'共 (\d+) 页').search(doc.xpath('//*[@id="endpage"]')[0].tail).groups()[0])
            if page % 10 == 0: print("[%d/%d]" % (page, max_page))
        except Exception as e:
            print(e)
            continue
        else:
            page += 1
    return pd.DataFrame(rs, columns=columns)


if __name__ == '__main__':
    with open('OpeningInfo.xlsx', 'wb') as f:
        get_info().to_excel(f, index=False)
