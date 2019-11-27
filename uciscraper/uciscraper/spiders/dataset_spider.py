import scrapy
import urllib

import os, io

class DatasetSpider(scrapy.Spider):
    name = "dataset"

    def start_requests(self):
        urls = [
            "../machine-learning-databases/abalone/", 
            "../machine-learning-databases/breast-cancer/", 
        ]

        for url in urls:
            cleanUrl = urllib.parse.urljoin('https://archive.ics.uci.edu/ml/base/', url)
            yield scrapy.Request(url=cleanUrl, callback=self.parse_directory)

    def parse_directory(self, response):
        for nLink, link in enumerate(response.css('a::attr(href)')):
            if nLink > 1:
                href = link.get()
                yield scrapy.Request(
                    url=response.urljoin(href),
                    callback=self.save_file
                )
    def save_file(self, response):
        urlParts = response.url.split('/')
        savePath = './data/%s' % (urlParts[-2])
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        with open(os.path.join(savePath, urlParts[-1]), 'wb') as f:
            f.write(response.body)