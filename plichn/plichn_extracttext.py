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

for parallel in paralleljson:
    for item in parallel:
        if pali_regex.match(item):
            newpath = outputpath+item
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                os.makedirs(newpath+'/partial')
                break
            # else:
            #     print(item," folder exists")

    for item in parallel:
        sutta = item.strip('~')
        if pali_regex.match(item):
            for root, dirs, files in os.walk(palifilespath):
                for name in files:
                    if name[:-17] == sutta:
                        filetext = open(root+"/"+name).read()
                        outputfile = open(newpath+'/'+sutta+'.json','w', encoding='utf8')
                        outputfile.write(filetext)
                        outputfile.close()

        if chn_regex.match(sutta):
            if sutta.startswith('t'):
                for root, dirs, files in os.walk(chinesefilespath2):
                    for name in files:
                        name_nr = re.findall('(?<=n)[0-9]+[a-hA-H]*(?=_)', name)[0]
                        while name_nr[0] == '0':
                            name_nr = name_nr[1:]
                        if name.startswith('T') and name_nr == sutta[1:].split('.')[0]:
                            filetext = open(root+"/"+name).read()
                            if item.startswith('~') or len(sutta[1:].split('.')) > 1:
                                outputfile = open(newpath+'/partial/'+name,'w', encoding='utf8')
                            else:
                                outputfile = open(newpath+'/'+name,'w', encoding='utf8')
                            outputfile.write(filetext)
                            outputfile.close()
            else: 
                if item.startswith('~'):
                    outputfile = open(newpath+'/partial/'+sutta+'.json','w', encoding='utf8')
                else:
                    outputfile = open(newpath+'/'+sutta+'.json','w', encoding='utf8')

                newsuttajson = {}
                for root, dirs, files in os.walk(chinesefilespath):
                    for name in files:
                        if name[:-5] == sutta:
                            t_list = []
                            filetext = open(root+"/"+name, 'r')
                            for line in filetext:
                                t_nr = re.findall(r't[0-9]+[a-h][0-9]+', line)
                                for nr in t_nr:
                                    t_list.append(nr)

                sutta_collection = re.findall(r'^[msde]a',sutta)[0]

                for root, dirs, files in os.walk(chinesefilespath3+'/'+sutta_collection):
                    for name in files:
                        with open(root+"/"+name) as json_file:
                            data = json.load(json_file)
                            for item in sorted(t_list):
                                segment = name[:-5]+':'+item[1:]
                                if segment in data.keys():
                                    newsuttajson[segment] = data[segment]

                outputfile.write(json.dumps(newsuttajson, ensure_ascii=False, indent=2))
                outputfile.close()
