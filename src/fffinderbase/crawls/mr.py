import hashlib
from dataclasses import dataclass

from crawler.spyder import Web
from dateutil import parser
from django.db import IntegrityError
from knbase.models import Page
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


@dataclass
class Post:
    domain: str
    url: str
    canonical_url: str
    title: str
    author: str
    date: str
    html: str

    def hash(self):
        content = [self.title, self.canonical_url, self.author, self.html]
        content = [str(x) for x in content if x]
        content = ",".join(content)
        return hashlib.sha256(bytes(content, "utf-8")).hexdigest()

    def save(self):
        try:
            Page.objects.create(
                domain=self.domain,
                url=self.canonical_url,
                content_hash=self.hash(),
                raw_url=self.url,
                title=self.title,
                author=self.author,
                content_date=parser.isoparse(self.date),
                content=self.html,
            )
        except IntegrityError:
            pass


class mr(Web):
    name = "mr"
    start_urls = ["https://marginalrevolution.com/"]
    allowed_domains = ["marginalrevolution.com"]
    rules = (
        Rule(
            LinkExtractor(allow=(r"marginalrevolution/.*/.*/.*.html",)),
            callback="parse",
        ),
        Rule(LinkExtractor(allow=(r".*")), callback="link_only"),
    )

    def parse_items(self, response: Response, canonical_url: str, domain: str):
        article = response.css("article.post")
        if article:
            yield Post(
                domain=domain,
                url=response.url,
                canonical_url=canonical_url,
                title=article.css("h1.entry-title::text").get(),
                author=article.css(".byline .author a::text").get(),
                date=article.css(".entry-date::attr(datetime)").get(),
                html=article.css(".entry-content").extract_first(),
            )
