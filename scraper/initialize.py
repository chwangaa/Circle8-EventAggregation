from models import PagePattern, SiteCrawler

botanic_css = {"title": "h1",
               "description": ".fdteventsdescription",
               "start_date": ".feeventsdate .fdteventsdate"}

event_url = 'http://www.botanic.cam.ac.uk/Botanic/Event.aspx'

botanic_url = 'http://www.botanic.cam.ac.uk/Botanic/WhatsOn.aspx'
botanic_base_url = 'http://www.botanic.cam.ac.uk/Botanic/Event.aspx'

botanic_page_pattern = PagePattern(title=botanic_css['title'],
                                   description=botanic_css['description'],
                                   start_time=botanic_css['start_date'],
                                   site_name='Botanic Garden',
                                   base_url=botanic_base_url,
                                   )
botanic_page_pattern.save()

botanic_site = SiteCrawler(index_page_url=botanic_url,
                           event_urls=event_url,
                           site_name='Botanic Garden',
                           event_page_crawler=botanic_page_pattern)

botanic_site.save()

botanic_site.fetch_events(storeFetched=True)


adc_css = {"title": ".showInfo h1",
           "description": "article.darkGreyBg",
           "start_date": ".showInfo > p"}

adc_event_url = 'https://www.adctheatre.com/whats-on'

adc_url = 'https://www.adctheatre.com/whats-on.aspx'
adc_base_url = 'https://www.adctheatre.com/whats-on.aspx'

adc_page_pattern = PagePattern(title=adc_css['title'],
                               description=adc_css['description'],
                               start_time=adc_css['start_date'],
                               site_name='ADC Theatre',
                               base_url=adc_base_url,
                               )
adc_page_pattern.save()

adc_site = SiteCrawler(index_page_url=adc_url,
                       event_urls=adc_event_url,
                       site_name='ADC',
                       event_page_crawler=adc_page_pattern)

adc_site.save()

adc_site.fetch_events(storeFetched=True)