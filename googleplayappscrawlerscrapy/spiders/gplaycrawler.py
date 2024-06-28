# -*- coding: utf-8 -*-
import scrapy
import googlemaps
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from googleplayappscrawlerscrapy.items import GoogleplayappscrawlerscrapyItem
from urllib.parse import urlparse

gmaps = googlemaps.Client(key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

class MySpider(CrawlSpider):
  name = "gplaycrawler"
  allowed_domains = ["play.google.com"]
  start_urls = ["https://play.google.com/store/apps/"]
  rules = [Rule(LinkExtractor(allow=(r'apps',),deny=(r'reviewId'),canonicalize=True,unique=True),follow=True,callback='parse_link')]

    	
  def abs_url(url, response):
      """Return absolute link"""
      base = response.xpath('//head/base/@href').extract()
      if base:
        base = base[0]
      else:
        base = response.url
      return urlparse.urljoin(base, url)
    
  def parse_link(self,response):
      hxs = HtmlXPathSelector(response)
      titles = hxs.select('/html')
      items = []
      for titles in titles:
        item = GoogleplayappscrawlerscrapyItem()

        if not (titles.xpath('//*[@class="document-title"]/div/text()').extract()):
            item["Item_name"] = ''.join('Null')
        else:
            item["Item_name"] =''.join(titles.xpath('//*[@class="document-title"]/div/text()').extract())

        if not (titles.xpath('//*[@itemprop="datePublished"]/text()').extract()):
            item["Updated"] = ''.join('Null')
        else:
            item["Updated"] = ''.join(titles.xpath('//*[@itemprop="datePublished"]/text()').extract())

        if not (titles.xpath('//*[@itemprop="author"]/a/span/text()').extract()):
            item["Author"] = ''.join('Null')
        else:
            item["Author"] = ''.join(titles.xpath('//*[@itemprop="author"]/a/span/text()').extract())

        if not (titles.xpath('//*[@itemprop="fileSize"]/text()').extract()):
            item["Filesize"] = ''.join('Null')
        else:
            item["Filesize"] = ''.join(titles.xpath('//*[@itemprop="fileSize"]/text()').extract())

        if not (titles.xpath('//*[@itemprop="numDownloads"]/text()').extract()):
            item["Downloads"] = ''.join('Null')
        else:
            item["Downloads"] = ''.join(titles.xpath('//*[@itemprop="numDownloads"]/text()').extract())

        if not (titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract()):
            item["CurrentVersion"] = ''.join('Null')
        else:
            item["CurrentVersion"] = ''.join(titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract())

        if not (titles.xpath('//*[@itemprop = "operatingSystems"]/text()').extract()):
            item["OperatingSystems"] = ''.join('Null')
        else:
            item["OperatingSystems"] = ''.join(titles.xpath('//*[@itemprop = "operatingSystems"]/text()').extract())

        if not (titles.xpath('//*[@itemprop="contentRating"]/text()').extract()):
            item["Content_rating"]= ''.join('Null')
        else:
            item["Content_rating"] = ''.join(titles.xpath('//*[@itemprop="contentRating"]/text()').extract())

        if not (titles.xpath('//a[@class="dev-link"][1]/@href').extract()):
            item["Official_link"]= ''.join('Null')
        else:
            item["Official_link"] = ''.join(titles.xpath('//a[@class="dev-link"][1]/@href').extract())

        if not (titles.xpath('//a[@class="dev-link"][2]/@href').extract()):
            item["Official_mail"] =''.join('Null')
        else:
            item["Official_mail"] =''.join(titles.xpath('//a[@class="dev-link"][2]/@href').extract())

        if not (titles.xpath('//*[@itemprop="genre"]/text()').extract()):
            item["Genre"]= ''.join('Null')
        else:
            item["Genre"] = ''.join(titles.xpath('//*[@itemprop="genre"]/text()').extract())

        if not (titles.xpath('//meta[@itemprop="price"]/@content').extract()):
            item["Price"] = ''.join('Null')
        else:
            item["Price"] = ''.join(titles.xpath('//meta[@itemprop="price"]/@content').extract())

        if not (titles.xpath('//*[@class="score"]/text()').extract()):
            item["Rating_value"] = ''.join('Null')
        else:
            item["Rating_value"] = ''.join(titles.xpath('//*[@class="score"]/text()').extract())

        if not (titles.xpath('//*[@class="reviews-num"]/text()').extract()):
            item["Review_number"] = ''.join('Null')
        else:
            item["Review_number"] = ''.join(titles.xpath('//*[@class="reviews-num"]/text()').extract())

        if not (titles.xpath('//*[@jsname = "C4s9Ed"]/text()').extract()):
            item["Description"] = ''.join('Null')
        else:
            item["Description"] = ''.join(titles.xpath('//*[@jsname = "C4s9Ed"]/text()').extract())

        #item["IAP"] = ''.join(titles.xpath('//*[@class="inapp-msg"]/text()').extract())
        if not (titles.xpath('//*[@class="badge-title"]/text()').extract()):
            item["Developer_badge"] = ''.join('Null')
        else:
            item["Developer_badge"] = ''.join(titles.xpath('//*[@class="badge-title"]/text()').extract())

        if not (titles.xpath('//*[@class="content physical-address"]/text()').extract()):
            item["Physical_address"] = ''.join('Null')
        else:
            item["Physical_address"] = ''.join(gmaps.geocode(titles.xpath('//*[@class="content physical-address"]/text()').extract())[0]['formatted_address'])
            # geocode_result = gmaps.geocode(titles.xpath('//*[@class="content physical-address"]/text()').extract())
            # if geocode_result:
            #   item["Latitude"] = ''.join(geocode_result[0]["geometry"]["location"]["lat"])
            #   item["Longitude"] = ''.join(geocode_result[0]["geometry"]["location"]["lng"])

        components = gmaps.geocode(titles.xpath('//*[@class="content physical-address"]/text()').extract())[0]['address_components']
        for c in components:
            if "country" in c['types']:
                country = c['long_name']
                item["Country"] = ''.join(country)

        if not(titles.xpath('//*[@class="play-action-container"]/@data-video-url').extract()):
            item["Video_URL"] = ''.join('Null')
        else:
            item["Video_URL"] = ''.join(titles.xpath('//*[@class="play-action-container"]/@data-video-url').extract())

        if not (titles.xpath('//*[@itemprop="author"]/a/@href').extract()):
            item["Developer_ID"] = ''.join('Null')
        else:
            item["Developer_ID"] = ''.join(titles.xpath('//*[@itemprop="author"]/a/@href').extract())

        if not (titles.xpath('//*[@class="rating-bar-container five"]/span[3]/text()').extract()):
            item["five_stars"] = ''.join('Null')
        else:
            item["five_stars"] = ''.join(
                titles.xpath('//*[@class="rating-bar-container five"]/span[3]/text()').extract())

        if not(titles.xpath('//*[@class="rating-bar-container four"]/span[3]/text()').extract()):
            item["four_stars"] = ''.join('Null')
        else:
            item["four_stars"] = ''.join(
                titles.xpath('//*[@class="rating-bar-container four"]/span[3]/text()').extract())

        if not (titles.xpath('//*[@class="rating-bar-container three"]/span[3]/text()')):
            item["three_stars"] = ''.join('Null')
        else:
            item["three_stars"] = ''.join(titles.xpath('//*[@class="rating-bar-container three"]/span[3]/text()').extract())

        if not (titles.xpath('//*[@class="rating-bar-container two"]/span[3]/text()').extract()):
            item["two_stars"] = ''.join('Null')
        else:
            item["two_stars"] = ''.join(titles.xpath('//*[@class="rating-bar-container two"]/span[3]/text()').extract())

        if not (titles.xpath('//*[@class="rating-bar-container one"]/span[3]/text()').extract()):
            item["one_star"] = ''.join('Null')
        else:
            item["one_star"] = ''.join(titles.xpath('//*[@class="rating-bar-container one"]/span[3]/text()').extract())

        if not (titles.xpath('//*[@class="review-text"]/text()').extract()):
            item["review"] = ''.join('Null')
        else:
            item["review"] = ''.join(titles.xpath('//*[@class="review-text"]/text()').extract())

        if not (titles.xpath('//*[@class ="recent-change"]/text()').extract()):
            item["whats_new"] = ''.join('Null')
        else:
            item["whats_new"] = ''.join(titles.xpath('//*[@class ="recent-change"]/text()').extract())

        if not (titles.xpath('//a[@class="title"][1]/text()').extract()):
            item["similar_apps"] = ''.join('Null')
        else:
            item["similar_apps"] = ''.join(titles.xpath('//a[@class="title"][1]/text()').extract())

        if item["Item_name"] != 'Null':
            items.append(item)
      return items







