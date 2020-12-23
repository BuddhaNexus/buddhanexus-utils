#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
From the parallellist created with plichn.py, extract the various pali and chinese texts and make them into a folder
"""
import os
import re
import json

parallelpath = os.environ['HOME']+'/buddhanexus-utils/plichn/plichn_parallel_list.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/plichn/files/'

# retrieving data from the parallels file.
parallelfile = open(parallelpath,'r', encoding='utf8').read()
paralleljson = json.loads(parallelfile)

# pali_regex = re.compile('^[md]n[0-9]+|^[sa]n[0-9]+\.[0-9]+')
pali_regex = re.compile('^[md]n[0-9]+')
chn_regex = re.compile('^[mds]a[0-9]+|^t[0-9]+[a-z1-9\.]*|^[es]a-[2-3]\.[0-9]+|ea[0-9]+\.[0-9]+')

palifilespath = os.environ['HOME']+'/segmented-pali/inputfiles/'
chinesefilespath = os.environ['HOME']+'/sc-data/html_text/lzh/sutta/'
chinesefilespath2 = os.environ['HOME']+'/segmented-chinese/files/'
chinesefilespath3 = os.environ['HOME']+'/buddhanexus-utils/chn_files/'

t_list = [
  "t0001a01",
  "t0001a02",
  "t0001a03",
  "t0001a04",
  "t0001a05"]

for root, dirs, files in os.walk(chinesefilespath3+'/da'):
    for name in files:
        with open(root+"/"+name) as json_file:
            data = json.load(json_file)
            for item in t_list:

                if name[:-5]+':'+item[1:] in data.keys():
                    print(data[name[:-5]+':'+item[1:]])





            
