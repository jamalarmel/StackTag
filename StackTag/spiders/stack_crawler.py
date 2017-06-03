# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from StackTag.items import StacktagItem


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']
    #start_urls = ['http://stackoverflow.com/questions?pagesize=50&sort=newest']
    start_urls = ['https://stackoverflow.com/questions/tagged/python?page=1&sort=votes&pagesize=15']

    rules = (
        #Rule(LinkExtractor(allow=r'questions\?page=[0-9]&sort=votes'),callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'questions/tagged/python\?page=[0-9]&sort=votes'),callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        questions = response.xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = StacktagItem()
            item['url'] = question.xpath('a[@class="question-hyperlink"]/@href').extract()[0]
            item['title'] = question.xpath('a[@class="question-hyperlink"]/text()').extract()[0]
            yield item
