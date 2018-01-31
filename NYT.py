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

class NYTimesSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	name = 'NYTimes'


	allowed_domains = ['https://www.nytimes.com']

	
	start_urls = [('https://query.nytimes.com/search/sitesearch/?action=click&contentCollection&region=TopBar&WT.nav=searchWidget&module=SearchSubmit&pgtype=Homepage#/space+propulsion/since1851/allresults/%d/allauthors/newest/' %i) for i in range (1,10)]

	def parse(self, response):
        #iterate entries
		
		for entry in response.css('div.element2'):
            
            #retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'NYTimes'
			temp_string = entry.css('span.dateline::text').extract_first()
			item['brief'] = entry.css('p.summary').extract_first()
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('a::text').extract_first()

			# check time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

			print(item)

			yield item


