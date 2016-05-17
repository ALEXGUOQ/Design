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
		for menuItem in response.xpath('//div[@class="moquuso"]/li[@class="moquu_listscx"]'):
			tag = menuItem.xpath('./a/text()').extract()
			if tag:
				tag = tag[0]

			href = menuItem.xpath('./a/@href').extract()
			if href:
				href = href[0]
				href = self.baseUrl + href
				yield scrapy.Request(href,callback=self.parseItem,meta={'tag':tag})

	def parseItem(self,response):
		tag = response.meta['tag']
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

			tags = []
			tags.append(tag)
			design['tags'] = tags

			detailUrl = item.xpath('./div[@class="moquu_picc"]/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				detailUrl = self.baseUrl + detailUrl
				yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		nextPage = response.xpath('//div[@id="page"]/ul/li[@class="next"]/a/@href').extract()
		if nextPage:
			nextPage = nextPage[0]
			nextPage = self.baseUrl + nextPage
			yield scrapy.Request(nextPage, callback=self.parseItem,meta={'tag':tag})

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
