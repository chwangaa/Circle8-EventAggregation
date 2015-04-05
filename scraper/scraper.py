import scrapy
from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from sets import Set
# import your spider here


class Event(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    start_date = scrapy.Field()
    description = scrapy.Field()


class EventCrawlSpider(CrawlSpider):

    def __init__(self, href, css, **kw):
        self.rules = [Rule(LinkExtractor(allow=href), 'parse_event')]
        self.css = css
        self.name = "default"
        super(EventCrawlSpider, self).__init__(**kw)

    def parse_event(self, response):
        url = response.url
        css = self.css
        title = response.css(css["title"]).extract()
        description = response.css(css["description"]).extract()
        start_date = response.css(css["start_date"]).extract()[0]
        new_event = Event(url=url, title=title, description=description,
                          start_date=start_date)
        return new_event


class MultipleEventsScraper():

    scraped_events = Set()

    def __init__(self, start_urls, href, css, name="MultipleEventsScraper"):
        self.start_urls = start_urls
        self.href = href
        self.css = css
        self.name = name

    def callback(self, spider, reason):
        self.stats = spider.crawler.stats.get_stats()
        print "spider closed"
        reactor.stop()

    def storeEvent(self, item, response, spider):
        self.scraped_events.add(item)
        print "new event scraped"

    def fetch_events(self):
        spider = EventCrawlSpider(self.href, self.css, name=self.name,
                                  start_urls=self.start_urls)
        settings = get_project_settings()
        # output_path = self.name + '.json'
        # settings.overrides['FEED_URI'] = output_path
        # settings.overrides['FEED_FORMAT'] = 'json'
        crawler = Crawler(settings)
        crawler.signals.connect(self.callback, signal=signals.spider_closed)
        crawler.signals.connect(self.storeEvent, signal=signals.item_scraped)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        # log.start()
        reactor.run()
        return self.scraped_events


class EventSpider(Spider):

    def __init__(self, css, start_urls, **kw):
        self.css = css
        self.start_urls = start_urls
        super(Spider, self).__init__(**kw)

    def parse(self, response):
        url = response.url
        css = self.css
        title = response.css(css["title"]).extract()
        description = response.css(css["description"]).extract()
        start_date = response.css(css["start_date"]).extract()[0]
        new_event = Event(url=url, title=title, description=description,
                          start_date=start_date)
        return new_event


class SingleEventScraper():

    scraped_events = Set()

    def __init__(self, start_urls, css, name="SingleEventScraper"):
        self.start_urls = start_urls
        self.css = css
        self.name = name

    def callback(self, spider, reason):
        self.stats = spider.crawler.stats.get_stats()
        reactor.stop()

    def storeEvent(self, item, response, spider):
        self.scraped_events.add(item)
        print "new event scraped"

    def fetch_event(self):
        spider = EventSpider(self.css, self.start_urls, name=self.name)
        settings = get_project_settings()
        # output_path = self.name + '.json'
        # settings.overrides['FEED_URI'] = output_path
        # settings.overrides['FEED_FORMAT'] = 'json'
        crawler = Crawler(settings)
        crawler.signals.connect(self.callback, signal=signals.spider_closed)
        crawler.signals.connect(self.storeEvent, signal=signals.item_scraped)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()
        # log.start()
        reactor.run()
        return self.scraped_events
