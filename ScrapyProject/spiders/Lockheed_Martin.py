# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import datetime
import scrapy
from ScrapyProject.items import ScrapyItem

class NewsSpider(scrapy.Spider):


	name = 'lm'
	allowed_domains = ['https://news.lockheedmartin.com']

	
	start_urls = [('https://news.lockheedmartin.com/news-releases?o=%d' %i*5) for i in range(20)]

	def parse(self, response):
	# iterate entries
		for entry in response.css('li.wd_item'):
	
			#retrieve info for our current post
			item = ScrapyItem()
		
					
			item['source'] = 'lockheed_martin'
			item['date'] = entry.css('div.wd_date::text').extract_first()
			item['brief'] = entry.css('div').css('p::text').extract_first()
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('div').css('a::text').extract_first()
			

			# check time
			now = datetime.datetime.now()
			item['tstamp'] = now
		

		   # item['date'] = entry.css('time::text').extract_first()
		   # item['brief'] = entry.css('p.post-excerpt::text').extract_first()
		   # item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
		   # item['title'] = entry.css('h2').css('a::text').extract_first()

			yield item


