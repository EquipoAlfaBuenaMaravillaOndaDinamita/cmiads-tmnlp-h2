import scrapy
from scrapy.selector import Selector

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://es.wikipedia.org/wiki/Wikipedia:Portada']
    custom_settings = {'FEEDS':{'results.json':{'format':'json', 'overwrite': True}}}
    max_tokens = 10

    def parse(self, response):
        # entry point
        yield from response.follow_all(css='[id="main-tfa"] h2 span a::text', callback=self.parseArticle)
            
    def parseArticle(self, response, current_tokens=0):
        title = response.css('[id="firstHeading"]::text').extract_first().strip()
        body = response.css('div.mw-parser-output > *').extract()
        result = self.parseRecursive({'level': 1, 'title': title, 'children': []}, body)
        yield result
        # reviews = response.css('div[data-test-target="reviews-tab"] div[data-test-target="HR_CC_CARD"]').getall()
        # hotel_name = response.css('[id="HEADING"]::text').extract_first()
        # for review in reviews:
        #     if (current_reviews < self.max_reviews_per_hotel): 
        #         current_reviews +=1
        #         yield self.parseReview(review, hotel_name, response.url)

        # href_ = response.xpath("//a[contains(@class, 'ui_button') and contains(@class, 'nav') and contains(@class, 'next') and contains(@class, 'primary')]/@href").extract_first()
        # if (current_reviews < self.max_reviews_per_hotel and href_ != None):
        #     yield response.follow(href_, callback=self.parseHotel, cb_kwargs={'current_reviews': current_reviews})
    
    def parseRecursive(self, current_object, children):
        while len(children) > 0:
            if (not children[0].startswith('<p') and not children[0].startswith('<h')):
                deleted = children.pop(0)
                continue
            
            if (children[0].startswith('<p')):
                child = children.pop(0)
                child_object = Selector(text=child)
                child_text = ' '.join(child_object.css('p::text').extract())
                current_object['children'].append(child_text)
            elif (children[0].startswith('<h')): 
                level = children[0][2:3]
                self.log(f'level: {level}')
                level = int(level)
                if (current_object['level'] < level):
                    child = children.pop(0)
                    child_object = Selector(text=child)
                    child_text = child_object.css(f'h{level}::text').extract_first()
                    children_object = self.parseRecursive({'title': child_text, 'level': level, 'children': []}, children)
                    current_object['children'].append(children_object)
                else:
                    return current_object
        return current_object