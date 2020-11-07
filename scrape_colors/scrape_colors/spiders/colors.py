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
            follow=True,
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
                    {
                        "id": self.count_palette,
                        "color1": colors[0],
                        "color2": colors[1],
                        "color3": colors[2],
                        "color4": None,
                        "color5": None,
                        "foundcolor": 1,
                    }
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
                try:
                    if colors[4]:
                        item.append(
                            {
                                "id": self.count_palette,
                                "color1": colors[0],
                                "color2": colors[1],
                                "color3": colors[2],
                                "color4": colors[3],
                                "color5": colors[4],
                                "foundcolor": 0,
                            }
                        )
                except:
                    try:
                        if colors[3]:
                            item.append(
                                {
                                    "id": self.count_palette,
                                    "color1": colors[0],
                                    "color2": colors[1],
                                    "color3": colors[2],
                                    "color4": colors[3],
                                    "color5": None,
                                    "foundcolor": 0,
                                }
                            )
                    except:
                        item.append(
                            {
                                "id": self.count_palette,
                                "color1": colors[0],
                                "color2": colors[1],
                                "color3": colors[2],
                                "color4": None,
                                "color5": None,
                                "foundcolor": 0,
                            }
                        )
                finally:
                    colors = []
        return item
