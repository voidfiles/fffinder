from dataclasses import dataclass
from urllib.parse import urlparse

import scrapy
from django.db import IntegrityError
from knbase.models import OutboundLink as OutboundLinkModel
from scrapy.linkextractors import LinkExtractor

from .utils import canonical_url


@dataclass
class OutboundLink:
    domain: str
    url: str
    canonical_url: str
    link: str

    def save(self):
        try:
            OutboundLinkModel.objects.create(
                domain=self.domain,
                url=self.canonical_url,
                raw_url=self.url,
                outbound_url=self.link,
            )
        except IntegrityError:
            raise


class Web(scrapy.Spider):
    name = "web"
    link_extractor = LinkExtractor()
    custom_settings = {
        "HTTPCACHE_ENABLED": True,
        "SPIDER_MIDDLEWARES": {
            "scrapy.spidermiddlewares.offsite.OffsiteMiddleware": 100,
        },
        "ITEM_PIPELINES": {
            "crawler.pipeline.ItemPipeline": 300,
        },
    }

    def link_only(self, response: scrapy.http.Response):
        url = canonical_url(response.url)
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)

            yield OutboundLink(urlparse(link.url).netloc, response.url, url, link.url)

    def parse(self, response: scrapy.http.Response):
        url = canonical_url(response.url)
        domain = urlparse(response.url).netloc
        for link in self.link_extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)
            yield OutboundLink(urlparse(link.url).netloc, response.url, url, link.url)

        for a in self.parse_items(response, url, domain):
            yield a

    def parse_items(self, response: scrapy.http.Response, url: str, domain: str):
        raise NotImplementedError("You must implment the parse_items")
