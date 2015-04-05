from django.db import models
import urllib2
from bs4 import BeautifulSoup
from sets import Set
from urlparse import urljoin


class AggregatedEventState:
    NEW = 0
    ADDED_TO_AGORA = 1
    NOT_OF_INTEREST = 2
    HAS_ERROR = 3

    CHOICES = (
        (NEW, u'New'),
        (ADDED_TO_AGORA, u"Added to Agora"),
        (NOT_OF_INTEREST, u"Not of interest"),
        (HAS_ERROR, u"Has error"),
    )


class EventScrapped(models.Model):
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.CharField(max_length=255)
    downloaded_on = models.DateTimeField(auto_now_add=True)
    state = models.IntegerField(choices=AggregatedEventState.CHOICES,
                                default=AggregatedEventState.NEW)

    def __unicode__(self):
        return self.title


class PagePattern(models.Model):
    base_url = models.URLField(max_length=255, null=True)
    site_name = models.CharField(max_length=20, null=True)

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)

    def __unicode__(self):
        return self.site_name

    def attributes(self):
        return {"title": self.title,
                "description": self.description,
                "start_date": self.start_time}

    def storeEvent(self, event):
        EventScrapped(url=event['url'], title=event['title'],
                      description=event['description'],
                      start_date=event['start_date']).save()

    def fetch_event(self, page_url, storeFetched=True):
        response = urllib2.urlopen(page_url)
        html = response.read()
        soup = BeautifulSoup(html)
        event = {"url": page_url}
        for attribute, css in self.attributes().iteritems():
            value_list = soup.select(css)
            try:
                value = ""
                for string in value_list[0].stripped_strings:
                    value = value + string
                event[attribute] = value
            except Exception as exception:
                print exception
                print attribute, "not found"
                return None

        if storeFetched:
            self.storeEvent(event)

        return event


class ScraperLog(models.Model):
    run_on = models.DateTimeField(auto_now_add=True)
    crawler = models.ForeignKey('SiteCrawler', editable=False)
    num_parsed_events = models.IntegerField()


class SiteCrawler(models.Model):
    index_page_url = models.URLField(max_length=255)
    event_urls = models.URLField(max_length=255)
    event_page_crawler = models.ForeignKey(PagePattern,
                                           related_name='index_pages')
    site_name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.site_name

    def fetch_events(self, storeFetched=True):
        response = urllib2.urlopen(self.index_page_url)
        html = response.read()
        soup = BeautifulSoup(html)
        all_urls = Set()
        for link in soup.find_all('a'):
            relative_url = link.get('href')
            absolute_url = urljoin(self.index_page_url, relative_url)
            if absolute_url.startswith(self.event_urls):
                all_urls.add(absolute_url)
        events = []
        event_crawler = self.event_page_crawler
        for event_url in all_urls:
            event = event_crawler.fetch_event(event_url, storeFetched)
            if event:
                events.append(event)
        num_events = len(events)
        if num_events > 0:
            ScraperLog(crawler=self, num_parsed_events=num_events).save()
        return events
