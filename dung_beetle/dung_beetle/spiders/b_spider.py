import scrapy
import re

from dung_beetle.items import DungBeetleItem
from scrapy.http import Request

class BeetleSpider(scrapy.Spider):
    name = "b_spider"
    
    def start_requests(self):

        urls = [
            'http://scarabaeinae.myspecies.info/gallery', 
            'http://scarabaeinae.myspecies.info/gallery?page=1',
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
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        for i in response.css('.file-image-jpeg .element-invisible'):
            imageURL = i.css("a").xpath("@href").extract()
            tex = i.css("a::text").extract()[0]
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
           
            yield DungBeetleItem(species=species, genus=genus, author=author, nomenclatural_type=nomenclatural_type, image_urls = imageURL)       
        


    

    