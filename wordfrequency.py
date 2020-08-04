#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
finding the frequency of long words in the pali texts
"""

import re
import os
import json

path = os.environ['HOME']+'/segmented-pali/inputfiles/'
# path = './palitest/'

WORDLENGTH = 40

totalworddict = {}

SUTTAS_EARLY = [
      "dn",
      "mn",
      "sn",
      "an",    
      "kp",
      "dhp",
      "ud",
      "iti",
      "snp",
      "thag",
      "thig"]

SUTTAS_LATE = [
      "vv",
      "pv",
      "tha-ap",
      "thi-ap",
      "bv",
      "cp",
      "ja",
      "mnd",
      "cnd",
      "ps",
      "ne",
      "pe",
      "mil"]

ABHIDHAMMA = ["ds", "vb", "dt", "pp", "kv", "ya", "patthana"]

COMMENTARIES = ["atk-s", "atk-vin", "atk-abh", "tika-s", "tika-vin", "tika-abh", "anya-e"]

COLLECTION_PATTERN = r"^(pli-tv-b[ui]-vb|[a-z\-]+)"


def find_category(collectionname):
    category = ''
    if collectionname.startswith('pli'):
        category = 'vinaya'
    elif collectionname in SUTTAS_EARLY:
        category = 'suttas_early'
    elif collectionname in SUTTAS_LATE:
        category = 'suttas_late'    
    elif collectionname in ABHIDHAMMA:
        category = 'abhidhamma'
    elif collectionname in COMMENTARIES:
        category = 'commentaries'
    return category


for root, dirs, files in os.walk(path):
    for name in files:
        filetext = open(root+"/"+name).read()
        collectionname = re.search(COLLECTION_PATTERN, name[:-17]).group()
        category = find_category(collectionname)

        jsonobject = json.loads(filetext)
        for item in jsonobject.items():
            cleaneditem = re.sub(r'[+–]', ' ', item[1])
            wordlist = cleaneditem.strip().split(' ')
            for word in wordlist:
                if len(word) > WORDLENGTH:
                    cleanedword = re.sub(r'[\*\(\).?!|:;—\-…“‘,_0-9]', '', word)
                    cleanedword = re.sub(r'[’”]ti', '', cleanedword)
                    cleanedword = re.sub(r'[’”]', '', cleanedword)
                    cleanedword = cleanedword.lower()
                    word_length = len(cleanedword)
                    if word_length > WORDLENGTH:
                        if cleanedword not in totalworddict: 
                            if category == 'suttas_early':
                                totalworddict[cleanedword] = [word_length,1,1,0,0,0,0]
                            elif category == 'suttas_late':
                                totalworddict[cleanedword] = [word_length,1,0,1,0,0,0]
                            elif category == 'vinaya':
                                totalworddict[cleanedword] = [word_length,1,0,0,1,0,0]
                            elif category == 'abhidhamma':
                                totalworddict[cleanedword] = [word_length,1,0,0,0,1,0]
                            elif category == 'commentaries':
                                totalworddict[cleanedword] = [word_length,1,0,0,0,0,1]
                            else:
                                print("cannot find category", category)
                        else:
                            totalworddict[cleanedword][1] += 1
                            if category == 'suttas_early':
                                totalworddict[cleanedword][2] += 1
                            elif category == 'suttas_late':
                                totalworddict[cleanedword][3] += 1
                            elif category == 'vinaya':
                                totalworddict[cleanedword][4] += 1
                            elif category == 'abhidhamma':
                                totalworddict[cleanedword][5] += 1
                            elif category == 'commentaries':
                                totalworddict[cleanedword][6] += 1
                            else:
                                print("cannot find category", category)

filepath_Out = open('frequency.json','w', encoding='utf8')
filepath_Out.write(json.dumps(totalworddict, ensure_ascii=False, indent=0))

'''
"(.*?)": \[\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5},)\n(\d{1,5})\n\],
\1,\2\3\4\5\6\7\8
'''