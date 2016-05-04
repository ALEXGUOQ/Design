#-*- coding:utf-8 -*-

import scrapy
import re
from Design.items import DesignItem

# 方酷 -> 首页
class Spinder_fondCool(scrapy.Spider):

	name = 'fondCool'

	start_urls = {
		'http://www.fondcool.com/index.html',
	}

	def parse(self, response):
		pages = response.xpath('//ul[@id="pagefen_ul"]')
		pageNum = pages.xpath('./a/text()').extract()
		if pageNum:
			pageNum = pageNum[0]
			if pageNum == 'LAST':
				lastPage = pages.xpath('./a/@href').extract()
				if lastPage:
					lastPage = lastPage[0]
					mode = re.compile(r'\d+')
					num = mode.findall(lastPage.lstrip().strip().rstrip(','))
					pageCount = int(num[0])

					for i in xrange(1,pageCount):
						url = 'http://www.fondcool.com/index.html?&p=%d#post_list' % i
						yield scrapy.Request(url,callback=self.parseEachPage)

	def parseEachPage(self,response):
		for item in response.xpath('//ul[@class="hot_list_ul"]/li[@class="hot_list_li clearfix wraps"]'):
			design = DesignItem()

			title = item.xpath('./div[@class="text fl"]/h4/a/@title').extract()
			if title:
				title = title[0]
				design['title'] = title

			detailUrl = item.xpath('./div[@class="img fl"]/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]

			icon = item.xpath('./div[@class="img fl"]/a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon

			yield scrapy.Request(detailUrl,callback=self.openDetail,meta={'design':design})

	def openDetail(self,response):
		design = response.meta['design']
		imgs = []
		img = response.xpath('//div[@class="detail truncate "]/div[@class="inner_text align_center ml_20"]/a/@href').extract()
		if img:
			img = img[0]
			imgs.append(img)

		tags = []
		for item in response.xpath('//p[@class="tags "]/a'):
			tag = item.xpath('./text()').extract()
			if tag:
				tag = tag[0]
				tags.append(tag)

		design['img'] = imgs
		design['tags'] = tags
		return design





