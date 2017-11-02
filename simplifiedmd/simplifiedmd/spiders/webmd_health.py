import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import bleach
import webmd_health_const as CONST

class WebMDSpider(scrapy.Spider):
	name = 'webmd_health'
	start_urls = [
        CONST.WEBMD_BASE_URL
    ]
	
	# follow links to next alphabet page
	def parse(self, response):
		letter_urls = []

		for letter in range(CONST.ASCII_LETTER_A, CONST.ASCII_LETTER_Z):
			letter_urls.append(CONST.WEBMD_BASE_URL + CONST.WEBMD_ALPHABET_EXT + chr(letter))

		for url in letter_urls:
			yield Request(response.urljoin(url), callback = self.parse_topics)
	
	# go through the topics on the alphabet page
	def parse_topics(self, response):
		topics = response.css('ul.az-index-results-group-list a::attr(href)').extract()

		for topic in topics:
			yield Request(response.urljoin(topic), callback = self.parse_page)
	
	# parse a topice page
	def parse_page(self, response):
		txt_str = ''
		for page in response.css('div.article-page').extract():
			tmp = page.strip()
			tmp = bleach.clean(tmp, tags=[], strip=True)
			txt_str += ' ' + tmp
			
			if len(txt_str) > 0:
				yield {
					'title': response.css('title::text').extract_first(),
					'text': ' '.join(txt_str.strip().split()),
                }
			
			else:
				hub_links = []
				for link in response.xpath('//*[(@id = "ContentPane32")]//li//a').css('a::attr(href)').extract():
					hub_links.append(link)
				
				hub_links.append(response.xpath('//*[(@id = "ContentPane35")]//*[contains(concat( " ", @class, " " ), concat( " ", "button", " " ))]').css('a::attr(href)').extract_first())
				for l in hub_links:
					yield Request(response.urljoin(l), callback = self.parse_hub)
					
	# parse a hub link
	def parse_hub(self, response):
		links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "link-title", " " ))]').css('a::attr(href)').extract()
		if len(links) > 0:
			for l in links:
				txt_str = ''
				for page in response.css('div.article-page').extract():
					tmp = page.strip()
					tmp = bleach.clean(tmp, tags=[], strip=True)
					txt_str += ' ' + tmp
					
					if len(txt_str) > 0:
						yield {
							'title': response.css('title::text').extract_first(),
							'text': ' '.join(txt_str.strip().split()),
						}
		
		else:
			txt_str = ''
			for page in response.css('div.article-page').extract():
				tmp = page.strip()
				tmp = bleach.clean(tmp, tags=[], strip=True)
				txt_str += ' ' + tmp
				
				if len(txt_str) > 0:
					yield {
						'title': response.css('title::text').extract_first(),
						'text': ' '.join(txt_str.strip().split()),
					}