#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
converts vri xml files to files used in buddhanexus before tokanization.
"""

import re
import os
import json

base_dir = os.environ['HOME']+'/Desktop/cscd/'
suttadir = os.environ['HOME']+'/Desktop/cscd-converted/'

filenames = open(os.environ['HOME']+'/Desktop/filenames.txt','w')

def convert_filename(file):
    fileparts = file.split('.')
    filestart = ''
    if fileparts[0].startswith('e'):
        filestart = 'anya-'
    elif fileparts[1].startswith('att'):
        filestart = 'atk-'
    elif fileparts[1].startswith('tik') or fileparts[0].endswith('t'):
        filestart = 'tika-'
    elif fileparts[1].startswith('nrf'):
        filestart = 'tika-'
    else:
        print("file not found: ", file)
    filename = filestart+fileparts[0]+fileparts[1][3:]
    filenames.write(filename+'\n')
    return filename

countomitted = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if re.search(r"toc",file):
            countomitted += 1
            continue
        elif re.search(r"mul",file) and not file.startswith('e'):
            countomitted += 1
            continue
        elif re.search(r"518m|520m",file):
            countomitted += 1
            continue
        else:
            fileIn = open(base_dir+file,'r', encoding='utf16')
            filename = convert_filename(file)
            fileOut = open(suttadir+filename+'_root-pli-ms.json','w', encoding='utf8')
            counter = 0
            jsonobject = {}
            for line in fileIn:
                if not line.startswith('<p rend='):
                    continue
                else:
                    line = re.sub(r'<.*?>','',line)
                    line = re.sub(r'\n','',line)
                    line = re.sub(r'  ',' ',line)
                    jsonobject[filename+':'+str(counter)] = line
                    counter += 1

            fileOut.write(json.dumps(jsonobject, ensure_ascii=False, indent=2))
            fileOut.close()

filenames.close()
print(countomitted)
