#-*- coding:utf-8 -*-
import scrapy

from Design.items import DesignItem

# 别样
class Spider_ssyer(scrapy.Spider):
	name = 'ssyer'

	start_urls = [
		'http://www.ssyer.com',
	]

	baseUrl = 'http://www.ssyer.com/index_'

	def parse(self, response):
		for menuItem in response.xpath('//div[@class="srt_text"]/li'):
			tag = menuItem.xpath('./a/text()').extract()
			if tag:
				tag = tag[0]

			url = menuItem.xpath('./a/@href').extract()
			if url:
				url = url[0]
				urls = url.split("'")
				left = urls[1].split("=")[0]
				right =urls[1].split("=")[1]

				menuUrl = self.baseUrl + left +'_' + right +'.html'
				yield scrapy.Request(menuUrl,callback=self.parseItem,meta={'tag':tag})

	def parseItem(self,response):
		tag = response.meta['tag']

		for item in response.xpath('//div[@id="waterfall"]/div[@class="box"]/div[@class="pic"]/img'):
			img = item.xpath('./@src').extract()
			if img:
				design = DesignItem()
				design['title'] = ''

				img = img[0]
				img = self.start_urls[0] + img
				design['icon'] = img

				design['img'] = []
				tags = []
				tags.append(tag)
				design['tags'] = tags
				yield design

		nextPage = response.xpath('//div[@class="badoo"]/a[@id="pageNext"]/@href').extract()
		if nextPage:
			nextPage = nextPage[0]
			url = self.start_urls[0] + nextPage
			yield scrapy.Request(url,callback=self.parseItem,meta={'tag':tag})