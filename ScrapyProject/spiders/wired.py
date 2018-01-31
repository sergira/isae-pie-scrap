# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import timestring
import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import pytz
import dateutil.parser

class NewsSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	#name = item_id.source[0]

	name = 'wired'
	allowed_domains = ['https://www.wired.com']

	#start_urls = [('https://www.wired.com/search/?q=rocket' % i) for i in range(1,50)]
	start_urls = ['https://www.wired.com/search/?page=1&q=rocket&size=10&sort=publishDate_tdt%20desc&types%5B0%5D=article']
	#start_urls = ['https://www.wired.com/search/?q=rocket']

	def parse(self, response):
	# iterate entries
		for entry in response.css('div').css('li.archive-item-component'):
	
			#retrieve info for our current post
			item = ScrapyItem()
		
		# p.post-excerpt   class de type p = post-excerpt			
			item['source'] = 'wired'
			temp_string = entry.css('time::text').extract_first()
			item['brief'] = entry.css('a').css('p.archive-item-component__desc::text').extract_first()
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('a').css('h2::text').extract_first()


			# check time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
		

		   # item['date'] = entry.css('time::text').extract_first()
		   # item['brief'] = entry.css('p.post-excerpt::text').extract_first()
		   # item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
		   # item['title'] = entry.css('h2').css('a::text').extract_first()

			yield item


