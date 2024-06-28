# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleplayappscrawlerscrapyItem(scrapy.Item):
    # define the fields for your item here like:

    Item_name = scrapy.Field()
    Updated = scrapy.Field()
    Author = scrapy.Field()
    Filesize = scrapy.Field()
    Downloads = scrapy.Field()
    CurrentVersion = scrapy.Field()
    OperatingSystems= scrapy.Field()
    Content_rating = scrapy.Field()
    Official_link = scrapy.Field()
    Official_mail = scrapy.Field()
    Genre = scrapy.Field()
    Price = scrapy.Field()
    Rating_value = scrapy.Field()
    Review_number = scrapy.Field()
    Description = scrapy.Field()
    Developer_badge = scrapy.Field()
    Physical_address = scrapy.Field()
    # Latitude = scrapy.Field()
    # Longitude = scrapy.Field()
    Country = scrapy.Field()
    Video_URL = scrapy.Field()
    Developer_ID = scrapy.Field()
    five_stars = scrapy.Field()
    four_stars = scrapy.Field()
    three_stars = scrapy.Field()
    two_stars = scrapy.Field()
    one_star = scrapy.Field()
    review= scrapy.Field()
    whats_new= scrapy.Field()
    similar_apps = scrapy.Field()




    
	

