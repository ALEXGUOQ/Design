#-*- coding:utf-8 -*-

import scrapy
from Design.items import DesignItem

class Spider_lifeofpix(scrapy.Spider):
	name = 'lifeofpix'

	start_urls = [
		'http://www.lifeofpix.com/',
	]

	def parse(self, response):
		for item in response.xpath('//section[@id="main"]/article[@class="article portfolio-item big"]'):
			design = DesignItem()

			design['title'] = ''

			img = item.xpath('./div[@class="wrapper"]/div[@class="portfolio-piece"]/a/span/img/@src').extract()
			if img:
				img = img[0]
				design['icon'] = img

			design['img'] = ''
			design['tags'] = ''
			yield design

		nextPage = response.xpath('//div[@class="pagination"]/a[@class="next page-numbers"]/@href')
		if nextPage:
			nextPage = nextPage[0]
			yield scrapy.Request(nextPage,callback=self.parse)