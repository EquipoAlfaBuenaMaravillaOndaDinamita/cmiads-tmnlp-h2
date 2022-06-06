import scrapy
from scrapy.selector import Selector

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotel_Review-g34438-d2253238-Reviews-Hampton_Inn_Suites_by_Hilton_Miami_Brickell_Downtown-Miami_Florida.html']
    custom_settings = {"FEEDS":{"results.csv":{"format":"csv", "overwrite": True}}}
    max_pages = 15

    def parse(self, response, page=1):
        reviews = response.css('div[data-test-target="reviews-tab"] div[data-test-target="HR_CC_CARD"]').getall()
        for review in reviews:
            yield self.parseReview(review)

        ## search next page
        href_ = response.xpath("//a[contains(@class, 'ui_button') and contains(@class, 'nav') and contains(@class, 'next') and contains(@class, 'primary')]/@href").extract_first()
        self.log(f'href: {href_}')
        if (page < self.max_pages and href_ != None):
            yield response.follow(href_, callback=self.parse, cb_kwargs={'page': page+1})
    
    def parseReview(self, html):
        response = Selector(text=html)
        title = response.css('div[data-test-target="review-title"] a span span::text').extract_first()
        rating_classes = response.css('div[data-test-target="review-rating"] span::attr(class)').extract_first().split(' ')
        rating = ''
        for rc in rating_classes:
            if 'bubble_50' in rc:
                rating = 'Excelent'
            elif 'bubble_40' in rc:
                rating = 'Very Good'
            elif 'bubble_30' in rc:
                rating = 'Average'
            elif 'bubble_20' in rc:
                rating = 'Poor'
            elif 'bubble_10' in rc:
                rating = 'Terrible'
        
        review = response.css('q span::text').extract_first()

        result = {
            "rating": rating
            , "title": title
            , "review": review
        }
        return result
