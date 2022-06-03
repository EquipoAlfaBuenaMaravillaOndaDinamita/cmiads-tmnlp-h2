import scrapy

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    allowed_domains = ['data.gov']
    start_urls = ['https://catalog.data.gov/dataset']
    custom_settings = {"FEEDS":{"results.json":{"format":"json", "overwrite": True}}}
    max_pages = 25

    def parse(self, response, page=1):
        ## parse page
        yield from response.follow_all(css='h3.dataset-heading a', callback=self.parseDocument, cb_kwargs={'page': page})

        ## search next page
        if (page < self.max_pages):
            href_ = response.xpath("//li/a[contains(text(), '»')]/@href").extract_first()
            if href_ is not None:
                # next_url = response.urljoin(href_)
                yield response.follow(href_, callback=self.parse, cb_kwargs={'page': page+1})
    
    def parseDocument(self, response, page):
        name = response.css('h1[itemprop="name"]::text').extract_first().strip()
        description = response.css('div[itemprop="description"] p::text').extract_first().strip()
        item = {'page': page,'url': response.url,'body': {}}
        if name:
            item['body']['title'] = name
        if description:
            item['body']['paragraph'] = description
        yield item
