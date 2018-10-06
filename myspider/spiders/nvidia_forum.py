import re, os
import scrapy
from myspider.items import MyspiderItem


class MySpider(scrapy.Spider):
    name = 'nvidia_forum'
    # start_urls = ['https://devtalk.nvidia.com/default/board/58/cuda-setup-and-installation/1/?orderBy=created-DESC']

    def start_requests(self):
        urls = ['https://devtalk.nvidia.com/default/board/58/cuda-setup-and-installation/1/?orderBy=created-DESC']

        for page in xrange(1,160):
            page = str(page)
            next_page = urls[0].replace('1', page)
            print next_page
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse(self, response):
        items = MyspiderItem()
        items['topics'] = response.xpath(r'//div[@class="body board-topics"]/div/@data-topic').extract()
        # print items['topics']
        for topicID in items['topics']:
            started_by = response.xpath('//div[@data-topic="'+topicID+'"]/div[@class="topic-first-comment"]/p/text()').extract()
            author = response.xpath('//div[@data-topic="'+topicID+'"]/div[@class="topic-first-comment"]/p/a/text()').extract()
            title = response.xpath('//div[@data-topic="'+topicID+'"]/div/div/div[@class="raw-topic-title"]/text()').extract()
            link = "https://devtalk.nvidia.com/default/topic/"+topicID+"/"+title[0]
            views = response.xpath('//div[@data-topic="'+topicID+'"]/div/p[@class="topic-views"]/text()').extract()
            replies = response.xpath('//div[@data-topic="'+topicID+'"]/div/p[@class="topic-replies"]/text()').extract()

            # with open(r'./topic.txt', 'a+') as fp:
            #     if len(author):
            #         fp.write(author[0]+';')
            #     fp.write(views.pop()+';')
            #     fp.write(started_by[0]+'\n')
                # fp.write(title[0]+';')
                # fp.write(link+'\n')
            if len(author):
                author_ = author.pop()
            else:
                author_ = 'empty name'
            views_ = views[0].replace(',','').replace(' Views', '')
            replies_ = replies[0].replace(',','').replace(' Replies', '')
            yield {
                'author': author_,
                'views': int(views_),
                'replies': int(replies_),
                'title': title.pop(),
                'started_by': started_by.pop(),
                'link': link,
                'topicID': int(topicID)
            }




