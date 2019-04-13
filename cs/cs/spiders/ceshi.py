# -*- coding: utf-8 -*-
import scrapy


class CeshiSpider(scrapy.Spider):
    name = 'ceshi'
    # allowed_domains = ['httpbin.org']
    # start_urls = ['http://httpbin.org/ip']

    def start_requests(self):
        for i in range(10):
            # url = 'http://httpbin.org/user-agent'
            url = 'http://httpbin.org/ip'
            yield scrapy.Request(url=url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        # print(response.status)
        print(response.text)


