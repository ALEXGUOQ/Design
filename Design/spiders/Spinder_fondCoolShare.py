#-*- coding:utf-8 -*-

import scrapy
import re
from Design.items import DesignItem

# 方酷 -> 设计分享
class Spinder_fondCoolShare(scrapy.Spider):
	name = 'share'

	start_urls =[
		'http://www.fondcool.com/share.html',
	]

	# http://www.fondcool.com/share.html?&p=225#post_list
	def parse(self, response):
		lastPage = response.xpath('//ul[@id="pagefen_ul"]/a/@href').extract()
		if lastPage:
			lastPage = lastPage[0]
			mode = re.compile(r'\d+')
			num = mode.findall(lastPage.lstrip().strip().rstrip(','))
			pageCount = int(num[0])

			for i in xrange(1,pageCount):
				url = 'http://www.fondcool.com/share.html?&p=%d#post_list' % i
				yield scrapy.Request(url,callback = self.parsePages)

	def parsePages(self,response):
		for item in response.xpath('//div[@class="hot fl"]/ul[@class="hot_list_ul"]/li[@class="hot_list_li clearfix wraps"]'):
			design = DesignItem()

			title = item.xpath('./div[@class="text fl"]/h4/a/@title').extract()
			if title:
				title = title[0]
				design['title'] = title

			tags = []
			for tag in item.xpath('./div[@class="text fl"]/p[@class="tags"]/a'):
				str = tag.xpath('./text()').extract()
				if str:
					tags.append(str[0])
			design['tags'] = tags

			detailUrl = item.xpath('./div[@class="text fl"]/h4/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]

			icon = item.xpath('./div[@class="img fl"]/a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon

			yield scrapy.Request(detailUrl,callback=self.parseDetails,meta={'design':design})

	def parseDetails(self,response):
		design = response.meta['design']
		imgs = []

		for item in response.xpath('//div[@id="article_img_list_wrap"]/a'):
			img = item.xpath('./@href').extract()
			if img:
				img = img[0]
				imgs.append(img)

		design['img'] = imgs
		return design

