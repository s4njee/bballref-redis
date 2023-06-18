# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import json

from itemadapter import ItemAdapter

class JsonWriterPipeline:

    def open_spider(self, spider):
        if spider.name == 'bballref':
            self.file = open('items.json', 'w')

        elif spider.name == 'playerspider':
            self.file = open('playerurls.json', 'w')

    def close_spider(self, spider):
        if spider.name == 'bballref':
            self.file.close()

        elif spider.name == 'playerspider':
            self.file.close()

    def process_item(self, item, spider):
        # if spider.name == 'bballref':
            # if item['Date']:
            #     line = json.dumps(item) + "\n"
            #     self.file.write(line)
            # return item

        if spider.name == 'playerspider':
            print(item)
            if item:
                line = json.dumps(item['url']) + "\n"
            self.file.write(line)
        return item