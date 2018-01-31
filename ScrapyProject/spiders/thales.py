# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import datetime
import scrapy
from ScrapyProject.items import ScrapyItem

class ThalesSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	name = 'thales'


	allowed_domains = ['https://www.thalesgroup.com']

	start_urls = [('https://www.thalesgroup.com/fr/search-everything/all/propulsion?page=%d' %i ) for i in range(0,30)]

	def parse(self, response):
        # iterate entries


		for entry in response.css('div.big__list__item__info'):

            #retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'thales'
			item['date'] = 'NotAvalaible'
			item['brief'] = entry.css('div.field__item even::text').extract_first()
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('a::text').extract_first()

			# check time
			now = datetime.datetime.now()
			item['tstamp'] = now

			print(item)

			yield item
