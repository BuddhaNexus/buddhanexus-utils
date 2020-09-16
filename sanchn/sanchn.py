#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
creating chinese - sanskrit language matches from parallels
for neural network training

"""
import os
import re
import json

dhppath = os.environ['HOME']+'/sc-data/html_text/pli/sutta/kn/dhp.html'
t210path = os.environ['HOME']+'/sc-data/html_text/lzh/sutta/lzh-dhp/t210/'
t212path = os.environ['HOME']+'/sc-data/html_text/lzh/sutta/lzh-dhp/t212/'
t213path = os.environ['HOME']+'/sc-data/html_text/lzh/sutta/lzh-dhp/t213/'
uvpath = os.environ['HOME']+'/sc-data/html_text/san/sutta/uv/'
uvkgpath = os.environ['HOME']+'/sc-data/html_text/xct/sutta/uv-kg/'

parallelpath = os.environ['HOME']+'/sc-data/relationship/parallels.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/sanchn/'

def removehtml(line):
    # removes html code from the line
    cleanline = re.sub(r'<span class="metre">.*?<br></span>','',line)
    cleanline = re.sub(r'<.*?>','',cleanline)
    cleanline = cleanline.replace('  ',' ')
    return cleanline.replace('\n','').strip().lower()

def retrieve_dictionary_single(path, regex_string, prefix):
    inputfile = open(path,'r', encoding='utf8')
    outputdict = {}
    for line in inputfile:
        idnumber = re.search(regex_string, line)
        if idnumber:
            outputdict[prefix+idnumber.group()] = removehtml(line)
    return outputdict

def retrieve_dictionary_multiple(path, regex_string):
    outputdict = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            file = open(root+'/'+name,'r', encoding='utf8')

            for line in file:
                number = re.search(regex_string, line)
                if number:
                    if not ". . . ." in line:
                        outputdict[name[:-5]+'#'+number.group().strip('"')] = removehtml(line)
    return outputdict


# retrieving dhp and uv lines and numbers
dhpdict = retrieve_dictionary_single(dhppath, 'dhp([0-9]+)', '')
t210dict = retrieve_dictionary_multiple(t210path, 'vgns([0-9]+\.[0-9]+[A-B]*)')
t212dict = retrieve_dictionary_multiple(t212path, 'vgns([0-9]+\.[0-9]+[A-B]*)')
t213dict = retrieve_dictionary_multiple(t213path, 'vgns([0-9]+\.[0-9]+[A-B]*)')
uvdict = retrieve_dictionary_multiple(uvpath, '([0-9]+\.[0-9]+[A-Z]*)')
uvkgdict = retrieve_dictionary_multiple(uvkgpath, '"([0-9]+)"')

chndict = {**t210dict, **t212dict, **t213dict}

# temp. writing data to file. This code can be commented out after done once.
# outputpmfile = open(outputpath+'chn.json','w', encoding='utf8')
# outputpmfile.write('[\n')
# outputpmfile.write(json.dumps(chndict, ensure_ascii=False, indent=2))
# outputpmfile.write('\n]')
# outputpmfile.close()

# outputpmfile = open(outputpath+'uvkg.json','w', encoding='utf8')
# outputpmfile.write('[\n')
# outputpmfile.write(json.dumps(uvkgdict, ensure_ascii=False, indent=2))
# outputpmfile.write('\n]')
# outputpmfile.close()

# retrieving data from the parallels file.
parallelfile = open(parallelpath,'r', encoding='utf8').read()
outputparallelfile = open(outputpath+'parallel2.json','w', encoding='utf8')
outputparallelfile.write('[\n')

paralleljson = json.loads(parallelfile)
for parallel in paralleljson:
    try:
        dhpnr = re.compile('^dhp[0-9]+')
        t210nr = re.compile('^t210\.[0-9]+#vgns[0-9]+\.[0-9]+[A-B]*')
        t212nr = re.compile('^t212\.[0-9]+#vgns[0-9]+\.[0-9]+[A-B]*')
        t213nr = re.compile('^t213\.[0-9]+#vgns[0-9]+\.[0-9]+[A-B]*')
        uvnr = re.compile('^uv[0-9]+#[0-9]+\.[0-9]+[A-Z]*')
        uvkgnr = re.compile('^uv-kg[0-9]+#[0-9]+[A-Z]*')
        paralleldict = {}

        if any(dhpnr.match(x) for x in parallel["parallels"]) and any(uvnr.match(y) for y in parallel["parallels"]):
            dhpuvparallel = []
            for item in parallel["parallels"]:
                if dhpnr.match(item) or uvnr.match(item):
                    dhpuvparallel.append(item)
            dhpuvparallel = sorted(dhpuvparallel)
            if len(dhpuvparallel[0].split("-")) == 1:
                paralleldict[dhpuvparallel[1]] = uvdict[dhpuvparallel[1]]
                paralleldict[dhpuvparallel[0]] = dhpdict[dhpuvparallel[0]]

        if any(uvkgnr.match(x) for x in parallel["parallels"]) and any(uvnr.match(y) for y in parallel["parallels"]):
            uvkguvparallel = []
            for item in parallel["parallels"]:
                if uvkgnr.match(item) or uvnr.match(item):
                    uvkguvparallel.append(item)
            uvkguvparallel = sorted(uvkguvparallel)
            if len(uvkguvparallel[0].split("-#")) == 1:
                paralleldict[uvkguvparallel[1]] = uvdict[uvkguvparallel[1]]
                paralleldict[uvkguvparallel[0]] = uvkgdict[uvkguvparallel[0]]

        if any(uvnr.match(x) for x in parallel["parallels"]) and any(t210nr.match(y) for y in parallel["parallels"]):
            t210uvparallel = []
            for item in parallel["parallels"]:
                if t210nr.match(item) or uvnr.match(item):
                    t210uvparallel.append(item)
            t210uvparallel = sorted(t210uvparallel)
            if len(t210uvparallel[0].split("-#")) == 1:
                paralleldict[t210uvparallel[1]] = uvdict[t210uvparallel[1]]
                paralleldict[t210uvparallel[0]] = t210dict[t210uvparallel[0]]

        if any(uvnr.match(x) for x in parallel["parallels"]) and any(t212nr.match(y) for y in parallel["parallels"]):
            t212uvparallel = []
            for item in parallel["parallels"]:
                if t212nr.match(item) or uvnr.match(item):
                    t212uvparallel.append(item)
            t212uvparallel = sorted(t212uvparallel)
            if len(t212uvparallel[0].split("-#")) == 1:
                paralleldict[t212uvparallel[1]] = uvdict[t212uvparallel[1]]
                paralleldict[t212uvparallel[0]] = t212dict[t212uvparallel[0]]

        if any(uvnr.match(x) for x in parallel["parallels"]) and any(t213nr.match(y) for y in parallel["parallels"]):
            t213uvparallel = []
            for item in parallel["parallels"]:
                if t213nr.match(item) or uvnr.match(item):
                    t213uvparallel.append(item)
            t213uvparallel = sorted(t213uvparallel)
            if len(t213uvparallel[0].split("-#")) == 1:
                paralleldict[t213uvparallel[1]] = uvdict[t213uvparallel[1]]
                paralleldict[t213uvparallel[0]] = t213dict[t213uvparallel[0]]

        if paralleldict:
            outputparallelfile.write(json.dumps(paralleldict, ensure_ascii=False, indent=2))
            outputparallelfile.write(',\n')

    except:
        continue

outputparallelfile.write('\n]')
outputparallelfile.close()


