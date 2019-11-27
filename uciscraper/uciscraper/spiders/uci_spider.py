import scrapy
import urllib

class UciSpider(scrapy.Spider):
    name = "uci"

    def start_requests(self):
        urls = [
            "https://archive.ics.uci.edu/ml/datasets.php"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        counter = 0
        for dataset in response.css("table"):
            dsUrl = dataset.css("a::attr(href)").get()
            if dsUrl is not None and 'datasets' in dsUrl:
                ret = {
                    'datasetName': dataset.css("a::text").get(),
                    'datasetUrl': dsUrl
                }
                print(ret)
                if 'datasets' in ret['datasetUrl'] and ('format' not in ret['datasetUrl']):
                    counter += 1

                    yield scrapy.Request(url=urllib.parse.urljoin(response.url, dsUrl) , callback=self.parse_dataset)

    def parse_dataset(self, response):
        metaList = response.css('table')[3].css('td *::text').getall()
        paras = response.css('body > table > tr > td > p.normal').getall()
        metaData = {
            'url': response.url,
            'dsName': response.css('table span.heading b::text').get(),
            'dataSetCharacteristics': metaList[1],
            'nInstances': metaList[3],
            'area': metaList[5],
            'attributeCharacteristics': metaList[7].split(', '),
            'nAttributes': metaList[9],
            'dateDonated': metaList[11],
            'associatedTasks': metaList[13],
            'missingValues': metaList[15],
            'nWebHits': metaList[17],
            'source': paras[0],
            'dataSetInformation': paras[1],
            'attributeInformation': paras[2],
            'papers': paras[3],
            'citingPapers': paras[4],
            'citationRequest': paras[5],
            'dataFolderUrl': response.css('body > table > tr > td> table > tr > td a::attr(href)').getall()[0],
            'abstract': 'Abstract%s' % response.css('body > table > tr > td > table > tr > td > p.normal::text')[0].get() 
        }
        yield metaData