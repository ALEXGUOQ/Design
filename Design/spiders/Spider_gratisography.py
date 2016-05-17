#-*- coding:utf-8 -*-
import scrapy
from Design.items import DesignItem


class Spider_gratisography(scrapy.Spider):
	name = 'gratisography'

	start_urls = [
		'http://www.gratisography.com/',
	]

	def parse(self, response):
		for item in response.xpath('//section[@id="container"]/ul/li'):
			design = DesignItem()

			icon = item.xpath('./a/@href').extract()
			if icon:
				icon = icon[0]
				icon = icon.split('?')[0]
				design['icon'] = icon

				design['title'] = ''
				design['img'] = []

				design['tags'] = ''
				yield design

