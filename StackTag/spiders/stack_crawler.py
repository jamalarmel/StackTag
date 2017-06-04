# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from StackTag.items import StacktagItem


class StackCrawlerSpider(CrawlSpider):
    name = 'stack_crawler'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python?page=1&sort=votes&pagesize=15']
    rules = (
        Rule(LinkExtractor(allow=r'questions/tagged/python\?page=[0-9]&sort=votes'),callback='parse_item', follow=True),
    )

    BASE_URL = 'https://stackoverflow.com/'

    def parse(self, response):
        links = response.xpath('//a[@class="question-hyperlink"]/@href').extract()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        item = StacktagItem()
        item["link"] = response.url
        item["qbody"] = "".join(response.xpath('//div[@class="post-text"]/p/text()').extract())
        return item