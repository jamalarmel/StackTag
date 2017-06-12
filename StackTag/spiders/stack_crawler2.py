# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from StackTag.items import StacktagItem


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python?page=1&sort=votes&pagesize=30']

    # rules = (
    #     Rule(LinkExtractor(allow=r'questions/tagged/python\?page=0?[1-9]|[1-9][0-9]&sort=votes'),callback='parse_item', follow=True),
    # )
    rules = (
        Rule(LinkExtractor(allow=r'questions/tagged/python\?page=[0-9]&sort=votes'),callback='parse_item', follow=True),
    )
   
    BASE_URL = 'https://stackoverflow.com/'

    def parse_item(self, response):
        links = response.xpath('//a[@class="question-hyperlink"]/@href').extract()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        questions = response.xpath('//div[@id="mainbar"]')
        
        for question in questions:

            item = StacktagItem()
            #item["link"] = question.xpath('a[@class="question-hyperlink"]/@href').extract()
            item['body'] = "".join(question.xpath('//div[@class="post-text"]/p/text()').extract()) 
            yield item
