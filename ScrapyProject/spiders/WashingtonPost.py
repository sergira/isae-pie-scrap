
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import datetime
import scrapy
from ScrapyProject.items import ScrapyItem

class WashingtonPostSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	name = 'WP'


	allowed_domains = ['https://www.washingtonpost.com/']

	start_urls = [('https://www.washingtonpost.com/newssearch/?query=space propulsion&utm_term=.2b4058aeca71&sort=Date&datefilter=All Since 2005&startat=%d&spellcheck#top' % (i*20)) for i in range (0,10)]
	
	def parse(self, response):
        #iterate entries
		
		for entry in response.css('div.pb-feed-headline.ng-scope'):
            
            #retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'WP'
			item['date'] = entry.css('span.pb-timestamp.ng-binding::text').extract_first()
			item['brief'] = entry.css('div.pb-feed-description.ng-binding').extract_first()
			item['url'] = entry.css('a.ng-binding::attr(href)').extract_first()
			item['title'] = entry.css('a.ng-binding::text').extract_first()

			# check time
			now = datetime.datetime.now()
			item['tstamp'] = now

			print(item)

			yield item


