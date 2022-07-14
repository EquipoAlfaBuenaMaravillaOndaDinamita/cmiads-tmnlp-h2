import scrapy, random, re
from scrapy.selector import Selector
from bs4 import BeautifulSoup

class PaginationSpider(scrapy.Spider):
    name = 'pagination'
    allowed_domains = ['wikipedia.org']
    start_urls = [
        "https://en.wikipedia.org/wiki/Sports"
    ]
    topic = 'Sports'
    
    max_tokens = 10000
    current_tokens = 0
    urls_followed = []
    urls_to_follow = []
    
    def __init__(self, *args, **kwargs):
        super(PaginationSpider, self).__init__(*args, **kwargs)
        if 'tokens' in kwargs:
            tokens = int(kwargs.get('tokens'))
            self.max_tokens = tokens
        if 'topic' in kwargs:
            self.topic = kwargs.get('topic')
            self.start_urls = [
                f'https://en.wikipedia.org/w/index.php?search={self.topic}&title=Special%3ASearch&go=Go&wprov=acrw1_-1'
            ]
            
        self.urls_followed = [i for i in self.start_urls]


    def parse(self, response):
        # get title
        title = response.css('[id="firstHeading"]').extract_first()
        title = BeautifulSoup(title,'lxml').get_text()
        if title != None:
            title = title.strip()

        # check if already got the max tokens
        if self.current_tokens > self.max_tokens:
            return
        
        # extract article content
        html_body = response.css('div.mw-parser-output').extract_first()

        # print(f'################# html_body: {html_body}')
        
        # remove html content with Beautiful soup library
        text = BeautifulSoup(html_body,'lxml').get_text()

        # print(f'################# beutifulsoup: {text}')
        text = text.replace('↑','')
        text = re.sub('\n+','. ',text)      # all text in one line
        text = re.sub('[ \t]+',' ',text)    # consecutive spaces and tabs as one space
        text = re.sub('\\[[0-9A-Za-z]+\\]','',text)     # remove references
        text = re.sub('(\.+ *)+','. ',text) # multiple dots with spaces between them

        if text != None and len(text.strip()) > 0 and title != None:
            # text = title+'. '+text.strip()
            text = text.strip()

            # split in tokens
            #tokens = text.split(' ')

            if False: #self.current_tokens + len(tokens) > self.max_tokens:
                partial_text = ' '.join(tokens[0:self.max_tokens-self.current_tokens])
                self.current_tokens = self.max_tokens
                yield {'topic': self.topic, 'title': title, 'text':partial_text}
            else:
                self.current_tokens += 1 # len(tokens)
                yield {'topic': self.topic, 'title': title, 'text':text}
        else: 
            self.log(f'******** error:{title}')
        
        # log url, title and current tokens
        self.log(f'******** URL:{response.request.url}')
        self.log(f'\t** Title:{title}')
        self.log(f'\t** current tokens:{self.current_tokens}')

        if self.current_tokens < self.max_tokens:
            # search new urls to follow
            for a in response.css('div.mw-parser-output *>a'):
                tmp_url = a.xpath('.//@href').get()
                # search only for wikipedia links
                if tmp_url!=None and tmp_url.startswith("/wiki/"):
                    if ':' in tmp_url:
                        continue
                    # discard images
                    if re.match( r'.*\.(?:gif|jpg|jpeg|tiff|png|svg)$', tmp_url, re.M|re.I):
                        continue
                    # discard files
                    if 'archivo:' in tmp_url.lower():
                        continue
                    # discard ISBN book searchs
                    if 'especial:fuentesdelibros' in tmp_url.lower():
                        continue
                    if 'portal:' in tmp_url.lower():
                        continue
                    
                    # search if current link already followed or is on list to follow
                    if tmp_url in self.urls_followed or tmp_url in self.urls_to_follow:
                        continue
                    
                    # add url to follow
                    self.urls_to_follow.append(tmp_url)

            # follow next url in list
            if len(self.urls_to_follow)>0:
                self.log(f'******** urls len:{len(self.urls_to_follow)}')
                # follow first url
                current_url = self.urls_to_follow[0]
                self.urls_to_follow.pop(0)
                # random.shuffle(self.urls_to_follow)
                # mark as followed
                self.urls_followed.append(current_url)
                # follow
                yield response.follow(url=current_url, callback=self.parse)
                
          