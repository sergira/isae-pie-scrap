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
	name = 'spacenews'


	allowed_domains = ['http://spacenews.com']

	start_urls = [('http://spacenews.com/?s=propulsion&orderby=date-desc&paged=%d' % i) for i in range(1,50)]

	def parse(self, response):
        # iterate entries
		for entry in response.css('div.launch-article'):
            
            #retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'spacenews'
			temp_string  = entry.css('time::text').extract_first()
			item['brief'] = entry.css('p.post-excerpt::text').extract_first()
			item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
			item['title'] = entry.css('h2').css('a::text').extract_first()

			# check time
			now = datetime.datetime.now()
			now  = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
			item['tstamp'] = now

			# transfer time into ISO 8601
			temp = timestring.Date(temp_string).date
			item['date']  = temp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")

			yield item


