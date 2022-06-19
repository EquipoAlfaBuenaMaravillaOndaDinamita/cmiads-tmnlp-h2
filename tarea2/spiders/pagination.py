import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import re

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    allowed_domains = ['wikipedia.org']
    start_urls = ["https://es.wikipedia.org/wiki/Tecnolog%C3%ADa"]
    custom_settings = {'FEEDS':{'test1.csv':{'format':'csv', 'overwrite': True}}}
    max_tokens = 10000
    current_tokens = 0
    
    def __init__(self, *args, **kwargs):
        super(PaginationSpider, self).__init__(*args, **kwargs)
        if 'tokens' in kwargs:
            tokens = int(kwargs.get('tokens'))
            self.max_tokens = tokens

    def parse(self, response):
        
        if self.current_tokens > self.max_tokens:
            return
        
        # extract article content
        html_body = response.css('div.mw-parser-output').extract_first()
        
        # remove html content with Beautiful soup library
        text = BeautifulSoup(html_body,'lxml').get_text()
        text = re.sub('\n+','. ',text)
        text = re.sub(' +',' ',text).replace('[editar]','').strip()
        
        tokens = text.split(' ')
        
        if self.current_tokens + len(tokens) > self.max_tokens:
            partial_text = ' '.join(tokens[0:self.max_tokens-self.current_tokens])
            self.current_tokens = self.max_tokens
            yield {'text':partial_text}
        else:
            self.current_tokens += len(tokens)
            yield {'text':text}
        
        self.log(f'************************************** current tokens:{self.current_tokens}')

        if self.current_tokens < self.max_tokens:
            # search new urls
            link_list = []
            for a in response.css('div.mw-parser-output a'):
                tmp_url = a.xpath('.//@href').get()
                # search only for wikipedia links
                if tmp_url!=None and tmp_url.startswith("/wiki/"):
                    # discard images
                    if re.match( r'.*\.(?:gif|jpg|jpeg|tiff|png|svg)$', tmp_url, re.M|re.I):
                        continue
                    # discard files
                    if 'archivo:' in tmp_url.lower():
                        continue
                    # discard ISBN book searchs
                    if 'especial:fuentesdelibros' in tmp_url.lower():
                        continue
                    link_list.append(tmp_url)
            # remove duplicate links
            link_list = list(set(link_list))

            for link in link_list:
                #self.log(link)
                if self.current_tokens > self.max_tokens:
                    break
                yield response.follow(url=link, callback=self.parse)
                #yield scrapy.Request(url='https://en.wikipedia.org'+link, callback=self.parse)
    
          