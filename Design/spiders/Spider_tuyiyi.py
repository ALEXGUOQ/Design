#-*- coding:utf-8 -*-
import scrapy

from Design.items import DesignItem

class Spider_tuyiyi(scrapy.Spider):
	name = 'tuyiyi'

	start_urls = [
		'http://www.tuyiyi.com/show-33',
	]

	baseUrl = 'http://www.tuyiyi.com'

	def parse(self, response):
		for item in response.xpath('//div[@id="list"]/ul/li'):
			design = DesignItem()

			icon = item.xpath('./div[@class="moquu_picc"]/a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon
			else:
				design['icon'] = ''

			title = item.xpath('./div[@class="moquu_zpbt"]/text()').extract()
			if title:
				title = title[0]
				design['title'] = title
			else:
				design['title'] = ''

			design['tags'] = []

			detailUrl = item.xpath('./div[@class="moquu_picc"]/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				detailUrl = self.baseUrl + detailUrl
				yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		# nextPage = response.xpath('//div[@id="page"]/ul/li[@class="next"]/a/@href').extract()
		# if nextPage:
		# 	nextPage = nextPage[0]
		# 	nextPage = self.baseUrl + nextPage
		# 	yield scrapy.Request(nextPage,callback=self.parse)

		for i in xrange(1,1126):
			url = 'http://www.tuyiyi.com/show-33-31522-%d' % i
			yield scrapy.Request(url, callback=self.parse)

	def parseDetail(self,response):
		design = response.meta['design']

		imgs = []

		for item in response.xpath('//div[@id="slider"]/p/img'):
			img = item.xpath('./@src').extract()
			if img:
				img = img[0]
				img = self.baseUrl + img
				imgs.append(img)

		design['img'] = imgs
		yield design
