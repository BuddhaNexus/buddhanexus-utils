#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Adds files from ***-files.json to categories where none exists.

"""
import os
import re
import json

base_dir = os.environ['HOME']+'/buddhanexus/data/'
catname = 'tib-categories.json'
filename = 'tib-files.json'
fileCatIn = open(base_dir+catname,'r', encoding='utf8').read()
jsoncatobject = json.loads(fileCatIn)

fileFileIn = open(base_dir+filename,'r', encoding='utf8').read()
jsonfileobject = json.loads(fileFileIn)

fileOut = open('filesadded_'+catname,'w', encoding='utf8')
fileOut.write('[\n')

for item in jsoncatobject:
    filelist = []
    for file in jsonfileobject:
        if file['category'] == item['category']:
            filelist.append(file['filename'])
    item["files"] = filelist
    fileOut.write(json.dumps(item, ensure_ascii=False, indent=2))
    fileOut.write(',\n')

fileOut.write(']\n')