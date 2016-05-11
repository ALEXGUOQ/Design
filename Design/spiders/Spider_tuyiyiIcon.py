#-*- coding:utf-8 -*-
import scrapy

from Design.items import DesignItem


class Spider_tuyiyiIcon(scrapy.Spider):
    name = 'tuyiyiIcon'

    start_urls = [
        'http://www.tuyiyi.com/show-73',
    ]
    baseUrl = 'http://www.tuyiyi.com'

    def parse(self, response):
        for item in response.xpath('//div[@class="moquu_free"]/ul/li'):
            design = DesignItem()

            icon = item.xpath('./a/img/@src').extract()
            if icon:
                icon = icon[0]
                design['icon'] = icon
            else:
                design['icon'] = ''

            title = item.xpath('./a/div[@class="txt"]/p/text()').extract()
            if title:
                title = title[0]
                design['title'] = title
            else:
                design['title'] = ''

            design['tags'] = []

            detailUrl = item.xpath('./a/@href').extract()
            if detailUrl:
                detailUrl = self.baseUrl + detailUrl[0]
                yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})


    def parseDetail(self,response):
        design = response.meta['design']
        imgs = []
        yield design
