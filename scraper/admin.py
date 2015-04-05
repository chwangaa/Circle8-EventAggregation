from django.contrib import admin
from django import forms
from django.contrib.admin.helpers import ActionForm
import models
# Register your models here.

class SiteCrawlerInline(admin.TabularInline):
    model = models.SiteCrawler


class SiteCrawlerAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'index_page_url', 'event_page_crawler')
    list_inlines = ('event_page_crawler')

    def fetch_events(self, request, queryset):
        for crawler in queryset:
            crawler.fetch_events(storeFetched=True)

    actions = ['fetch_events']


class PageCrawlerForm(ActionForm):
    page_url = forms.URLField()


class PagePatternAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'base_url')
    fields = ('site_name', 'base_url', ('title', 'description', 'start_time'))
    inlines = [SiteCrawlerInline]

    action_form = PageCrawlerForm

    def fetch_event(self, request, queryset):
        for crawler in queryset:
            event = crawler.fetch_event(request.POST['page_url'])
            title = event['title']
        self.message_user(request, ("EVENT titled %s created"%title))

    actions = ['fetch_event']


class EventScrappedAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'downloaded_on', )
    fieldsets = [(None, {'fields': ['url']}),
                 ('event info', {'fields': ['title', 'start_date', 'description']}),
                 ('state', {'fields': ['state']})
                 ]


class ScraperLogAdmin(admin.ModelAdmin):
    list_display = ('run_on', 'crawler', 'num_parsed_events')
    fields = ('run_on', 'crawler', 'num_parsed_events')

admin.site.register(models.PagePattern, PagePatternAdmin)
admin.site.register(models.SiteCrawler, SiteCrawlerAdmin)
admin.site.register(models.EventScrapped, EventScrappedAdmin)
admin.site.register(models.ScraperLog, ScraperLogAdmin)
