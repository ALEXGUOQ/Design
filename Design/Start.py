#-*- coding:utf-8 -*-
from scrapy import cmdline

names = ['fondCool','share','works','zcool','gratisography']
for item in names:
	cmd = 'scrapy crawl %s' % item
	cmdline.execute(cmd.split())