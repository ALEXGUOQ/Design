# -*- coding:utf-8 -*-
import scrapy

from Design.items import DesignItem

# 图翼网 -> 素材
class Spider_tuyiyiIcon(scrapy.Spider):
	name = 'tuyiyiIcon'

	start_urls = [
		'http://www.tuyiyi.com/show-73',
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
				yield scrapy.Request(href, callback=self.parseItem, meta={'tag': tag})

	def parseItem(self, response):
		tag = response.meta['tag']

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

			tags = []
			tags.append(tag)
			design['tags'] = tags

			detailUrl = item.xpath('./a/@href').extract()
			if detailUrl:
				detailUrl = self.baseUrl + detailUrl[0]
				yield scrapy.Request(detailUrl, callback=self.parseDetail, meta={'design': design})

		nextPage = response.xpath('//div[@id="page"]/ul/li[@class="next"]/a/@href').extract()
		if nextPage:
			nextPage = self.baseUrl + nextPage[0]
			yield scrapy.Request(nextPage, callback=self.parseItem,meta={'tag': tag})

	def parseDetail(self, response):
		design = response.meta['design']
		imgs = []

		img = response.xpath('//div[@id="slider"]/p/img/@src').extract()
		if img:
			img = img[0]
			imgs.append(img)

		design['img'] = imgs

		yield design
