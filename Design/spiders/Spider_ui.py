#-*- coding:utf-8 -*-

import scrapy

# ui 作品
from Design.items import DesignItem


class Spider_ui(scrapy.Spider):
    name = 'ui'

    start_urls = [
        'http://www.ui.cn/list.html?tag=0&r=all&subcatid=1&catid=0',
    ]
    baseUrl = 'http://www.ui.cn'

    def parse(self, response):
        for menuItem in response.xpath('//div[@id="works-nav"]/div[@class="works-tit cl"]/div[@class="screen"]/div[3]/ul[@class="drop-menu"]/li'):
            menuType = menuItem.xpath('./a/text()').extract()
            if menuType:
                menuType = menuType[0]

            menuUrl = menuItem.xpath('./a/@href').extract()
            if menuUrl:
                if menuUrl:
                    if menuUrl[0] != '/list.html?tag=0&r=all&subcatid=0&catid=0':
                        url = self.baseUrl + menuUrl[0]
                        yield scrapy.Request(url,callback=self.parseItem,meta={'tag':menuType})

    def parseItem(self,response):
        tag = response.meta['tag']

        for item in response.xpath('//div[@class="wpn"]/ul[@class="post post-works mtv cl"]/li'):
            design = DesignItem()
            icon = item.xpath('./div[@class="cover pos"]/a/img/@src').extract()
            if icon:
                icon = icon[0]
                design['icon'] = icon
            else:
                design['icon'] = ''

            title = item.xpath('./div[@class="info"]/h4/text()').extract()
            if title:
                title = title[0]
                design['title'] = title.strip()
            else:
                design['title'] = ''

            tags = []
            tags.append(tag)
            design['tags'] = tags

            detailUrl = item.xpath('./div[@class="cover pos"]/a/@href').extract()
            if detailUrl:
                detailUrl =self.baseUrl + detailUrl[0]
                yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

        nextPage = response.xpath('//div[@class="min_page mbw"]/ul[@class="cl"]/li[@class="next"]/a/@href').extract()
        if nextPage:
            nextPage = self.baseUrl + '/list.html' + nextPage[0]
            yield scrapy.Request(nextPage,callback=self.parseItem,meta={'tag':tag})

    def parseDetail(self,response):
        design = response.meta['design']

        imgs = []

        img = response.xpath('//*[@id="p-content"]/a/img/@src').extract()
        if img:
            imgs.append(img[0])

        design['img'] = imgs
        yield design
