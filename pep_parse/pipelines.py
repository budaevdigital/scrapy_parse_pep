# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime as dt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pathlib import Path


BASE_DIR = Path(__name__).absolute().parent

status_summary = {}

Base = declarative_base()


class Pep(Base):
    __tablename__ = "pep"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(250))
    status = Column(String(50))


class PepParsePipeline:
    def open_spider(self, spider):
        engine = create_engine("sqlite:///results/pep_lists.db")
        # Удаляем существующие таблицы, если они есть
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        if item["status"] not in status_summary:
            status_summary[item["status"]] = 1
        else:
            status_summary[item["status"]] += 1
        pep = Pep(
            number=item["number"], name=item["name"], status=item["status"]
        )
        self.session.add(pep)
        self.session.commit()
        return item

    def close_spider(self, spider):
        filename = BASE_DIR / f"results/status_summary_{dt.now()}.csv"
        total = 0
        with open(filename, mode="w", encoding="utf-8") as file:
            file.write("Статус,Количество\n")
            for key, value in status_summary.items():
                file.write(f"{key},{value}\n")
                total += value
            file.write(f"Total,{total}")
        self.session.close()
