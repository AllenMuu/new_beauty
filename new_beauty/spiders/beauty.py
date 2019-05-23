import scrapy

from new_beauty.items import NewBeautyItem


class beauty(scrapy.Spider):
    name = 'beauty'
    start_urls = [
        'https://www.meitulu.com/t/jipin/',
        'https://www.meitulu.com/t/nvshen/',
        'https://www.meitulu.com/t/changtui/',
        'https://www.meitulu.com/t/xinggan/'
    ]

    def parse(self, response):
        imgUrls = response.xpath("//p[@class='p_title']/a/@href").extract()
        for imgUrl in imgUrls:
            next_url = response.xpath("//a[@class='a1'][2]/@href").extract_first()
            if next_url is not None:
                # 下一页
                yield response.follow(next_url, callback=self.parse)
            yield scrapy.Request(imgUrl, callback=self.content)

    def content(self, response):
        item = NewBeautyItem()
        item['imgName'] = response.xpath("//div[@class='weizhi']/h1/text()").extract_first()[0:30]
        item['imgUrls'] = response.xpath("//div[@class='content']/center/img/@src").extract()
        yield item
        next_url = response.xpath("//div[@id='pages']/a[@class='a1'][2]/@href").extract_first()
        print(next_url)
        if next_url is not None:
            # 下一页
            yield response.follow(next_url, callback=self.content)