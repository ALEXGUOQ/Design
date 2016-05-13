# -*- coding: utf-8 -*-
import scrapy

from Design.items import DesignItem


class Spider_mobileuiSite(scrapy.Spider):
	name = 'mobileuiSite'

	start_urls = [
		'http://site.mobileui.cn/',
	]

	def parse(self, response):
		for menu in response.xpath('//nav[@id="nav"]/li[contains(@class,"cat-item")]'):
			tag = menu.xpath('./a/text()').extract()
			if tag:
				tag = tag[0]

			menuUrl = menu.xpath('./a/@href').extract()
			if menuUrl:
				menuUrl = menuUrl[0]
				yield scrapy.Request(menuUrl,callback=self.parseItem,meta={'tag':tag})

	def parseItem(self,response):
		tag = response.meta['tag']
		for item in response.xpath('//article[@id="main"]/article/section'):
			design = DesignItem()

			title = item.xpath('./h1/a/text()').extract()
			if title:
				title = title[0]
				design['title'] = title
			else:
				design['title'] = ''

			icon = item.xpath('./article[@class="thumb"]/a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon
			else:
				design['icon'] = ''

			tags = []
			tags.append(tag)
			design['tags'] = tags

			detailUrl = item.xpath('./article[@class="thumb"]/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				print detailUrl
				yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		pages = response.xpath('//div[@id="wp_page_numbers"]/ul/li')
		length = len(pages)
		for index, link in enumerate(pages):
			if index == length -1:
				nextPage = link.xpath('./a/@href').extract()
				if nextPage:
					nextPage = nextPage[0]
					yield scrapy.Request(nextPage,callback=self.parseItem,meta={'tag':tag})

	def parseDetail(self,response):
		design = response.meta['design']

		imgs = []

		img = response.xpath('//div[@id="post_content"]/p/img/@src').extract()
		if img:
			imgs.append(img[0])

		for item in response.xpath('//aside[@id="random"]/ul/li'):
			img = item.xpath('./a/@href').extract()
			if img:
				imgs.append(img[0])

		design['img'] = imgs
		yield design

