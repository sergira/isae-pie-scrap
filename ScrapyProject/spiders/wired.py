# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.


import scrapy
from ScrapyProject.items import ScrapyItem

class NewsSpider(scrapy.Spider):
	#item_id = ScrapyItem()
	#name = item_id.source[0]

	name = 'wired'
	allowed_domains = ['https://www.wired.com']

	#start_urls = [('https://www.wired.com/search/?q=rocket' % i) for i in range(1,50)]
	start_urls = ['https://www.wired.com/search/?page=1&q=rocket&size=200&sort=publishDate_tdt%20desc&types%5B0%5D=article']
	#start_urls = ['https://www.wired.com/search/?q=rocket']

	def parse(self, response):
	# iterate entries
		for entry in response.css('div').css('li.archive-item-component'):
	
			#retrieve info for our current post
			item = ScrapyItem()
		
		# p.post-excerpt   class de type p = post-excerpt			
			item['source'] = 'wired'
			item['date'] = entry.css('time::text').extract_first()
			item['brief'] = entry.css('a').css('p.archive-item-component__desc::text').extract_first()
			item['url'] = entry.css('a::attr(href)').extract_first()
			item['title'] = entry.css('a').css('h2::text').extract_first()

		   # item['date'] = entry.css('time::text').extract_first()
		   # item['brief'] = entry.css('p.post-excerpt::text').extract_first()
		   # item['url'] = entry.css('h2').css('a::attr(href)').extract_first()
		   # item['title'] = entry.css('h2').css('a::text').extract_first()

			yield item


