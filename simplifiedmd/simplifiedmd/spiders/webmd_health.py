import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import bleach

class WebMDSpider(scrapy.Spider):
	name = "webmd_health"
	start_urls = [
        'https://www.webmd.com/a-to-z-guides/health-topics',
    ]
	
	# follow links to next alphabet page
	def parse(self, response):
		a2z = []
		for i in range (97, 123):
			a2z.append("https://www.webmd.com/a-to-z-guides/health-topics" + "?pg=" + chr(i))
		for j in range(len(a2z)):
			yield Request(response.urljoin(a2z[j]), callback = self.parse_dis)
	
	# go through the diseases on the alpha page
	def parse_dis(self, response):
		alpha = response.css('ul.az-index-results-group-list a::attr(href)').extract()
		for i in range(len(alpha)):
			yield Request(response.urljoin(alpha[i]), callback = self.parse_page)
	
	# parse article
	def parse_page(self, response):
		txt_str = ""
		for page in response.css('div.article-page'):
			for paragraph in page.css('p').extract():
				tmp = paragraph.strip()
				tmp = bleach.clean(tmp, tags=[], strip=True)
				txt_str += tmp
		yield {
			'title': response.css('title::text').extract_first(),
			'text': txt_str,
		}