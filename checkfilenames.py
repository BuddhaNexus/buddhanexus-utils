#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Checks a list of filenames against the lang-files.json to make sure they are all in.

"""
import os
import re
import json

# base_dir = os.environ['HOME']+'/buddhanexus/data/'
# filename = 'chn-files.json'
base_dir = os.environ['HOME']+'/buddhanexus-utils/sanskrit_data/'
filename = 'skt-files_new.json'
filenameslist = os.environ['HOME']+'/Desktop/filelist.json'

filenamesjsonobject = []
files_dir = os.environ['HOME']+'/Desktop/convertbilara/outputfiles/'
for root, dirs, files in os.walk(files_dir):
		for file in files:
			filenamesjsonobject.append(file[:-4])

fileIn = open(base_dir+filename,'r', encoding='utf8').read()
fileobject = json.loads(fileIn)

filenamesIn = open(filenameslist,'r', encoding='utf8').read()
filenamesjsonobject = json.loads(filenamesIn)

fileslist = []
fileOut = open('errors_'+filename,'w', encoding='utf8')
fileOut.write('// Files mentioned in the lists but no json file found on server\n[\n')

for item in fileobject:
    fileslist.append(item['filename'])
    if item['filename'] not in filenamesjsonobject:
        fileOut.write(json.dumps(item['filename'], ensure_ascii=False, indent=2))
        fileOut.write(",\n")

fileOut.write(']\n// JSON files found on server but not mentioned in the lists \n[\n')

for item in filenamesjsonobject:
    if item not in fileslist:
        fileOut.write(json.dumps(item, ensure_ascii=False, indent=2))
        fileOut.write(",\n")

fileOut.write(']\n')