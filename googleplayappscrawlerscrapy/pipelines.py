# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter
from scrapy import signals
from scrapy.exporters import XmlItemExporter
import datetime
import mysql.connector
from mysql.connector import errorcode

dateTimeString = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class GoogleplayappscrawlerscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonPipeline(object):
    def __init__(self):
        self.file = open("GPlaystore" + dateTimeString + ".json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.fields_to_export = ['Item_name', 'Author', 'Developer_ID', 'CurrentVersion','OperatingSystems',
                                          'Content_rating','Developer_badge', 'Downloads', 'Filesize', 'Genre',
                                          'Official_link','Official_mail', 'Physical_address','Country', 'Price',
                                          'Updated', 'Video_URL', 'one_star', 'two_stars', 'three_stars',
                                          'four_stars', 'five_stars', 'Review_number', 'Rating_value', 'Description',
                                          'review', 'similar_apps', 'whats_new']
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class XmlPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open("GPlaystore" + dateTimeString + ".xml", 'w+b')
        self.files[spider] = file
        self.exporter = XmlItemExporter(file)
        self.exporter.fields_to_export = ['Item_name', 'Author', 'Developer_ID', 'CurrentVersion', 'OperatingSystems',
                                          'Content_rating', 'Developer_badge', 'Downloads', 'Filesize', 'Genre',
                                          'Official_link', 'Official_mail', 'Physical_address', 'Country', 'Price',
                                          'Updated', 'Video_URL', 'one_star', 'two_stars', 'three_stars',
                                          'four_stars', 'five_stars', 'Review_number', 'Rating_value', 'Description',
                                          'review', 'similar_apps', 'whats_new']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class CsvPipeline(object):
    def __init__(self):
        self.file = open("GPlaystore" + dateTimeString + ".csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.fields_to_export = ['Item_name', 'Author', 'Developer_ID', 'CurrentVersion', 'OperatingSystems',
                                          'Content_rating', 'Developer_badge', 'Downloads', 'Filesize', 'Genre',
                                          'Official_link', 'Official_mail', 'Physical_address', 'Country', 'Price',
                                          'Updated', 'Video_URL', 'one_star', 'two_stars', 'three_stars',
                                          'four_stars', 'five_stars', 'Review_number', 'Rating_value', 'Description',
                                          'review', 'similar_apps', 'whats_new']
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def create_valid_csv(self, item):
        for key, value in item.items():
            is_string = (isinstance(value, basestring))
            if (is_string and ("," in value.encode('utf-8'))):
                item[key] = "\"" + value + "\""


class MySqlPipeline(object):
    table = 'GPScrape1'
    conf = {
        'port': '3306',
        'charset': 'utf8mb4',
        'user': 'sqoop',
        'password': 'sqoopit',
        'database': 'GooglePlayStore',
        'raise_on_warnings': True
    }

    def __init__(self, **kwargs):
        self.cnx = self.mysql_connect()

    def open_spider(self, spider):
        print("spider open")

    def process_item(self, item, spider):
        print("Saving item into db ...")
        self.save(dict(item))
        return item

    def close_spider(self, spider):
        self.mysql_close()

    def mysql_connect(self):
        try:
            return mysql.connector.connect(**self.conf)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def save(self, row):
        cursor = self.cnx.cursor()
        create_query = ("INSERT INTO " + self.table +
                        '(Author,Content_rating ,Country,CurrentVersion,Description ,'
                        'Developer_ID,Developer_badge,Downloads,Filesize,Genre,'
                        'Item_name,Official_link,Official_mail,OperatingSystems ,'
                        'Physical_address,Price ,Rating_value,Review_number,Updated ,'
                        'Video_URL,five_stars,four_stars,one_star,review,similar_apps ,'
                        'three_stars,two_stars,whats_new)'
                        'VALUES (%(Author)s,%(Content_rating)s,%(Country)s,%(CurrentVersion)s,%(Description)s,'
                        '%(Developer_ID)s,%(Developer_badge)s,%(Downloads)s,%(Filesize)s,'
                        '%(Genre)s,%(Item_name)s,%(Official_link)s,%(Official_mail)s, '
                        '%(OperatingSystems)s,%(Physical_address)s,'
                        '%(Price)s, %(Rating_value)s,%(Review_number)s,%(Updated)s,'
                        '%(Video_URL)s, %(five_stars)s,%(four_stars)s,'
                        '%(one_star)s,%(review)s,%(similar_apps)s,%(three_stars)s, %(two_stars)s,%(whats_new)s)')

        # Insert new row
        cursor.execute(create_query, row)
        lastRecordId = cursor.lastrowid

        # Make sure data is committed to the database
        self.cnx.commit()
        cursor.close()
        print("Item saved with ID: {}".format(lastRecordId))

    def mysql_close(self):
        self.cnx.close()
