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

	name = 'wired_deep2_2Meta'
	allowed_domains = ['wired.com']

	start_urls = ['https://www.wired.com/search/?page=1&q=rocket&size=10&sort=publishDate_tdt%20desc&types%5B0%5D=article']
	

	def parse(self, response):
		
		
		item = ScrapyItem()
		
		for entry in response.css('div').css('li.archive-item-component'):

			url_temp = entry.css('a::attr(href)').extract_first()	
			next_page = response.urljoin(url_temp)		

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
		
			# request to article page
			request = scrapy.Request(next_page, callback=self.parse_article)
			request.meta['item'] = item

			yield request
			
			

	def parse_article(self, response):
			
		
		string = response.css('article').css('div').css('p::text').extract()

		item = response.meta['item']
		item['article'] = string
		return item

		
		

