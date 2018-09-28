import re
import scrapy
from myspider.items import MyspiderItem


class MySpider(scrapy.Spider):
    name = 'nvidia_forum'
    start_urls = ['https://devtalk.nvidia.com/default/board/58/cuda-setup-and-installation/?orderBy=created-DESC']


    def parse(self, response):
        item = []
        items = MyspiderItem()
        items['topics'] = response.xpath('//div[@class="topic   unread"]/@data-topic').extract()
        print items['topics']
        for topicID in items['topics']:
            # print "topic=", topic, type(topic)
            started_by = response.xpath('//div[@data-topic="'+topicID+'"]/div[@class="topic-first-comment"]/p/text()').extract()
            author = response.xpath('//div[@data-topic="'+topicID+'"]/div[@class="topic-first-comment"]/p/a/text()').extract()
            title = response.xpath('//div[@data-topic="'+topicID+'"]/div/div/div[@class="raw-topic-title"]/text()').extract()
            link = "\"https://devtalk.nvidia.com/default/topic/"+topicID+"/"+title[0]+"\""

            with open(r'/home/fancy/scrapy/myspider/topic.txt', 'a+') as fp:
                fp.write(author[0]+';')
                fp.write(started_by[0]+';')
                fp.write(title[0]+';')
                fp.write(link+'\n')




