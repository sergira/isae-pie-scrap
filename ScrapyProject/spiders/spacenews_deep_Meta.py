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
	name = 'spacenews_deep_meta'


	allowed_domains = ['spacenews.com']

	start_urls = ['http://spacenews.com/?s=propulsion&orderby=date-desc&paged=1']
	i = 0

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

			# request to article page
			request = scrapy.Request(item['url'], callback=self.parse_article)
			request.meta['item'] = item

			yield request

		NewsSpider.i = NewsSpider.i+1
		
		next_search_url = response.css('div').css('main').css('p').css('a::attr(href)').extract_first()
				
		yield scrapy.Request(next_search_url, callback=self.parse)

	def parse_article(self, response):
			
		
		string = response.css('div').css('p::text').extract()

		item = response.meta['item']
		item['article'] = string
		return item
