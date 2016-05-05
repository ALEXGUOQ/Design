#-*- coding:utf-8 -*-

import scrapy
import re
from Design.items import DesignItem

# 站酷
class Spider_zcool(scrapy.Spider):
	name = 'zcool'

	start_urls = [
		'http://www.zcool.com.cn/works/0!0!null!0!0!0!1!1!!!/',
	]

	baseUrl = 'http://www.zcool.com.cn'

	def parse(self, response):
		for item in response.xpath('//div[@class="camWholeBox"]/ul[@class="layout camWholeBoxUl"]/li'):
			design = DesignItem()

			title = item.xpath('./a/@title').extract()
			if title:
				title = title[0]
				design['title'] = title

			detailUrl = item.xpath('./a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]

			icon = item.xpath('./a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon

			tags = []
			for tag in item.xpath('./div[@class="camLiCon"]/div[@class="camLiDes"]/a'):
				str = tag.xpath('./text()').extract()
				if str:
					tags.append(str[0])
			design['tags'] = tags
			yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		nextPage = response.xpath('//div[@class="bigPage pt20 pb30 vm center"]/a[@class="pageNext"]/@href').extract()
		if nextPage:
			url = self.baseUrl + nextPage[0]
			yield scrapy.Request(url,callback=self.parse)

	def parseDetail(self,response):
		design = response.meta['design']

		imgs = []

		for item in response.xpath('//img[contains(@class,"mb10")]/@src'):
			image = item.extract()
			if image:
				imgs.append(image)

		design['img'] = imgs
		return design

	# def getImg(self,html):
	# 	reg = r'img .*? class="mb10"'
	# 	imgre = re.compile(reg)
	# 	imglist = re.findall(imgre, html)
	# 	print imglist
	# 	return imglist