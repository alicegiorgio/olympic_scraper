# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OlimpiadiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    athlete = scrapy.Field()
    number_of_games=scrapy.Field()
    born = scrapy.Field()
    specialty = scrapy.Field()
    place = scrapy.Field()
    result = scrapy.Field()
    nationality = scrapy.Field()
    sport = scrapy.Field()
    pass
