#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
finding the frequency of specific words in texts in the tibetan canon for Kangyur only
"""

import re
import os
import json

path = os.environ['HOME']+'/segmented-tibetan/files/'

# WORD_PATTERN = r"([pm]a ning|'dod 'gro)"

WORD_PATTERN = r"(mtshan gnyis [mp]a)"

totalworddict = {}

COLLECTION_PATTERN = r"^([A-Z]+[0-9]+)"


for root, dirs, files in os.walk(path):
    for name in files:
        filetext = open(root+"/"+name).read()
        collectionname = re.search(COLLECTION_PATTERN, name[:-5]).group()
        category = collectionname

        jsonobject = json.loads(filetext)
        for item in jsonobject.items():
            cleaneditem = re.sub(r'[+–/]', ' ', item[1])
            if re.search(WORD_PATTERN, cleaneditem):
                cleanedword = re.search(WORD_PATTERN, cleaneditem.strip()).group()
                if cleanedword not in totalworddict: 
                    if category.startswith('K'):
                        category_nr = int(category[1:])
                        totalworddict[cleanedword] = [1,0,0,0,0,0,0,0,0,0,0,0,0,0]
                        totalworddict[cleanedword][category_nr] = 1
                else:
                    if category.startswith('K'):
                        category_nr = int(category[1:])
                        totalworddict[cleanedword][0] += 1
                        totalworddict[cleanedword][category_nr] += 1

filepath_Out = open('frequency.json','w', encoding='utf8')
filepath_Out.write(json.dumps(totalworddict, ensure_ascii=False, indent=0))

