import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths="//h3/a"),
            callback='parse_item',
            follow=True,
            # process_request='set_user_agent'
        ),
    )

    def start_requests(self):
        yield scrapy.Request(
            url='http://books.toscrape.com/index.html',
            headers={
                'User-Agent': self.user_agent
            }
        )

    # def set_user_agent(self, request):
    #     request.headers['User-Agent'] = self.user_agent
    #     return request

    def parse_item(self, response):
        title = response.xpath("//h1/text()").get()
        price = response.xpath("//p[@class='price_color']/text()").get()
        yield {
            'title': title,
            'price': price,
            'link': response.url,
            'user_agent': response.request.headers['User-Agent']
        }
