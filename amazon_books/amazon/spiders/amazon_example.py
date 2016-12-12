# -*- coding: utf-8 -*-
import scrapy
from amazon.items import AmazonItem

class AmazonExampleSpider(scrapy.Spider):
    name = "amazon_example"
    allowed_domains = ["amazon.cn"]
    start_urls = ['https://www.amazon.cn/gp/bestsellers/books/ref=zg_bs_books_pg_1?ie=UTF8&pg=1']

    def parse(self, response):
        # 获取单页上面的数据
        zg_itemRow_lst = response.xpath('//div[@class="zg_itemRow"]')
        for zg_itemRow_row in zg_itemRow_lst:
            item = AmazonItem()
            item['rank_num'] = zg_itemRow_row.xpath('.//div/span[@class="zg_rankNumber"]/text()').extract_first().split()
            item['book_name'] = zg_itemRow_row.xpath('.//a[@class="a-link-normal"]/text()')[2].extract()
            item['author'] = zg_itemRow_row.xpath('.//span[@class="a-size-small a-color-base"]/text()').extract_first()
            item['star'] = zg_itemRow_row.xpath('.//span[@class="a-icon-alt"]/text()').extract_first()
            item['book_type'] = zg_itemRow_row.xpath('.//span[@class="a-size-small a-color-secondary"]/text()').extract_first()
            item['price'] = zg_itemRow_row.xpath('.//span[@class="a-size-base a-color-price"]/text()').extract_first()
            yield item

        # 自动获取多页的内容
        xpath_next_page = '//li[@class="zg_page zg_selected"]/following-sibling::li/a/@href'
        if response.xpath(xpath_next_page):
            url_next_page = response.xpath(xpath_next_page).extract_first()
            request = scrapy.Request(url_next_page, callback=self.parse)
            yield request
