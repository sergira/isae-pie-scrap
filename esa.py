# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import datetime
import scrapy
from ScrapyProject.items import ScrapyItem

class EsaSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	name = 'esa'


	allowed_domains = ['http://www.esa.int']

	start_urls = [('http://www.esa.int/esasearch?q=propulsion&start=%d' % (i*10+1)) for i in range(0,50)]

	def parse(self, response):

		news = response.css('div.sr')
		titles = news.css('h4')
		briefs = news.css('p')
		# iterate entries
		for j in range(len(titles)):


            #retrieve info for our current post
			item = ScrapyItem()

			item['source'] = 'esa'
			item['date'] = briefs[j].css('::text').extract_first()
			if briefs[j].css('b::text').extract_first()!='...':
				continue
			item['brief'] = briefs[j].css('::text').extract()[1]
			item['url'] = titles[j].css('a::attr(href)').extract_first()
			item['title'] = titles[j].css('a::text').extract_first()

			# check time
			now = datetime.datetime.now()
			item['tstamp'] = now

			yield item
