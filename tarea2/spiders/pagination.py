import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import re

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    allowed_domains = ['wikipedia.org']
    start_urls = ["https://es.wikipedia.org/wiki/Tecnolog%C3%ADa"]
    
    max_tokens = 10000
    current_tokens = 0
    urls_followed = []
    urls_to_follow = []
    
    def __init__(self, *args, **kwargs):
        super(PaginationSpider, self).__init__(*args, **kwargs)
        if 'tokens' in kwargs:
            tokens = int(kwargs.get('tokens'))
            self.max_tokens = tokens
        self.urls_followed = [i for i in self.start_urls]


    def parse(self, response):
        # get title
        title = response.css('[id="firstHeading"]::text').extract_first().strip()

        # check if already got the max tokens
        if self.current_tokens > self.max_tokens:
            return
        
        # extract article content
        html_body = response.css('div.mw-parser-output').extract_first()
        
        # remove html content with Beautiful soup library
        text = BeautifulSoup(html_body,'lxml').get_text()
        text = text.replace('↑','')
        text = re.sub('\n+','. ',text)      # all text in one line
        text = re.sub('[ \t]+',' ',text)    # consecutive spaces and tabs as one space
        text = re.sub('\\[[0-9A-Za-z]+\\]','',text)     # remove references
        text = re.sub('(\.+ *)+','. ',text) # multiple dots with spaces between them
        text = title+'. '+text.strip()
        
        # split in tokens
        tokens = text.split(' ')
        
        if self.current_tokens + len(tokens) > self.max_tokens:
            partial_text = ' '.join(tokens[0:self.max_tokens-self.current_tokens])
            self.current_tokens = self.max_tokens
            yield {'text':partial_text}
        else:
            self.current_tokens += len(tokens)
            yield {'text':text}
        
        # log url, title and current tokens
        self.log(f'******** URL:{response.request.url}')
        self.log(f'\t** Title:{title}')
        self.log(f'\t** current tokens:{self.current_tokens}')

        if self.current_tokens < self.max_tokens:
            # search new urls to follow
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
                    
                    # search if current link already followed or is on list to follow
                    if tmp_url in self.urls_followed or tmp_url in self.urls_to_follow:
                        continue
                    
                    # add url to follow
                    self.urls_to_follow.append(tmp_url)

            # follow next url in list
            if len(self.urls_to_follow)>0:
                # follow first url
                current_url = self.urls_to_follow[0]
                self.urls_to_follow.pop(0)
                # mark as followed
                self.urls_followed.append(current_url)
                # follow
                yield response.follow(url=current_url, callback=self.parse)
                
          