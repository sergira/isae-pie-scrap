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
import numpy as np

class NewsSpider(scrapy.Spider):


	name = 'lm'
	allowed_domains = ['https://news.lockheedmartin.com']

	
	start_urls = [('https://news.lockheedmartin.com/news-releases?advanced=1&keywords=rocket&start=2008-01-01&end=2018-02-06&have_asset_types=1&l=100&0=%d' % (i*100)) for i in range(0,8)]

	def parse(self, response):
	# iterate entries
		for entry in response.css('li.wd_item'):
	
			#retrieve info for our current post
			item = ScrapyItem()
		
					
			item['source'] = 'lockheed_martin'
			temp_string = entry.css('div.wd_date::text').extract_first()
			item['brief'] = entry.css('div').css('p::text').extract_first()
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('div').css('a::text').extract_first()
			

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


