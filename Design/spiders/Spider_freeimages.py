#-*- coding:utf-8 -*-
import scrapy
from Design.items import DesignItem

class Spider_freeimages(scrapy.Spider):
    name = 'freeimages'

    start_urls = [
        'http://cn.freeimages.com/image',
    ]

    baseUrl = 'http://cn.freeimages.com'

    def parse(self, response):
        for category in response.xpath('//ul[@class="category-group"]/li'):
            imageType = category.xpath('./a/@href').extract()
            if imageType:
                imageType = imageType[0]
                if imageType != '/image':
                    url = self.baseUrl + imageType

                    tag = category.xpath('./a/text()').extract()
                    if tag:
                        tag = tag[0]
                        print tag
                        yield scrapy.Request(url, callback=self.parseItem, meta={'tag': tag})

    def parseItem(self, response):
        tag = response.meta['tag']

        for item in response.xpath('//ul[@class="thumb-premium fn-clear"]/li'):
            design = DesignItem()

            icon = item.xpath('./a/span/span/img/@src').extract()
            if icon:
                icon = icon[0]
                design['icon'] = icon
            else:
                design['icon'] = ''

            design['title'] = ''
            design['img'] = []
            design['tags'] = tag
            yield design

        for page in response.xpath('//div[@class="pagination fn-right"]/a'):
            nextPage = page.xpath('./text()').extract()
            if nextPage:
                nextPage = nextPage[0]

                if nextPage == 'Next'.decode('utf-8'):
                    url = page.xpath('./@href').extract()
                    if url:
                        url = url[0]
                        yield scrapy.Request(url,callback=self.parseItem,meta={'tag': tag})

        # for item in response.xpath('//ul[@class="thumb-group thumb-group160x160 thumb-group-fixed thumb-group-line fn-clear"]/li'):
        #     image = DesignItem()
        #
        #     title = item.xpath('./a/text()').extract()
        #     if title:
        #         title = title[0]
        #         image['title'] = title
        #     else:
        #         image['title'] = ''
        #
        #
        #     icon = item.xpath('./a/span[@class="thumb-img offset-preview"]/img/@src').extract()
        #     if icon:
        #         icon = icon[0]
        #         image['icon'] = icon
        #     else:
        #         image['icon'] = ''
        #
        #     image['tags'] = ''
        #
        #     detailUrl = item.xpath('./a/@href').extract()
        #     if detailUrl:
        #         detailUrl = self.baseUrl + detailUrl[0]
        #         yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':image})

        #     for page in response.xpath('//div[@class="pagination fn-right"]/a'):
        #         nextPage = page.xpath('./text()').extract()
        #         if nextPage:
        #             nextPage = nextPage[0]
        #
        #             if nextPage == 'Next'.decode('utf-8'):
        #                 url = page.xpath('./@href').extract()
        #                 if url:
        #                     url = url[0]
        #                     yield scrapy.Request(url, callback=self.parseItem, meta={'tag': tag})

    def parseDetail(self,response):
        design = response.meta['design']
        img = response.xpath('//div[@class="img-preview-inner"]/a[@class="preview cboxElement"]/img/@src')
        if img:
            img = img[0]
            design['img'] = img
            yield design