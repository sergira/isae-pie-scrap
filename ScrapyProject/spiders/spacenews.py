# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import scrapy
from ScrapyProject.items import ScrapyItem

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
			item['date'] = entry.css('time::text').extract_first()
			item['brief'] = entry.css('p.post-excerpt::text').extract_first()
			item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
			item['title'] = entry.css('h2').css('a::text').extract_first()

			yield item


