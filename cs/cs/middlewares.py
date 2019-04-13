# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import user_agent
import requests
import re

class user_agent_DownloaderMiddleware(object):

    def process_request(self,request,spider):
        request.headers['user-agent'] = user_agent.generate_user_agent()


class proxy_DownloaderMiddleware(object):

    def __init__(self):
        # 含国外ip,扩大爬取数量请修改getnum
        self.ip_url = 'http://www.66ip.cn/nmtq.php?getnum=10'
        self.yanzhen_url = 'http://www.baidu.com'
        self.ip_list = []
        self.count = 0
        self.evecount = 0

    def getip(self):
        headers = {'user-agent': user_agent.generate_user_agent()}
        res = requests.get(url=self.ip_url, headers=headers)
        if res.status_code != 200:
            self.getip()

        text = re.findall('\d+.\d+.\d+.\d+:\d+', res.content.decode('gbk'))
        self.ip_list.clear()
        self.ip_list = text


    def yanzhen(self):
        try:
            if len(self.ip_list) == 0:
                self.getip()
            proxy = random.choice(self.ip_list)
            headers={'user-agent':user_agent.generate_user_agent()}
            status = requests.get(url=self.yanzhen_url,proxie={'http://'+str(proxy)},
                                  timeout=5,headers=headers)
            if status.status_code != 200:
                self.ip_list.remove(proxy)
                self.yanzhen()

            return proxy
        except:
            print('.........')


    def process_request(self, request, spider):

        # 当count等于0或者大于10求得ip
        # if self.count == 0 or self.count >10:
        #     self.getip()
        #     self.count = 1
        # 当使用次数超过多少次才进行切换,避免给代理ip网址压力
        # bug 当某个ip无法快速访问,会导致ip使用次数增加切换到下一个
        # if self.evecount == 3:
        #     self.count += 1
        #     self.evecount = 0
        # else:
        #     self.evecount += 1

        if len(self.ip_list) == 0:
            self.getip()

        # proxy = self.ip_list[self.count-1]
        proxy = random.choice(self.ip_list)
        # proxy = self.yanzhen()
        request.meta['proxy'] = 'http://' + str(proxy)

        # 当self.ip_list总共使用了多少次之后重新抓取
        self.evecount +=1
        if self.evecount == 40:
            self.getip()

    # 当proxy代理出现问题不可用,那么response检查出现状态码不等于200重新request
    def process_response(self, request, response, spider):
        if response.status != 200:
            if len(self.ip_list) == 0:
                self.getip()
                proxy = random.choice(self.ip_list)
                request.meta['proxy'] = 'http://' + proxy
                return request

            proxy = random.choice(self.ip_list)
            request.meta['proxy'] = 'http://' + proxy
            return request

        return response