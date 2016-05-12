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

        nextPage = response.xpath('//div[@id="page"]/ul/li[@class="next"]/a/@href').extract()
        if nextPage:
            nextPage = self.baseUrl + nextPage[0]
            yield scrapy.Request(nextPage,callback=self.parse)

    def parseDetail(self,response):
        design = response.meta['design']
        imgs = []

        img = response.xpath('//div[@id="slider"]/p/img/@src').extract()
        if img:
            img = img[0]
            imgs.append(img)

        design['img'] = imgs

        yield design
