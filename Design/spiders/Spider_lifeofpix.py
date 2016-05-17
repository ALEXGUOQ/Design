#-*- coding:utf-8 -*-

import scrapy
from Design.items import Photography

# 高清摄影图
class Spider_lifeofpix(scrapy.Spider):
	name = 'lifeofpix'

	start_urls = [
		'http://www.lifeofpix.com/',
	]

	def parse(self, response):
		for item in response.xpath('//*[@id="main"]/article'):
			design = Photography()
			img = item.xpath('./div[@class="wrapper"]/div[@class="portfolio-piece"]/a/span[@class="post-thumb"]/img/@src').extract()
			if img:
				img = img[0]
				print img
				print
				design['icon'] = img
			yield design

		nextPage = response.xpath('//div[@class="pagination"]/a[@class="next page-numbers"]/@href').extract()
		if nextPage:
			nextPage = nextPage[0]
			yield scrapy.Request(nextPage,callback=self.parse)