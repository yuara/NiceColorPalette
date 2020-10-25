import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector


class ColorsSpider(CrawlSpider):
    name = "colors"
    allowed_domains = ["colorion.co", "foundcolor.co"]
    start_urls = ["https://colorion.co/popular/", "https://foundcolor.co/"]

    rules = (
        Rule(
            LinkExtractor(allow=r"popular(\?page=)*\d*"),
            callback="parse_colorion",
            follow=False,
        ),
        Rule(
            LinkExtractor(allow="archive"), callback="parse_foundcolor", follow=False,
        ),
    )

    def __init__(self, *args, **kwargs):
        super(ColorsSpider, self).__init__(*args, **kwargs)
        self.count_palette = 0

    def parse_foundcolor(self, response):
        item = []
        colors = []
        for i in response.css("ul.archive-colors"):
            self.count_palette += 1
            for j in i.css("li::text").re(r"#\w{6}"):
                if j:
                    colors.append(j)
            if colors:
                item.append(
                    {"id": self.count_palette, "colors": colors, "foundcolor": 1}
                )
                colors = []
        return item

    def parse_colorion(self, response):
        item = []
        colors = []

        for i in response.xpath('//div[@class="col-md-4 text-center"]').extract():
            self.count_palette += 1
            for j in (
                Selector(text=i)
                .xpath('//div[@class="one animated zoomIn"]/@title')
                .re(r"#\w{6}")
            ):
                if j:
                    colors.append(j)
            if colors:
                item.append(
                    {"id": self.count_palette, "colors": colors, "foundcolor": 0}
                )
                colors = []
        return item
