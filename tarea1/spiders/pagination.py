import scrapy
from scrapy.selector import Selector

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    allowed_domains = ['tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Hotels-g295366-Antigua_Sacatepequez_Department-Hotels.html']
    custom_settings = {'FEEDS':{'results.json':{'format':'json', 'overwrite': True}}}
    max_hotels = 10
    max_reviews_per_hotel = 5

    def parse(self, response, current_hotels=0):
        hotels = response.css('div.listing_title a').getall()
        for hotel in hotels:
            if current_hotels < self.max_hotels:
                current_hotels += 1
                yield response.follow(hotel, callback=self.parseHotel)

        href_ = response.xpath("//a[contains(@class, 'ui_button') and contains(@class, 'nav') and contains(@class, 'next') and contains(@class, 'primary')]/@href").extract_first()
        if (current_hotels < self.max_hotels and href_ != None):
            yield response.follow(href_, callback=self.parse, cb_kwargs={'current_hotels': current_hotels})
            
    def parseHotel(self, response, current_reviews=0):
        reviews = response.css('div[data-test-target="reviews-tab"] div[data-test-target="HR_CC_CARD"]').getall()
        hotel_name = response.css('[id="HEADING"]::text').extract_first()
        for review in reviews:
            if (current_reviews < self.max_reviews_per_hotel): 
                current_reviews +=1
                yield self.parseReview(review, hotel_name, response.url)

        href_ = response.xpath("//a[contains(@class, 'ui_button') and contains(@class, 'nav') and contains(@class, 'next') and contains(@class, 'primary')]/@href").extract_first()
        if (current_reviews < self.max_reviews_per_hotel and href_ != None):
            yield response.follow(href_, callback=self.parseHotel, cb_kwargs={'current_reviews': current_reviews})
    
    def parseReview(self, html, hotel_name='', url=''):
        response = Selector(text=html)
        title = response.css('div[data-test-target="review-title"] a span span::text').extract_first()
        rating_classes = response.css('div[data-test-target="review-rating"] span::attr(class)').extract_first().split(' ')
        reviewer = response.css('a.ui_header_link::text').extract_first()
        rating = ''
        rating_value = 0
        for rc in rating_classes:
            if rc.startswith('bubble_'):
                rating_value = int(rc.replace('bubble_', ''))
                if rating_value > 40:
                    rating = 'Excelent'
                elif rating_value > 30:
                    rating = 'Very Good'
                elif rating_value > 20:
                    rating = 'Average'
                elif rating_value > 10:
                    rating = 'Poor'
                else:
                    rating = 'Terrible'
        
        review = ' '.join(response.css('q span::text').extract())

        result = {
            'url': url
            , 'hotel_name': hotel_name
            , 'rating': rating
            , 'rating_value': rating_value
            , 'reviewer': reviewer
            , 'title': title
            , 'review': review
        }
        return result
