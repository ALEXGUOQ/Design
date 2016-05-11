# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pymysql

'''
	格式化当前时间
'''
def getCurrentTime():
	# time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	return datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')

def dbHandle():
	conn = pymysql.connect(
		host='10.0.1.112',
		user='root',
		passwd='',
		db='design',
		charset='utf8',
		use_unicode= False
	)
	return conn

class DesignPipeline(object):

	def process_item(self, item, spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = "insert into design.image (title,icon,img,tags,create_time,modify_time) values (%s,%s,%s,%s,%s,%s)"

		images = ''
		if item['img']:
			for image in item['img']:
				images += image + ','

		tags = ''
		if item['tags']:
			for tag in item['tags']:
				tags += tag + ','

		icon = item['icon']

		selectSql = 'SELECT id FROM image WHERE icon = "%s"' % icon
		result = cursor.execute(selectSql)

		if result == 0:
			cursor.execute(sql, (item['title'], icon, images,tags,getCurrentTime(), getCurrentTime()))
			dbObject.commit()
		return item
