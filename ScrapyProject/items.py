# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyItem(scrapy.Item):
	
    # Source website or magazine
	source = scrapy.Field()
    # Date of the article
	date = scrapy.Field()
    # Title
	title = scrapy.Field()
    # Synopsis
	brief = scrapy.Field()
	# Body
	body = scrapy.Field()
    # Link to the article
	url = scrapy.Field()
    # Main author
	author = scrapy.Field()
    # Time of the extraction
	tstamp = scrapy.Field()
    # Tag
	tags = scrapy.Field()
    # Company
	company = scrapy.Field()
