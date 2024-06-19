import sys
from importlib import import_module
from os import PathLike
from pathlib import Path
from types import ModuleType
from typing import Union

from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.utils.spider import iter_spider_classes


def _import_file(filepath: Union[str, PathLike]) -> ModuleType:
    abspath = Path(filepath).resolve()
    if abspath.suffix not in (".py", ".pyw"):
        raise ValueError(f"Not a Python source file: {abspath}")
    dirname = str(abspath.parent)
    sys.path = [dirname] + sys.path
    try:
        module = import_module(abspath.stem)
    finally:
        sys.path.pop(0)
    return module


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("spider", nargs="?", type=str)

    def handle(self, *args: list[any], **opts: list[any]) -> str | None:
        filename = Path(opts["spider"])
        if not filename.exists():
            raise UsageError(f"File not found: {filename}\n")
        try:
            module = _import_file(filename)
        except (ImportError, ValueError) as e:
            raise UsageError(f"Unable to load {str(filename)!r}: {e}\n")
        spclasses = list(iter_spider_classes(module))
        if not spclasses:
            raise UsageError(f"No spider found in file: {filename}\n")
        spidercls = spclasses.pop()

        process = CrawlerProcess()
        process.crawl(spidercls)
        process.start()
        if process.bootstrap_failed:
            self.exitcode = 1
