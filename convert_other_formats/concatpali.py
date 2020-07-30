#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Retrieve list of an and sn suttas and concat them in number sorted order.
For an and sn only.
"""

import re
import os
import json

base_dir = os.environ['HOME']+'/bilara-data/root/pli/ms/sutta/sn'
suttadir = os.environ['HOME']+'/Desktop/bilara-converted/'

collections = {}

# retrieve a list of filenumbers and sort it.
for root, dirs, files in os.walk(base_dir):
    for directory in dirs:
        collections[directory] = []
        outputFile = open(suttadir+directory+'_root-pli-ms.json','w')
        for dirroot, dirdirs, dirfiles in os.walk(base_dir+'/'+directory):
            for file in dirfiles:
                filenumber = re.findall(r"[0-9]+",file)[1]
                collections[directory].append(int(filenumber))
            collections[directory].sort()
            for item in collections[directory]:
                for filename in dirfiles:
                    if re.match(directory+r"\."+str(item)+r'[_\-]',filename):
                        fileIn = open(dirroot+'/'+filename,'r', encoding='utf8').read()
                        jsonobject = json.loads(fileIn)

                        outputFile.write(json.dumps(jsonobject, ensure_ascii=False, indent=2))
        outputFile.close()

