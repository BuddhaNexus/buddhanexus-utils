#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Extract a list of chinese cbeta collections for input in the html extraction database.
"""
import re
import os
import json
# import asciicodes

path = os.environ['HOME']+'/buddhanexus-utils/cbeta_collections/'
base_dir = os.environ['HOME']+'/buddhanexus/data/'
collectionsfile = open('chn-categories.json','w', encoding='utf8')

fileCatIn = open(base_dir+'chn-categories.json','r', encoding='utf8').read()
jsoncatobject = json.loads(fileCatIn)

collectionsfile.write('[\n')

for root, dirs, files in os.walk(path):
    for name in sorted(files):
        collections = {}
        totalfiles = open(root+name,'r', encoding='utf8').read()
        files = re.findall(r"href='([TX][0-9][0-9]n[0-9][0-9][0-9][0-9a-zA-Z]+)", totalfiles)
        collections["category"] = name[:-5]
        
        for item in jsoncatobject:
            if item["category"] == name[:-5]:
                collections["categoryname"] = item["categoryname"]

        collections["files"] = files

        collectionsfile.write(json.dumps(collections, ensure_ascii=False, indent=2))
        collectionsfile.write(",\n")

collectionsfile.write(']\n')
collectionsfile.close()
