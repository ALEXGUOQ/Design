import scrapy

from Design.items import DesignItem


class Spider_uimaker(scrapy.Spider):
	name = 'uimaker'

	start_urls = [
		'http://www.uimaker.com/uimakerhtml/uidesign',
	]

	baseUrl = 'http://www.uimaker.com'

	def parse(self, response):
		for item in response.xpath('//dl[@class="imglist"]/dt/ul/li'):
			design = DesignItem()

			icon = item.xpath('./span/a/img/@src').extract()
			if icon:
				icon = icon[0]
				design['icon'] = icon

			title = item.xpath('./h2/a/text()').extract()
			if title:
				title = title[0]
				design['title'] = title

			detailUrl = item.xpath('./h2/a/@href').extract()
			if detailUrl:
				detailUrl = detailUrl[0]
				yield scrapy.Request(detailUrl,callback=self.parseDetail,meta={'design':design})

		nextPage = response.xpath('//div[@class="page"]/ul/li/a[@class="next"]/@href').extract()
		if nextPage:
			nextPage = nextPage[0]
			url = self.start_urls[0] +'/' + nextPage
			yield scrapy.Request(url,callback=self.parse)

	def parseDetail(self,response):
		design = response.meta['design']

		imgs = []
		for item in response.xpath('//div[@class="contentinfo"]/table/tr/td/p'):
			img = item.xpath('./img/@src').extract()
			if img:
				img = img[0]
				img = self.baseUrl + img
				imgs.append(img)

		design['img'] = imgs
		design['tags'] = []
		yield design