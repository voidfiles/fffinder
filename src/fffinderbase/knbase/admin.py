from django.contrib import admin

from .models import OutboundLink, Page


class OutboundLinkAdmin(admin.ModelAdmin):
    date_hierarchy = "created"
    list_display = ["domain", "url", "outbound_url"]


admin.site.register(OutboundLink, OutboundLinkAdmin)


class PageAdmin(admin.ModelAdmin):
    date_hierarchy = "content_date"
    list_display = ["domain", "author", "title", "url"]


admin.site.register(Page, PageAdmin)
