#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
creating a list of parallels between Sanskrit and Pali from SC parallels list
"""
import os
import re
import json

parallelpath = os.environ['HOME']+'/sc-data/relationship/parallels.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/sanpli/'


# retrieving data from the parallels file.
parallelfile = open(parallelpath,'r', encoding='utf8').read()
outputparallelfile = open(outputpath+'plisanchn_parallel_list.json','w', encoding='utf8')

parallelfulllist = []
paralleljson = json.loads(parallelfile)

pali_regex = re.compile('^[md]n[0-9]+|^[sa]n[0-9]+\.[0-9]+|^mil[0-9\.]+')
# pali_regex = re.compile('^[md]n[0-9]+')
san_regex = re.compile('^arv[0-9]+|^avs[0-9]+|^divy[0-9]+|^lal[0-9]+|^mkv[0-9]+|^sf[0-9]+|^sag|^sbh')
chn_regex = re.compile('^[mds]a[0-9]+|^t[0-9]+[a-z1-9\.]*|^[es]a-[2-3]\.[0-9]+|ea[0-9]+\.[0-9]+')

for parallel in paralleljson:
    try:
        if any(pali_regex.match(x) for x in parallel["parallels"]) and any(san_regex.match(y) for y in parallel["parallels"]):
            parallellist = []
            for item in parallel["parallels"]:
                if '#' not in item:
                    parallellist.append(item)
            if len(parallellist) >= 2 and any(pali_regex.match(x) for x in parallellist) and any(san_regex.match(y) for y in parallellist):
                parallelfulllist.append(parallellist)
    except:
        continue

    try:
        if any(pali_regex.match(x) for x in parallel["parallels"]) and any(chn_regex.match(y) for y in parallel["parallels"]):
            parallellist = []
            for item in parallel["parallels"]:
                if '#' not in item:
                    parallellist.append(item)
            if len(parallellist) >= 2 and any(pali_regex.match(x) for x in parallellist) and any(chn_regex.match(y) for y in parallellist):
                parallelfulllist.append(parallellist)
    except:
        continue


outputparallelfile.write(json.dumps(parallelfulllist, ensure_ascii=False, indent=2))

outputparallelfile.close()


