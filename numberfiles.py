#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Numbers all files in file-jsons data directory.

"""
import os
import re
import json

base_dir = os.environ['HOME']+'/buddhanexus/data/'
filename = 'pli-files.json'
fileIn = open(base_dir+filename,'r', encoding='utf8').read()
jsonobject = json.loads(fileIn)

fileOut = open('numbered_'+filename,'w', encoding='utf8')
fileOut.write('[\n')
counter = 1
for item in jsonobject:
    item['filenr'] = counter
    fileOut.write(json.dumps(item, ensure_ascii=False, indent=2))
    fileOut.write(',\n')
    counter = counter + 1

fileOut.write(']\n')