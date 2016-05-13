# -*- coding: utf-8 -*-
import scrapy
from Design.items import DesignItem

# 莫贝网 -> 灵感
class Spider_mobileuiInspiration(scrapy.Spider):
	name = 'inspiration'

	start_urls = [
		'http://un.mobileui.cn/inspiration/1',
	]

	baseUrl = 'http://un.mobileui.cn/'

	def parse(self, response):
		for menu in response.xpath('//ul[@id="thread_types"]/li'):
			tag = menu.xpath('./a/text()').extract()
			if tag:
				tag = tag[0]

			typeUrl = menu.xpath('./a/@href').extract()
			if typeUrl:
				typeUrl = typeUrl[0]
				if typeUrl != self.start_urls[0]:
					yield scrapy.Request(typeUrl,callback=self.parseItem,meta={'tag':tag})

	def parseItem(self,response):
		tag = response.meta['tag']

		for item in response.xpath('//ul[@id="waterfall"]/li'):
			design = DesignItem()

			icon = item.xpath('./div[@class="c cl"]/a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon
			else:
				design['icon'] = ''

			title = item.xpath('./h3/a/text()').extract()
			if title:
				title = title[0]
				design['title'] = title
			else:
				design['title'] = ''

			tags = []
			tags.append(tag)
			design['tags'] = tags

			detailUrl = item.xpath('./h3/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		nextPage = response.xpath('//span[@id="fd_page_bottom"]/div[@class="pg cl"]/div[@class="y"]/a[@class="nxt"]/@href').extract()
		if nextPage:
			nextPage = nextPage[0]
			print nextPage
			yield scrapy.Request(nextPage,callback=self.parseItem,meta={'tag':tag})

	def parseDetail(self,response):
		design = response.meta['design']

		imgs = []
		for item in response.xpath('//td[@class="t_f"]/ignore_js_op'):
			img = item.xpath('./img/@src').extract()
			if img:
				img = self.baseUrl + img[0]
				imgs.append(img)

		design['img'] = imgs
		yield design


