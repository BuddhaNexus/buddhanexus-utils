#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
finding the frequency of specific words in texts in the sanskrit canon
"""

import re
import os
import json

path = os.environ['HOME']+'/segmented-sanskrit/segmented_files/'
# path = './palitest/'

# WORD_PATTERN = r"([UuoO]bhaya[bv]ya.jana)"
WORD_PATTERN = r"(liṅga)"

totalworddict = {}


COLLECTION_PATTERN = r"^([A-Z]+[0-9]+|XX|OT)"


def find_category(collectionname):
    category = ''
    if collectionname.startswith('SA'):
        category = 'sastrapitaka'
    elif collectionname.startswith('V'):
        category = 'vinaya'
    elif collectionname.startswith('S'):
        category = 'sutra'    
    elif collectionname.startswith('XX'):
        category = 'buddhist'
    elif collectionname.startswith('GV'):
        category = 'veda'
    elif collectionname.startswith('GE'):
        category = 'epic'
    elif collectionname.startswith('GP'):
        category = 'purana'
    elif collectionname.startswith('GR'):
        category = 'rellit'
    elif collectionname.startswith('GK'):
        category = 'poetry'
    elif collectionname.startswith('GS'):
        category = 'sastra'
    return category


for root, dirs, files in os.walk(path):
    for name in files:
        filetext = open(root+"/"+name).read()
        collectionname = re.search(COLLECTION_PATTERN, name[:-5]).group()
        category = find_category(collectionname)

        jsonobject = json.loads(filetext)
        for item in jsonobject.items():
            cleaneditem = re.sub(r'[+–/]', ' ', item[1])
            wordlist = cleaneditem.strip().split(' ')
            for word in wordlist:
                if re.search(WORD_PATTERN, word):
                    cleanedword = re.sub(r'[\*\(\).?!|:;—\-…“‘,_0-9]', '', word)
                    cleanedword = re.sub(r'[’”]ti', '', cleanedword)
                    cleanedword = re.sub(r'[’”]', '', cleanedword)
                    cleanedword = cleanedword.lower()
                    if cleanedword not in totalworddict: 
                        if category == 'sutra':
                            totalworddict[cleanedword] = [1,1,0,0,0,0,0,0,0,0,0]
                        elif category == 'vinaya':
                            totalworddict[cleanedword] = [1,0,1,0,0,0,0,0,0,0,0]
                        elif category == 'sastrapitaka':
                            totalworddict[cleanedword] = [1,0,0,1,0,0,0,0,0,0,0]
                        elif category == 'buddhist':
                            totalworddict[cleanedword] = [1,0,0,0,1,0,0,0,0,0,0]
                        elif category == 'veda':
                            totalworddict[cleanedword] = [1,0,0,0,0,1,0,0,0,0,0]
                        elif category == 'epic':
                            totalworddict[cleanedword] = [1,0,0,0,0,0,1,0,0,0,0]
                        elif category == 'purana':
                            totalworddict[cleanedword] = [1,0,0,0,0,0,0,1,0,0,0]
                        elif category == 'rellit':
                            totalworddict[cleanedword] = [1,0,0,0,0,0,0,0,1,0,0]
                        elif category == 'poetry':
                            totalworddict[cleanedword] = [1,0,0,0,0,0,0,0,0,1,0]
                        elif category == 'sastra':
                            totalworddict[cleanedword] = [1,0,0,0,0,0,0,0,0,0,1]
                        else:
                            print("cannot find category", category, name)
                    else:
                        totalworddict[cleanedword][0] += 1
                        if category == 'sutra':
                            totalworddict[cleanedword][1] += 1
                        elif category == 'vinaya':
                            totalworddict[cleanedword][2] += 1
                        elif category == 'sastrapitaka':
                            totalworddict[cleanedword][3] += 1
                        elif category == 'buddhist':
                            totalworddict[cleanedword][4] += 1
                        elif category == 'veda':
                            totalworddict[cleanedword][5] += 1
                        elif category == 'epic':
                            totalworddict[cleanedword][6] += 1
                        elif category == 'purana':
                            totalworddict[cleanedword][7] += 1
                        elif category == 'rellit':
                            totalworddict[cleanedword][8] += 1
                        elif category == 'poetry':
                            totalworddict[cleanedword][9] += 1
                        elif category == 'sastra':
                            totalworddict[cleanedword][10] += 1
                        else:
                            print("cannot find category", category, name)

filepath_Out = open('frequency.json','w', encoding='utf8')
filepath_Out.write(json.dumps(totalworddict, ensure_ascii=False, indent=0))

'''
"(.*?)": \[\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5})\n\],
\1,\2\3\4\5\6\7\8
'''