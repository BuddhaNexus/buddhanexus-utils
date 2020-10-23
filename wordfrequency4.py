#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
finding the frequency of specific words in texts in the tibetan canon
"""

import re
import os
import json

path = os.environ['HOME']+'/segmented-tibetan/files/'

WORD_PATTERN = r"([pm]a ning|'dod 'gro)"

totalworddict = {}

KANGYUR1 = ["K01", "K02", "K03", "K04", "K05", "K06"]
KANGYUR2 = ["K07", "K08", "K09", "K10", "K11", "K12", "K13"]
TENGYUR1 = ["T01", "T02", "T03", "T04", "T05"]
TENGYUR2 = ["T06", "T07", "T08", "T09", "T10"]
TENGYUR3 = ["T11", "T12", "T13", "T14", "T15", "T16"]

COLLECTION_PATTERN = r"^([A-Z]+[0-9]+)"


def find_category(collectionname):
    category = ''
    if collectionname in KANGYUR1:
        category = 'kangyur1'
    elif collectionname in KANGYUR2:
        category = 'kangyur2'    
    elif collectionname in TENGYUR1:
        category = 'tengyur1'
    elif collectionname in TENGYUR2:
        category = 'tengyur2'
    elif collectionname in TENGYUR3:
        category = 'tengyur3'
    return category


for root, dirs, files in os.walk(path):
    for name in files:
        filetext = open(root+"/"+name).read()
        collectionname = re.search(COLLECTION_PATTERN, name[:-5]).group()
        category = find_category(collectionname)

        jsonobject = json.loads(filetext)
        for item in jsonobject.items():
            cleaneditem = re.sub(r'[+–/]', ' ', item[1])
            if re.search(WORD_PATTERN, cleaneditem):
                cleanedword = re.search(WORD_PATTERN, cleaneditem.strip()).group()
                if cleanedword not in totalworddict: 
                    if category == 'kangyur1':
                        totalworddict[cleanedword] = [1,1,0,0,0,0]
                    elif category == 'kangyur2':
                        totalworddict[cleanedword] = [1,0,1,0,0,0]
                    elif category == 'tengyur1':
                        totalworddict[cleanedword] = [1,0,0,1,0,0]
                    elif category == 'tengyur2':
                        totalworddict[cleanedword] = [1,0,0,0,1,0]
                    elif category == 'tengyur3':
                        totalworddict[cleanedword] = [1,0,0,0,0,1]
                    else:
                        print("cannot find category", category, name)
                else:
                    totalworddict[cleanedword][0] += 1
                    if category == 'kangyur1':
                        totalworddict[cleanedword][1] += 1
                    elif category == 'kangyur2':
                        totalworddict[cleanedword][2] += 1
                    elif category == 'tengyur1':
                        totalworddict[cleanedword][3] += 1
                    elif category == 'tengyur2':
                        totalworddict[cleanedword][4] += 1
                    elif category == 'tengyur3':
                        totalworddict[cleanedword][5] += 1
                    else:
                        print("cannot find category", category, name)

filepath_Out = open('frequency.json','w', encoding='utf8')
filepath_Out.write(json.dumps(totalworddict, ensure_ascii=False, indent=0))

'''
"(.*?)": \[\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5})\n\],
\1,\2\3\4\5\6\7\8
'''