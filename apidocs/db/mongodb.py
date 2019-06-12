from flask import (
    Blueprint
)
from pymongo import MongoClient
from bson.objectid import ObjectId

from apidocs.helpers.utils import get_configurations

bp = Blueprint('db', __name__)

class MongoDb:
    def __init__(self, col_name):
        config = get_configurations()
        db_mongo_prefix = config["database"]["mongo_prefix"]
        db_host = config["database"]["host"]
        db_port = config["database"]["port"]
        db_name = config["database"]["db"]

        self.page_size = config["pagination"]["max_per_page"]
        self.page_num = 1
        self.no_pagination = False

        if db_port and db_port != "":
            self.client = MongoClient("{}://{}".format(db_mongo_prefix, db_host), port=db_port)
        else:
            self.client = MongoClient("{}://{}".format(db_mongo_prefix, db_host))

        self.collection = self.client[db_name][col_name]

    def __enter__(self):
        return self

    def __del__(self):
        self.client.close()

    def __exit__(self, *args, **kwargs):
        return self

    def set_no_pagination(self, no_pagination):
        self.no_pagination = no_pagination

    def set_page_num(self, page_num):
        self.page_num = page_num

    def get_all(self, sort=None):
        skips = self.page_size * (self.page_num - 1)

        with self as db:
            if sort:
                return db.collection.find().sort(sort).skip(skips).limit(self.page_size)
            else:
                return db.collection.find().skip(skips).limit(self.page_size)

    def get_all_distinct(self, distinct_field, filter=None, sort=None):
        skips = self.page_size * (self.page_num - 1)

        with self as db:
            pipeline = [
                { "$match" : filter },
                { "$group" : { "_id" : { distinct_field: f"${distinct_field}"} }},
                { "$project" : { distinct_field : f"$_id.{distinct_field}" } },
                { "$sort" : sort },
                { "$skip" : skips },
                { "$limit" : self.page_size }]

            if filter:
                if sort:
                    pipeline = [
                        {"$match": filter},
                        {"$group": {"_id": {distinct_field: f"${distinct_field}"}}},
                        {"$project": {distinct_field: f"$_id.{distinct_field}"}},
                        {"$sort": sort},
                        {"$skip": skips},
                        {"$limit": self.page_size}]
                else:
                    pipeline = [
                        {"$match": filter},
                        {"$group": {"_id": {distinct_field: f"${distinct_field}"}}},
                        {"$project": {distinct_field: f"$_id.{distinct_field}"}},
                        {"$skip": skips},
                        {"$limit": self.page_size}]
            else:
                pipeline = [
                    {"$group": {"_id": {distinct_field: f"${distinct_field}"}}},
                    {"$project": {distinct_field: f"$_id.{distinct_field}"}},
                    {"$skip": skips},
                    {"$limit": self.page_size}]

            return list(db.collection.aggregate(pipeline))

    def get_all_by_filter(self, filter, sort=None):
        with self as db:
            col = None
            if sort:
                col = db.collection.find(filter).sort(sort)
            else:
                col = db.collection.find(filter)

            if self.no_pagination:
                return col
            else:
                skips = self.page_size * (self.page_num - 1)

                return col.skip(skips).limit(self.page_size)

    def get_by_id(self, id):
        with self as db:
            return db.collection.find_one({ '_id' : ObjectId(id) })

    def get_one_by_filter(self, filter):
        with self as db:
            return db.collection.find_one(filter)

    def count_total(self, filter=None, distinct_field=None):
        with self as db:
            if filter:
                if distinct_field:
                    pipeline = [
                        {"$match": filter},
                        {"$group": {"_id": None, f"COUNT(DISTINCT {distinct_field})": { "$addToSet" : f"${distinct_field}"}}},
                        {"$project": {"COUNT" : {"$size" : f"$COUNT(DISTINCT {distinct_field})"}}}]
                else:
                    pipeline = [
                        {"$match": filter},
                        {"$group": {"_id": None, "COUNT": {"$sum": 1}}}]
            else:
                if distinct_field:
                    pipeline = [
                        {"$group": {"_id": None, f"COUNT(DISTINCT {distinct_field})": { "$addToSet" : f"${distinct_field}"}}},
                        {"$project": {"COUNT" : {"$size" : f"$COUNT(DISTINCT {distinct_field})"}}}]
                else:
                    pipeline = [
                        {"$group": {"_id": None, "COUNT": {"$sum": 1}}}]

            col = list(db.collection.aggregate(pipeline))

            if col:
                return int(col[0]['COUNT'])
            else:
                return 0

    def insert(self, obj):
        with self as db:
            return db.collection.insert(obj)

    def update(self, obj):
        with self as db:
            return db.collection.save(obj)

    def delete(self, id):
        with self as db:
            return db.collection.remove({ '_id' : ObjectId(id) })