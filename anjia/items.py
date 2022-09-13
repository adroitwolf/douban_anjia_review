# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from turtle import title
import scrapy


class ReviewItem(scrapy.Item):
    author = scrapy.Field()
    pub_time = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    
    pass
