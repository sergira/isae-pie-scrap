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

	name = 'wired_deep2_1'
	allowed_domains = ['wired.com']

	start_urls = ['https://www.wired.com/search/?page=1&q=rocket&size=10&sort=publishDate_tdt%20desc&types%5B0%5D=article']
	url_list = np.empty((1,100), dtype=object)
	temp = False
	j = 0
		

	def parse(self, response):
		
		item = ScrapyItem()

		i = 0
		if NewsSpider.temp==False: 
			if NewsSpider.j ==0:
				for entry in response.css('div').css('li.archive-item-component'):

					
					np.put(NewsSpider.url_list, [i], entry.css('a::attr(href)').extract_first())
					#url_list = np.append(entry.css('a::attr(href)').extract_first())
					url_temp = entry.css('a::attr(href)').extract_first()		
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
	
					i = i+1

					yield item

			next_page = response.urljoin(NewsSpider.url_list.item(NewsSpider.j))
			NewsSpider.temp = True
			NewsSpider.j = NewsSpider.j+1
			yield scrapy.Request(next_page, callback=self.parse)
		
		else:
			item['article'] = response.css('article').css('div').css('p::text').extract()
			yield item
			previous_page = 'https://www.wired.com/search/?page=1&q=rocket&size=1&sort=publishDate_tdt%20desc&types%5B0%5D=article'
			NewsSpider.temp = False
			yield scrapy.Request(previous_page, callback=self.parse)

		
		

