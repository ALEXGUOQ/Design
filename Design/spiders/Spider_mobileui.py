#-*- coding:utf-8 -*-
import scrapy
from Design.items import DesignItem

# 莫贝网 -> ui库
class Spider_mobileui(scrapy.Spider):
	name = 'mobileui'

	start_urls = [
		'http://www.mobileui.cn/uiku/?action=ajax_post&pag=1',
	]

	index = 1
	baseUrl = 'http://www.mobileui.cn/uiku/?action=ajax_post&pag=%d'

	def parse(self, response):
		for item in response.xpath('//div[@class="post-home"]'):
			design = DesignItem()

			icon = item.xpath('./div[@class="post-thumbnail"]/a[@class="inimg"]/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon
			else:
				design['icon'] = ''

			title = item.xpath('./div[@class="post-thumbnail"]/h3[@class="celltip"]/a/text()').extract()
			if title:
				title = title[0]
				design['title'] = title
			else:
				design['title'] = ''

			design['tags'] = []

			detailUrl = item.xpath('./div[@class="post-thumbnail"]/a[@class="inimg"]/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		self.index += 1
		yield scrapy.Request(self.baseUrl % self.index,callback=self.parse)

	def parseDetail(self,response):
		design = response.meta['design']
		imgs = []
		img = response.xpath('//div[@class="post-content"]/p/a/img/@src').extract()
		if img:
			img = img[0]
			imgs.append(img)

		design['img'] = imgs
		yield design
