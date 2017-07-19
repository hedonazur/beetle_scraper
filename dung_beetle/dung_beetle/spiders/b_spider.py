import scrapy
import re

from dung_beetle.items import DungBeetleItem
from scrapy.http import Request

class BeetleSpider(scrapy.Spider):
    name = "b_spider"
    
    def start_requests(self):

        urls = [
            'http://scarabaeinae.myspecies.info/gallery', 
            """'http://scarabaeinae.myspecies.info/gallery?page=1',
            'http://scarabaeinae.myspecies.info/gallery?page=2',
            'http://scarabaeinae.myspecies.info/gallery?page=3',
            'http://scarabaeinae.myspecies.info/gallery?page=4',
            'http://scarabaeinae.myspecies.info/gallery?page=5',
            'http://scarabaeinae.myspecies.info/gallery?page=6',
            'http://scarabaeinae.myspecies.info/gallery?page=7',
            'http://scarabaeinae.myspecies.info/gallery?page=8',
            'http://scarabaeinae.myspecies.info/gallery?page=9',
            'http://scarabaeinae.myspecies.info/gallery?page=10',
            'http://scarabaeinae.myspecies.info/gallery?page=11',
            'http://scarabaeinae.myspecies.info/gallery?page=12',
            'http://scarabaeinae.myspecies.info/gallery?page=13',
            'http://scarabaeinae.myspecies.info/gallery?page=14',
            'http://scarabaeinae.myspecies.info/gallery?page=15',
            """
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        for i in response.css('.file-image-jpeg'):
            item = DungBeetleItem()
            #imageURL = i.css(".element-invisible a").xpath("@href").extract()
            tex = i.css(".element-invisible a::text").extract()[0]
            words = tex.split()
            types = ["lectotype", "paratype", "syntype", "holotype", "cotype", "type", "LECTOTYPE", "PARATYPE", "SYNTYPE", "HOLOTYPE", "COTYPE", "TYPE"]
            nomenclatural_type = None
            author = None
            if len(words) == 2:
                genus = words[0]
                species = words[1]
            if words[1]== "cf":
                genus = words[0]
                species = words[1] + " " + words[2]
                author = ' '.join(words[3:])
            if len(words) > 2 and words[1] != "cf":
                genus = words[0]
                species = words[1]
                author = ' '.join(words[2:])

            for tip in types:
                if tip in words:
                    nomenclatural_type = tip
            item['genus'] =  genus
            item['species'] =  species
            item['author'] =  author
            #item['image_urls'] = imageURL 
            item['nomenclatural_type'] = nomenclatural_type
                                                           
            url = response.urljoin(i.css(".content span a::attr(href)").extract()[0])
            request = scrapy.Request(url, callback=self.parse_licence)
            request.meta['item'] = item
            yield request

    def parse_licence(self, response):
            item = response.meta['item']
            item['licence'] = response.css('.field-name-field-cc-licence .field-item a').xpath("@href").extract()
            item['creator'] = response.css('.field-name-field-creator .field-items div::text').extract()
            yield item
                          
        


    

    