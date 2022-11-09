# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime as dt

from pathlib import Path

BASE_DIR = Path(__name__).absolute().parent

status_summary = {}


class PepParsePipeline:
    def open_spider(self, spider):
        ...

    def process_item(self, item, spider):
        if item["status"] not in status_summary:
            status_summary[item["status"]] = 1
        else:
            status_summary[item["status"]] += 1
        return item

    def close_spider(self, spider):
        filename = BASE_DIR / f'results/status_summary_{dt.now()}.csv'
        total = 0
        with open(
            filename, mode="w", encoding="utf-8"
        ) as file:
            file.write("Статус,Количество\n")
            for key, value in status_summary.items():
                file.write(f"{key},{value}\n")
                total += value
            file.write(f"Total,{total}")
