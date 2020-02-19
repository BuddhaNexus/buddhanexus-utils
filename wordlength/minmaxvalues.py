#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Calculating minumum and maximum values and average total values of the AWL for each collection dependent on file values

"""
import os
import re
import json

# collections = ["dn","mn","sn","an","kp","dhp","ud","iti","snp","vv","pv","thag","thig","tha-ap","thi-ap","bv","cp","ja","mnd","cnd","ps","ne","pe","mil","pli-tv-bu-pm","pli-tv-bi-pm","pli-tv-bu-vb","pli-tv-bi-vb","pli-tv-kd","pli-tv-pvr","ds","vb","dt","pp","kv","ya","patthana","atk-s","atk-vin","atk-abh","tika-s","tika-vin","tika-abh","anya-e"]
collections = ["vb","ya"]
filedatapath = os.environ['HOME']+'/buddhanexus-utils/wordlength/filesdata.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/wordlength/'

# retrieving data from the filedata file.
filedata = json.loads(open(filedatapath,'r', encoding='utf8').read())
outputdata = open(outputpath+'minmax.csv','w', encoding='utf8')

for collection in collections:
    minvalue = 10
    maxvalue = 0
    totalvalue = 0
    counter = 1
    for key,value in filedata.items():
        if re.search(r"^"+collection+r"[0-9-]", key):
            if value > maxvalue:
                maxvalue = value
            if value < minvalue:
                minvalue = value
            totalvalue += value
            counter += 1

    if counter > 1:  
        outputdata.write(collection+","+str(minvalue)+","+str(maxvalue)+","+str(totalvalue/(counter-1))+"\n")

outputdata.close()

