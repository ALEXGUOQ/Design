#-*- coding:utf-8 -*-

import scrapy

# 站酷搜素材
from Design.items import DesignItem


class Spider_zcoolSucai(scrapy.Spider):
	name = 'sucai'

	start_urls = [
		'http://sucai.zcool.com.cn/view.do?category=0&sort=',
	]
	baseUrl = 'http://sucai.zcool.com.cn/'
	maxPage = 100

	def parse(self, response):
		for item in response.xpath('//ul[@class="clearfix imglist mt20"]/li'):
			design = DesignItem()

			title = item.xpath('./div[@class="textbox"]/a/text()').extract()
			if title:
				title = title[0]
				design['title'] = title

			icon = item.xpath('./div[@class="picbox"]/a[3]/span[@class="img"]/img/@data-original').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon

			tag = item.xpath('./div[@class="picbox"]/a[3]/span[@class="tag"]/text()').extract()
			if tag:
				tag = tag[0]
				tag = tag.replace(',','')
				tag = tag.strip()
				tag = tag.replace(',', '')
				design['tags'] = tag

			detailUrl = item.xpath('./div[@class="textbox"]/a/@href').extract()
			if detailUrl:
				detailUrl = self.baseUrl + detailUrl[0]
				yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		self.maxPage += 1
		if self.maxPage < 100:
			url = 'http://sucai.zcool.com.cn/view.do?category=0&sort=&oriCate=0&guid=F9341B58-EF50-5F9E-318D-F6387F1FB80C&start=%d' % self.maxPage
			yield scrapy.Request(url,callback=self.parse)

	def parseDetail(self,response):
		design = response.meta['design']
		imgs = []

		for item in response.xpath('//div[@class="detailLeft"]/table/tr/td'):
			image = item.xpath('./img/@data-original').extract()
			if image:
				image = image[0]
				imgs.append(image)
				print image
		design['img'] = imgs
		return design
