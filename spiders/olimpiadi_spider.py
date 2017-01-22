# -*- coding: utf-8 -*-

# Define your item pipelines here
# We have no item pipelines, refer to settings.py to see how we deal with exporting data
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
from olimpiadi.items import OlimpiadiItem
import string
import time
import urlparse
import re


class OlimpiadiSpider(CrawlSpider):
    name = "olimpiadi"
    allowed_domains = ["olympic.org"]
    start_urls = ['https://www.olympic.org/london-2012']

    item={}

    def parse(self, response):
        sel = Selector(response)
        sports = sel.xpath('/html/body/div[@id="wrapper"]/div[@id="main"]/div[@class="main-holder main-container"]/section[@class="game-results-box mosaic-box"]/div[@class="select-box"]/ul/li/a')
        for s in sports:
            item=OlimpiadiItem()
            sport=s.xpath('text()').extract()[1]
            sport=sport.strip()
            url=s.xpath('@href').extract()[0]
            item['sport'] = sport
            yield Request(urlparse.urljoin(response.url, url[1:]), callback=self.parse_url_specialties, meta={"item":item}, dont_filter=True)

    def parse_url_specialties(self, response):
        sel = Selector(response)
        specialties = sel.xpath('/html/body/div[@id="wrapper"]/div[@id="main"]/div[@class="main-holder"]/div[@class="add-cols"]/div[@class="col"]/section[@class="event-box"]/h2/a')
        for s in specialties:
            item=OlimpiadiItem(response.request.meta["item"])
            specialty=s.xpath('text()').extract()[1]
            specialty=specialty.strip()
            specialtyUrl=s.xpath('@href').extract()[0]
            item['specialty']=specialty
            yield Request(url=urlparse.urljoin(response.url, specialtyUrl[13:]), callback=self.parse_url_athletes, meta={"item":item}, dont_filter=True)

    def parse_url_athletes(self, response):
        sel = Selector(response)
        athletes = sel.xpath('/html/body/div/div/div/section/table/tbody/tr/td/div/a/div/strong/text()').extract()
        for j in range(len(athletes)):
            item=OlimpiadiItem(response.request.meta["item"])
            athleteUrl = sel.xpath('/html/body/div/div/div/section/table/tbody/tr/td/div/a/@href').extract()[j]
            #athleteUrl = sel.xpath('/html/body/div/div/div/section[@class="table-box last active"]/table[@class="table4"]/tbody/tr[@class="slide"]/td/div[@class="slide-row"]/table[@class="col4"]/tbody/tr/td[@class="col2"]/div[@class="profile-section"]/a/@href').extract()[j]
            item['athlete']=athletes[j]
            try:
                place=sel.xpath('/html/body/div/div[@id="main"]/div[@class="main-holder"]/section[@class="table-box"]/table[@class="table4"]/tbody/tr/td[@class="col1"]').extract()[j]
            except:
                place=None
            def trasf_place(place):
                if len(place)==77:
                    return place[41:42]
                elif len(place)==78:
                    return place[41:43]
                elif len(place)==114:
                    return place[70:71]
                elif len(place)==120:
                    return place[76:77]
                else:
                    return None
            if place is not None:
                place=trasf_place(place)
            else: None
            try:
                item['place']=place
            except:
                item['place']=None
            try:
                result=sel.xpath('/html/body/div/div/div/section/table/tbody/tr/td[3]/text()').extract()[j]
                result=result.strip()
            except:
                result=None
            try:
                item['result']=result
            except:
                item['result']=None
            yield Request(url=urlparse.urljoin('http://www.olympic.org/', athleteUrl[1:]), callback=self.parse_url_athletesinfo, meta={"item":item}, dont_filter=True)

    def parse_url_athletesinfo(self, response):
        sel = Selector(response)
        item=OlimpiadiItem(response.request.meta["item"])
        try:
            born=sel.xpath('/html/body/div/div/section/div/div/ul/li[3]/div[@class="text-box"]/text()').extract()[1]
            born=born.strip()
        except:
            born=None
        try:
            number_of_games=response.xpath('/html/body/div/div[2]/section/div/div/ul/li[4]/div/a/text()').extract()
            number_of_games=len(number_of_games)
        except:
            number_of_games=None
        try:
            nationality=response.xpath('/html/body/div/div[2]/section/div/div/ul/li[2]/div/a/text()').extract()[0]
        except:
            nationality=None
        try:
            item['born']=born
        except:
            item['born']=None
        try:
            item['number_of_games']=number_of_games
        except:
            item['number_of_games']=None
        try:
            item['nationality']=nationality
        except:
            item['nationality']=None
        yield item
