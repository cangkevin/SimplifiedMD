import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import bleach
import webmd_health_const as CONST
import unidecode as UNI
import re

class WebMDSpider(scrapy.Spider):
    name = 'webmd_health'
    start_urls = [CONST.WEBMD_BASE_URL]

    def parse(self, response):
        letter_urls = []
        for letter in range(CONST.ASCII_LETTER_A, CONST.ASCII_LETTER_Z):
            letter_urls.append(CONST.WEBMD_BASE_URL + CONST.WEBMD_ALPHABET_EXT + chr(letter))

        for url in letter_urls:
            yield Request(response.urljoin(url), callback=self.parse_topics)

    def parse_topics(self, response):
        topics = response.xpath('//ul[@class="az-index-results-group-list"]//a/text()').extract()
        topic_links = response.css('ul.az-index-results-group-list a::attr(href)').extract()
        for i in range(0, len(topics)):
            yield Request(response.urljoin(topic_links[i]), callback=self.parse_page, meta={'article_title': topics[i]})

    def parse_page(self, response):
        article_title = response.meta.get('article_title')
        try:
            test = response.css('div.article-page').css('p').extract_first()
            test = UNI.unidecode(test.strip())
            test = bleach.clean(test, tags=[], strip=True)
            test = ' '.join(test.strip().split())
            txt_str = ''
            if test.startswith(CONST.WEBMD_IMPORTANT_SECTION):
                p = re.compile('\(\d\d\d\)')
                summary_6 = response.css('p:nth-child(6)').extract_first()
                summary_8 = response.xpath('//p[(((count(preceding-sibling::*) + 1) = 8) and parent::*)]').extract_first()
                if summary_6 is None:
                    summary_6 = ''
                if summary_8 is None:
                    summary_8 = ''
                if p.search(summary_8):
                    summary_6 = UNI.unidecode(summary_6.strip())
                    summary_6 = bleach.clean(summary_6, tags=[], strip=True)
                    summary_6 = ' '.join(summary_6.strip().split())
                    txt_str = summary_6
                else:
                    summary_8 = UNI.unidecode(summary_8.strip())
                    summary_8 = bleach.clean(summary_8, tags=[], strip=True)
                    summary_8 = ' '.join(summary_8.strip().split())
                    txt_str = summary_8
            else:
                for paragraph in response.css('.active-page > p , .active-page li'):
                    tmp = paragraph.extract()
                    tmp = UNI.unidecode(tmp.strip())
                    tmp = bleach.clean(tmp, tags=[], strip=True)
                    tmp = ' '.join(tmp.strip().split())
                    txt_str += ' ' + tmp

            if len(txt_str) > 0:
                yield {'website_title': response.css('title::text').extract_first(),
                 'article_title': article_title,
                 'text': ' '.join(txt_str.strip().split())}
        except AttributeError:
            hub_links = []
            titles = []
            for link in response.xpath('//*[(@id = "ContentPane32")]//li//a').css('a::attr(href)').extract():
                hub_links.append(link)

            for title in response.xpath('//*[(@id = "ContentPane32")]//*[contains(concat( " ", @class, " " ), concat( " ", "long-list", " " ))]//a/text()').extract():
                titles.append(title)

            bottom_link = response.xpath('//*[(@id = "ContentPane35")]//*[contains(concat( " ", @class, " " ), concat( " ", "button", " " ))]').css('a::attr(href)').extract_first()
            bottom_title = response.xpath('//*[(@id = "ContentPane35")]//h2/text()').extract_first()
            if bottom_link is not None and bottom_title is not None:
                hub_links.append(bottom_link)
                titles.append(bottom_title)
            for i in range(len(hub_links)):
                yield Request(response.urljoin(hub_links[i]), callback=self.parse_hub, meta={'article_title': article_title, 'sub_title': titles[i]})

    def parse_hub(self, response):
        article_title = response.meta.get('article_title')
        sub_title = response.meta.get('sub_title')
        links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "link-title", " " ))]').css('a::attr(href)').extract()
        if len(links) > 0:
            link_titles = []
            for title in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "link-title", " " ))]/text()').extract():
                link_titles.append(title)

            for i in range(len(links)):
                txt_str = ''
                for paragraph in response.css('.active-page > p , .active-page li'):
                    tmp = paragraph.extract()
                    tmp = UNI.unidecode(tmp.strip())
                    tmp = bleach.clean(tmp, tags=[], strip=True)
                    tmp = ' '.join(tmp.strip().split())
                    txt_str += ' ' + tmp

                if len(txt_str) > 0:
                    yield {'website_title': response.css('title::text').extract_first(),
                     'article_title': article_title + ' ' + sub_title + ' ' + link_titles[i],
                     'text': ' '.join(txt_str.strip().split())}

        else:
            txt_str = ''
            for paragraph in response.css('.active-page > p , .active-page li'):
                tmp = paragraph.extract()
                tmp = UNI.unidecode(tmp.strip())
                tmp = bleach.clean(tmp, tags=[], strip=True)
                tmp = ' '.join(tmp.strip().split())
                txt_str += ' ' + tmp

            if len(txt_str) > 0:
                yield {'website_title': response.css('title::text').extract_first(),
                 'article_title': article_title + ' ' + sub_title,
                 'text': ' '.join(txt_str.strip().split())}

