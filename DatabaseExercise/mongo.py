#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Qi Wang
Professor: Osama
Course: EC500 C1
Description: Database Exercise - Phase 1

"""
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client["airport"]
collection = db["airports"]
print('Airport dataset records count: ')
print(collection.count())
print('10 Airports information in the United States: ')
cursor = collection.find({'country': 'United States'}).limit(10)
for document in cursor: 
    pprint(document)
print('5 Airports information in Boston: ')
cursor = collection.find({'city': 'Boston'}).limit(5)
for document in cursor: 
    pprint(document)
collection.update({"city": "Boston", "code":"BOS"},{"$set": {"code":"BOS_Updated"}})
cursor = collection.find({'city': 'Boston', 'code':'BOS_Updated'})
for document in cursor: 
    pprint(document)





