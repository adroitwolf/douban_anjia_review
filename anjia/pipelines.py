# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json
import os
from itemadapter import ItemAdapter


class ReviewPipeline:
    # 打开文件
    def __init__(self) -> None:
        self.file = codecs.open('data.json','w+',encoding='UTF-8')
    # 爬虫开始的时候
    def open_spider(self,spider):
        
        # self.file.write('[\n')
        pass
    # 将爬取到的item传到json文件中
    def process_item(self, item, spider):
        item_json = json.dumps(dict(item),ensure_ascii=False)
        self.file.write(item_json +'\n')
        return item
    
    # 爬虫结束时候的方法：
    def close_spider(self,spider):
        # self.file.seek(-2,os.SEEK_END)
        # self.file.truncate()
        # self.file.write('\n]')
        # self.file.close()
        pass