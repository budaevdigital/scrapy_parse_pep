import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    URL = "peps.python.org"
    name = "pep"
    allowed_domains = [URL]
    start_urls = [f"https://{URL}/"]

    def parse(self, response):
        pep_links = response.css("a.pep::attr('href')").getall()
        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        raw_header = response.css("h1:contains('PEP')::text").get()
        number = int(raw_header.split(" ")[1])
        # По срезу заголовка, найдём название PEP без номера
        # Надём первый индекс искомого символа (+3) до начала заголовка
        name = raw_header[(raw_header.find(" – ") + 3) :]
        status = response.css("dt:contains('Status') + dd::text").get()
        pep_item = {"number": number, "name": name, "status": status}
        yield PepParseItem(pep_item)
