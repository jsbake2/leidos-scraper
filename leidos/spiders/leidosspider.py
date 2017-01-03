import time
from time import sleep
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from leidos.items import LeidosItem
from scrapy.http import HtmlResponse
import json
import re
from scrapy.exceptions import CloseSpider

L = open('parseInfo', 'w')


class LeidosSpider(CrawlSpider):
    name = "leidosJobStart"
    page = 1
    ajaxURL = "http://jobs.leidos.com/ListJobs/All/Page-"

    def start_requests(self):
      yield Request(self.ajaxURL + str(self.page), callback=self.parse_listings , headers={'Referer':(self.ajaxURL + str(self.page))})

    def parse_listings(self, response):
        c = 0
        jobs = response.xpath('//*[@class="coljobtitle"]/a/@href').extract()
        L.write(str(len(jobs))+'  -  '+str(self.page)+'\n')

        for job_url in jobs:
          if re.search('ShowJob', job_url):
            c += 1
            L.write("\tGenerated URL for job #: "+str(c)+'\n')
            job_url = 'http://jobs.leidos.com' + job_url
            job_url = self.__normalise(job_url)
            yield Request(url=job_url, callback=self.parse_details)

        # go to next page...
        self.page += 1
        #sleep(30)
        if self.page == 107:
          L.write("Just  hit the magic number.. finishing up now!")
          #raise CloseSpider("No more pages... exiting...")
        else:
          yield Request(self.ajaxURL + str(self.page), callback=self.parse_listings, headers={'Referer':(self.ajaxURL + str(self.page))})


    def parse_details(self, response):
      sel = Selector(response)
      job = sel.xpath('//*[@id="mainbody-jobs"]')
      item = LeidosItem()
      # Populate job fields
      item['title'] = job.xpath('//*[@id="mainbody-jobs"]/h1/text()').extract()
      item['location'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[2]/div[1]/div/div[3]/div[2]/text()').extract()
      item['applink'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[1]/a/@href').extract()
      item['description'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[2]/div[2]/div[1]/div[2]').extract()
      item['travel'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[2]/div[1]/div/div[5]/div[2]/text()').extract()
      item['job_category'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[2]/div[1]/div/div[2]/div[2]/text()').extract()
      item['clearance_have'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[2]/div[1]/div/div[8]/div[2]/text()').extract()
      item['clearance_get'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[2]/div[1]/div/div[8]/div[2]/text()').extract()
      item['job_number'] = job.xpath('//*[@id="mainbody-jobs"]/div[3]/div[2]/div[1]/div/div[1]/div[2]/text()').extract()
      item['page_url'] = response.url
      item = self.__normalise_item(item, response.url)
      #sleep(1)
      L.write((str(item['page_url']))+"\n")
      return item

    def __normalise_item(self, item, base_url):
      '''
      Standardise and format item fields
      '''
      # Loop item fields to sanitise data and standardise data types
      for key, value in vars(item).values()[0].iteritems():
        item[key] = self.__normalise(item[key])
        # Convert job URL from relative to absolute URL
        #item['job_url'] = self.__to_absolute_url(base_url, item['job_url'])
        return item

    def __normalise(self, value):
      # Convert list to string
      value = value if type(value) is not list else ' '.join(value)
      # Trim leading and trailing special characters (Whitespaces, newlines, spaces, tabs, carriage returns)
      value = value.strip()
      return value

    def __to_absolute_url(self, base_url, link):
      '''
      Convert relative URL to absolute URL
      '''
      import urlparse
      link = urlparse.urljoin(base_url, link)
      return link

    def __to_int(self, value):
      '''
      Convert value to integer type
      '''
      try:
        value = int(value)
      except ValueError:
        value = 0
      return value

    def __to_float(self, value):
      '''
      Convert value to float type
      '''
      try:
        value = float(value)
      except ValueError:
        value = 0.0
      return value
