# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 自定义抓取对象属性
class ReviewItem(scrapy.Item):
    author = scrapy.Field()
    pub_time = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    
    pass
