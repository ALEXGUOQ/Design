#-*- coding:utf-8 -*-
import scrapy

from Design.items import DesignItem

# 图翼网 -> 作品 -> 电商
class Spider_tuyiyi_h5(scrapy.Spider):
	name = 'business'

	start_urls = [
		'http://www.tuyiyi.com/t-157-1.html',
	]
	baseUrl = 'http://www.tuyiyi.com'

	def parse(self, response):
		for item in response.xpath('//div[@id="list"]/div[@class="moquu_free"]/ul/li'):
			design = DesignItem()
			icon = item.xpath('./a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon
			else:
				design['icon'] = ''

			title = item.xpath('./a/div[@class="txt"]/p/b/text()').extract()
			if title:
				title = title[0]
				design['title'] = title
			else:
				design['title'] = ''

			tags = []
			tags.append('business')
			design['tags'] = tags

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

		for item in response.xpath('//div[@id="slider"]/p'):
			for eachImg in item.xpath('./img'):
				img = eachImg.xpath('./@src').extract()
				if img:
					img = img[0]
					imgs.append(img)

		design['img'] = imgs
		yield design