# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import datetime
import scrapy
from ScrapyProject.items import ScrapyItem
import numpy as np

class NewsSpider(scrapy.Spider):

	name = 'wired_deep2_2Meta'
	allowed_domains = ['wired.com']

	start_urls = ['https://www.wired.com/search/?page=1&q=rocket&size=10&sort=publishDate_tdt%20desc&types%5B0%5D=article']
	url_list = np.empty((1,100), dtype=object)
	temp = False
	j = 0
	
	
		

	def parse(self, response):
		
		
		item = ScrapyItem()
		
		for entry in response.css('div').css('li.archive-item-component'):

			url_temp = entry.css('a::attr(href)').extract_first()	
			next_page = response.urljoin(url_temp)		

			item['url'] = url_temp	
			
			request = scrapy.Request(next_page, callback=self.parse_article)
			request.meta['item'] = item

			yield request
			
			
			

		


	def parse_article(self, response):
			
		
		string = response.css('article').css('div').css('p::text').extract()

		item = response.meta['item']
		item['article'] = string
		return item

		
		

