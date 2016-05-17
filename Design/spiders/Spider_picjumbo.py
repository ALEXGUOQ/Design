#-*- coding:utf-8 -*-
import scrapy
from Design.items import IconItem

class Spider_picjumbo(scrapy.Spider):
	name = 'picjumbo'

	start_urls = [
		'https://picjumbo.com/',
	]

	def parse(self, response):
		for menu in response.xpath('//li[@id="menu-item-3475"]/ul[@class="sub-menu"]/li'):
			url = menu.xpath('./a/@href').extract()
			if url:
				url = url[0]

				menuType = menu.xpath('./a/text()').extract()
				if menuType:
					menuType = menuType[0]
					yield scrapy.Request(url,callback=self.dealParse,meta={'menuType':menuType})

	def dealParse(self,response):
		try:
			menuType = response.meta['menuType']

			for item in response.xpath('//div[@class="content"]/div[@class="item_wrap"]/div[@class="single_img"]/a/img'):
				design = IconItem()

				img = item.xpath('./@src').extract()
				if img:
					img = img[0]
					img = 'http:' + img
					design['icon'] = img

					if menuType:
						tags = []
						tags.append(menuType)
						design['tags'] = tags
					else:
						design['tags'] = ''
					yield design

			nextPage = response.xpath('//div[@class="navigation"]/div[@class="next"]/a/@href').extract()
			if nextPage:
				nextPage = nextPage[0]
				yield scrapy.Request(nextPage,callback=self.dealParse,meta={'menuType':menuType})
		except:
			print 'exception'