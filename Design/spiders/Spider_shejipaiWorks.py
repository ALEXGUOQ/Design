#-*- coding:utf-8 -*-
import scrapy

from Design.items import DesignItem

# 设计派 ->创意灵感
class Spider_shejipaiWorks(scrapy.Spider):
    name = 'shejipaiWorks'

    start_urls = [
        'http://www.shejipai.cn/category/master-works',
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

            detailUrl = item.xpath(
                './article/div[@class="post-body"]/div[@class="post-media-body"]/div[@class="figure-link-w"]/a/@href').extract()
            if detailUrl:
                detailUrl = detailUrl[0]
                yield scrapy.Request(detailUrl, callback=self.parseDetail, meta={'design': design})


        nextPage = response.xpath('//div[@class="pagination-w hide-for-isotope"]/div[@class="wp-pagenavi"]/a[@class="nextpostslink"]/@href').extract()
        if nextPage:
            nextPage = nextPage[0]
            yield scrapy.Request(nextPage,callback=self.parse)

    def parseDetail(self, response):
        design = response.meta['design']

        imgs = []
        for item in response.xpath('//img[contains(@class,"aligncenter size-full")]'):
            img = item.xpath('./@src').extract()
            if img:
                img = img[0]
                imgs.append(img)
        design['img'] = imgs
        yield design