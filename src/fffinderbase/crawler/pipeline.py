class ItemPipeline:
    def process_item(self, item, spider):
        if hasattr(item, "save"):
            item.save()

        return item
