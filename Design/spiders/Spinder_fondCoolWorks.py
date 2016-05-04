#-*- coding:utf-8 -*-

import scrapy
import re
from Design.items import DesignItem

# 方酷 -> 原创作品
class Spinder_fondCoolWorks(scrapy.Spider):
	name = 'works'
	start_urls = [
		'http://www.fondcool.com/works.html',
	]

	def parse(self, response):
		lastPage = response.xpath('//ul[@id="pagefen_ul"]/a/@href').extract()
		if lastPage:
			lastPage = lastPage[0]
			mode = re.compile(r'\d+')
			num = mode.findall(lastPage.lstrip().strip().rstrip(','))
			pageCount = int(num[0])

			for i in xrange(1, pageCount):
				url = 'http://www.fondcool.com/works.html?&p=%d#post_list' % i
				yield scrapy.Request(url, callback=self.parsePages)

	def parsePages(self,response):
		for item in response.xpath('//ul[@class="works_box clearfix"]/li[@class="fl wraps truncate"]'):
			design = DesignItem()

			title = item.xpath('./h2/a/text()').extract()
			if title:
				title = title[0]
				design['title'] = title

			detailUrl = item.xpath('./h2/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]

			icon = item.xpath('./a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon

			design['img'] = []
			design['tags'] = []
			yield scrapy.Request(detailUrl,callback=self.parseDetails,meta={'design':design})

	def parseDetails(self,response):
		design = response.meta['design']

		for item in response.xpath('//div[@id="article_img_list_wrap"]/a'):
			img = item.xpath('./@href').extract()
			if img:
				design['img'].append(img[0])

		if len(design['tags']) == 0:
			for item in response.xpath('//p[@class="tags "]/a'):
				tag = item.xpath('./text()').extract()
				if tag:
					design['tags'].append(tag[0])

		# 下一页
		for page in response.xpath('//ul[@id="pagefen_ul"]/li'):
			nextPage = page.xpath('./a/text()').extract()
			if nextPage:
				nextPage = nextPage[0]
				if nextPage == 'NEXT':
					nextPageUrl = page.xpath('./a/@href').extract()
					if nextPageUrl:
						nextPageUrl = nextPageUrl[0]
						yield scrapy.Request(nextPageUrl, callback=self.parseDetails, meta={'design': design})
		yield design

