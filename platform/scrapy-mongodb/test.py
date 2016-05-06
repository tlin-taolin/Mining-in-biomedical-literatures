# -*- coding: utf-8 -*-
#
# A script that used to test the function of the platform.
#
from pymongo import MongoClient
import datetime

client = MongoClient('mongodb', 27017)

db = client.tododb

if __name__ == "__main__":
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print post_id
    print posts.find_one()
