#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday 18-July-2019

@author: BenGfoyle - github.com/bengfoyle
@overview: This program will convert a csv file to json file
"""

import csv, json
#Using pprint for making the output more readable.
from pprint import pprint
import pandas as pd

#warning about overwriting files
print("This program will create a json file based off a csv. Please note if\
the there already exists a json file with the same name as the csv\
that json file will be overwritten!\n")

#filename
filename = input("Enter the filename of the csv you would like to convert:")

csvFilePath = filename + ".csv"
jsonFilePath = filename + ".json"

def CSV_To_JSON(x):
    #read csv file and add data
    data = {}
    with open(csvFilePath) as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            id = rows[x]
            data[id] = rows

    #create new json file and write data
    with open(jsonFilePath, 'w') as jsonFile:
        #beautify
        jsonFile.write(json.dumps(data, indent = 4))
        print("A new file ",filename+".json should be in the current directory")

def JSON_To_CSV():
    df = pd.read_json(jsonFilePath)
    df.to_csv(csvFilePath)
    print("A new file ",filename+".csv should be in the current directory")

x = input("Enter unique column ID")
CSV_To_JSON(x)
