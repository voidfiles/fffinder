from django.db import models


class Page(models.Model):
    url = models.CharField(max_length=2000, unique=True)
    domain = models.CharField(max_length=2000)
    raw_url = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    content_hash = models.CharField(max_length=512, unique=True)
    content = models.TextField(null=True)
    title = models.TextField(null=True)
    author = models.TextField(null=True)
    content_date = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("url", "content_hash")

    def __str__(self) -> str:
        return "Page(url='%s', title='%s')" % (self.url, self.title)


class OutboundLink(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    domain = models.CharField(max_length=2000)
    raw_url = models.CharField(max_length=2000)
    url = models.CharField(max_length=2000)
    outbound_url = models.CharField(max_length=2000)

    class Meta:
        unique_together = ("url", "outbound_url")

    def __str__(self) -> str:
        return "OutboundLink(url='%s', outbound_url='%s')" % (
            self.url,
            self.outbound_url,
        )
