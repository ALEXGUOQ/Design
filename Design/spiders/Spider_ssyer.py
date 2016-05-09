#-*- coding:utf-8 -*-
import scrapy

from Design.items import DesignItem

# 别样
class Spider_ssyer(scrapy.Spider):
	name = 'ssyer'

	start_urls = [
		'http://www.ssyer.com',
	]

	def parse(self, response):
		for item in response.xpath('//div[@id="waterfall"]/div[@class="box"]/div[@class="pic"]/img'):
			img = item.xpath('./@src').extract()
			if img:
				design = DesignItem()
				design['title'] = ''

				img = img[0]
				img = self.start_urls[0] + img
				design['icon'] = img

				design['img'] = []
				design['tags'] = []
				yield design

		nextPage = response.xpath('//div[@class="badoo"]/a[@id="pageNext"]/@href').extract()
		if nextPage:
			nextPage = nextPage[0]
			url = self.start_urls[0] + nextPage
			yield scrapy.Request(url,callback=self.parse)