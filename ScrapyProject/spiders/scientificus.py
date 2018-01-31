# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import datetime
import scrapy
from ScrapyProject.items import ScrapyItem

class NewsSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	name = 'scientificus'


	allowed_domains = ['scientificamerican.com']

	start_urls = ['https://www.scientificamerican.com/search/?q=propulsion&sortby=releasedate&source=&days=']

	def parse(self, response):
        # iterate entries
		for entry in response.css('div.listing-wide__inner'):
            
            #retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'scientificamerican'
			item['date'] = entry.css('div.t_meta::text').extract_first().split(' — ')[0]
			item['brief'] = entry.css('p::text').extract_first()
			item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
			item['title'] = entry.css('h2').css('a::text').extract_first()

			# check time
			now = datetime.datetime.now()
			item['tstamp'] = now

			yield item


