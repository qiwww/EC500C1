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
# Create a MongoClient to the running mongod instance
client = MongoClient('mongodb://localhost:27017/')
# Switch to the airport DB
db = client["airport"]
# Go into airports collection
collection = db["airports"]
# Get airport dataset records count
print('Airport dataset records count: ')
print(collection.count())
# Use find and limit to display 10 airports in the U.S.
print('10 Airports information in the United States: ')
cursor = collection.find({'country': 'United States'}).limit(10)
for document in cursor: 
    pprint(document)
# Use find and limit to display 5 airports in Boston
print('5 Airports information in Boston: ')
cursor = collection.find({'city': 'Boston'}).limit(5)
for document in cursor: 
    pprint(document)
# Use update to change one airport information
collection.update({"city": "Boston", "code":"BOS"},{"$set": {"code":"BOS_Updated"}})
# Display the updated airport information
cursor = collection.find({'city': 'Boston', 'code':'BOS_Updated'})
for document in cursor: 
    pprint(document)





