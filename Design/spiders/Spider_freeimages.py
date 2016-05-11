#-*- coding:utf-8 -*-
import scrapy

class Spider_freeimages(scrapy.Spider):
	name = 'freeimages'

	start_urls = [
		'http://cn.freeimages.com/image'
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
						yield scrapy.Request(url,callback=self.parseItem,meta={'tag':tag})
			break

	def parseItem(self,response):
		tag = response.meta['tag']

		for item in response.xpath('ul[@class="thumb-premium fn-clear"]/li'):
			icon = item.xpath('./a/span/span/img/@src').extract()
			if icon:
				icon = icon[0]

				detailUrl = item.xpath('./a/@href').extract()
				if detailUrl:
					detailUrl = detailUrl[0]

					
