#-*- coding:utf-8 -*-

import scrapy

from Design.items import DesignItem

# 创意派 -> 素材
class Spider_shejipai(scrapy.Spider):
    name = 'shejipai'

    start_urls = [
        'http://www.shejipai.cn/category/materials-and-download',
    ]

    def parse(self, response):
        for item in response.xpath('//div[@class="item-isotope"]'):
            design = DesignItem()

            icon = item.xpath('./article/div[@class="post-body"]/div[@class="post-media-body"]/div[@class="figure-link-w"]/a/figure/img/@src').extract()
            if icon:
                icon = icon[0]
                design['icon'] = icon
            else:
                design['icon'] = ''

            tags = []
            for tagItem in item.xpath('./article/div[@class="post-body"]/div[@class="post-content-body"]/ul[@class="post-categories"]/li'):
               tag = tagItem.xpath('./a/text()').extract()
               if tag:
                   tag = tag[0]
                   tags.append(tag)
            design['tags'] = tags

            title = item.xpath('./article/div[@class="post-body"]/div[@class="post-content-body"]/h4[@class="post-title entry-title"]/a/text()').extract()
            if title:
                title = title[0]
                design['title'] = title
            else:
                design['title'] = ''

            detailUrl = item.xpath('./article/div[@class="post-body"]/div[@class="post-media-body"]/div[@class="figure-link-w"]/a/@href').extract()
            if detailUrl:
                detailUrl = detailUrl[0]
                yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

        nextpage = response.xpath('//div[@class="wp-pagenavi"]/a[@class="nextpostslink"]/@href').extract()
        if nextpage:
            nextpage = nextpage[0]
            yield scrapy.Request(nextpage,callback=self.parse)

    def parseDetail(self,response):
        design = response.meta['design']

        imgs = []
        for item in response.xpath('//img[contains(@class,"alignnone size-medium")]'):
            img = item.xpath('./@src').extract()
            if img:
                img = img[0]
                imgs.append(img)
        design['img'] = imgs
        yield design