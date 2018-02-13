
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
    name = 'scientificus_Meta'
    allowed_domains = ['scientificamerican.com']
    start_urls = ['https://www.scientificamerican.com/search/?q=propulsion&sortby=releasedate&source=&days=']
    def parse(self, response):
        # iterate entries
        item = ScrapyItem()
        for entry in response.css('div.listing-wide__inner'):
            url_temp = entry.css('a::attr(href)').extract_first()
            next_page = response.urljoin(url_temp)
            #retrieve info for our current post
            item['source'] = 'scientificamerican'
            temp_string = entry.css('time::text').extract_first()
            item['date'] = entry.css('div.t_meta::text').extract_first().split(' — ')[0]
            item['brief'] = entry.css('p::text').extract_first()
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
            request = scrapy.Request(next_page, callback=self.parse_article)
            request.meta['item'] = item

            yield request



    def parse_article(self, response):


            string = response.css('article').css('div').css('p::text').extract()

            item = response.meta['item']
            item['body'] = string
            return item


