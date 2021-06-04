import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

    rules = (
        # This rule extracts links from which data is to be scrapped
        Rule(
            LinkExtractor(
                restrict_xpaths="//h3/a"),  # Link to the individual book
            callback='parse_item',  # Call the parse_item() function
            follow=True,
            process_request='set_user_agent'  # Set the user-agent header
        ),
        Rule(
            LinkExtractor(
                restrict_xpaths="//li[@class='next']/a"),  # This link is for next page
            process_request='set_user_agent'
        )
    )

    def start_requests(self):
        """ Starts the request with set User-Agent """
        yield scrapy.Request(
            # Start URL from where the data is to be scrapped
            url='http://books.toscrape.com/index.html',
            headers={
                'User-Agent': self.user_agent  # Spoof the user agent header
            }
        )

    def set_user_agent(self, request, response):
        """ Set the user-agent header """
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        """ Extract the required data from each link """
        title = response.xpath("//h1/text()").get()
        price = response.xpath("//p[@class='price_color']/text()").get()
        yield {
            'title': title,
            'price': price,
            'link': response.url,
        }
