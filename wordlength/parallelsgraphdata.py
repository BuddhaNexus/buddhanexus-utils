#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
creating graph data for numbers of parallels of indicated collections

"""
import os
import re
import json

parallelpath = os.environ['HOME']+'/sc-data/relationship/parallels.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/wordlength/'

# retrieving data from the parallels file.
parallelfile = open(parallelpath,'r', encoding='utf8').read()
outputparallelfile = open(outputpath+'parallel.json','w', encoding='utf8')

paralleljson = json.loads(parallelfile)
collectiondict = {}

# change the regex according to the criteria you want to search on
collectionnr = re.compile('^ja[0-9]+')
totalrange = 547

for parallel in paralleljson:
    try:

        if any(collectionnr.match(x) for x in parallel["parallels"]):
            for item in parallel["parallels"]:
                if collectionnr.match(item):
                    itemnumber = item.split('#')[0]
                    if itemnumber in collectiondict.keys():
                        collectiondict[itemnumber] += len(parallel["parallels"])-1
                    else:
                        collectiondict[itemnumber] = len(parallel["parallels"])-1
    except:
        continue

for parallel in paralleljson:
    try:
        if any(collectionnr.match(x) for x in parallel["mentions"]):
            for item in parallel["mentions"]:
                if collectionnr.match(item):
                    itemnumber = item.split('#')[0]
                    if itemnumber in collectiondict.keys():
                        collectiondict[itemnumber] += len(parallel["mentions"])-1
                    else:
                        collectiondict[itemnumber] = len(parallel["mentions"])-1
    except:
        continue

for parallel in paralleljson:
    try:
        if any(collectionnr.match(x) for x in parallel["retells"]):
            for item in parallel["retells"]:
                if collectionnr.match(item):
                    itemnumber = item.split('#')[0]
                    if itemnumber in collectiondict.keys():
                        collectiondict[itemnumber] += len(parallel["retells"])-1
                    else:
                        collectiondict[itemnumber] = len(parallel["retells"])-1
    except:
        continue

# add 0 where there is no parallel and sort numbers.
newcollectiondict = {}
for i in range(totalrange):
    if "ja"+str(i+1) in collectiondict.keys():
        newcollectiondict["ja"+str(i+1)] = collectiondict["ja"+str(i+1)]
    else:
        newcollectiondict["ja"+str(i+1)] = 0


outputparallelfile.write(json.dumps(newcollectiondict, ensure_ascii=False, indent=2))
outputparallelfile.write(',\n')
outputparallelfile.close()

