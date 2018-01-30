# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import datetime
import scrapy
from ScrapyProject.items import ScrapyItem

class NewsSpider(scrapy.Spider):


	name = 'roscosmos'
	allowed_domains = ['http://en.roscosmos.ru']

	
	start_urls = [('http://en.roscosmos.ru/102/2017%s/' %i[0]) for i in zip(["01","02","03","04","05","06","07","08","09","10","11","12"])]

	def parse(self, response):
	# iterate entries
		for entry in response.css('div.newslist'):
	
			#retrieve info for our current post
			item = ScrapyItem()
		
					
			item['source'] = 'roscosmos'
			item['date'] = entry.css('div.date::text').extract_first()
			item['brief'] = 'none'
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('div').css('a.name::text').extract_first()
			

			# check time
			now = datetime.datetime.now()
			item['tstamp'] = now
		

		   # item['date'] = entry.css('time::text').extract_first()
		   # item['brief'] = entry.css('p.post-excerpt::text').extract_first()
		   # item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
		   # item['title'] = entry.css('h2').css('a::text').extract_first()

			yield item


