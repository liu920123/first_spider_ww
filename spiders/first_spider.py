# -*- coding: utf-8 -*-
"""
Created on 2022-04-20 23:04:37
---------
@summary:
---------
@author: 92044
"""
import time
import feapder
import datetime
import traceback
import requests
from lxml import etree
import random
from feapder.utils import metrics

class Tess():
    def __init__(self):

        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
            "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
        ]

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': random.choice(self.user_agents)
        }


    def get_html(self,url):
        num = 0
        while num < 20:
            try:
                num += 1
                metrics.init()
                print("@@@@@@@@@@@@@@@@@", url)
                # print(proxies)
                start_time = time.time()
                r = requests.get(url, headers=self.headers, timeout=10, proxies='')
                end_time = time.time()
                metrics.emit_counter("请求时长", count=int(end_time-start_time), classify="运行时长")
                metrics.close()
                if r.status_code == 200:
                    return r
                elif r.status_code == 404:
                    return ''
                else:
                    print("ip被封，切换代理")
            except Exception as e:
                traceback.print_exc()
                pass


    def html_info(self,ll_url, ll_name,url_z,url,tim):
        try:
            res = self.get_html(ll_url)
            res.encoding = "utf-8"
            res_info = etree.HTML(res.text)
            jt_url = res_info.xpath('//div[@class="dConL"]//td/a[contains(@href,"content")]/@href')
            print(jt_url)
            jt_name = res_info.xpath('//div[@class="dConL"]//td/a[contains(@href,"content")]//text()')
            for index, jt_nnn in enumerate(jt_url):
                jt_nnn = url_z + jt_nnn
                print("***************",jt_nnn, jt_name[index],ll_name,url)

        except Exception as e:
            traceback.print_exc()
            print(e)


    def run(self,url,url_z,tim):
        try:
            res = self.get_html(url)
            if res:
                res.encoding = "utf-8"
                res_info = etree.HTML(res.text)
                ll = res_info.xpath('//div[@id="bmdh"]//td/a[contains(text(),"第")]/@href')
                ll_name = res_info.xpath('//div[@id="bmdh"]//td/a[contains(text(),"第")]/text()')
                for index, ll_url in enumerate(ll):
                    urll_ = url_z + ll_url.replace("./","")
                    print("!!!!!!!!!!!!",urll_)
                    self.html_info(urll_, ll_name[index],url_z,url,tim)
            else:
                pass
        except Exception as e:
                traceback.print_exc()
                print(e)

    def time_end_start(self,i):
        aaa = datetime.datetime.strptime('2019-08-16', '%Y-%m-%d')
        threeDayAgo = (aaa + datetime.timedelta(days=i))
        return threeDayAgo

    "http://newpaper.dahe.cn/dhb/html/2018-02/28/node_897.htm"
    def start(self):
        for i in range(0, 1065):
            tim = self.time_end_start(i)
            tim = str(tim).replace("00:00:00", "").replace(" ", "")
            tim_l = tim.split("-")
            tim_1 = tim_l[0] + "-" + tim_l[1]
            tim_2 = tim_l[-1]
            print(tim_1, tim_2)
            url = "http://newpaper.dahe.cn/dhb/html/{}/{}/node_897.htm".format(tim_1, tim_2)
            url_z = "http://newpaper.dahe.cn/dhb/html/{}/{}/".format(tim_1, tim_2)
            self.run(url, url_z, tim)

if __name__ == '__main__':
    aa = Tess()
    aa.start()



