#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
creating sanskrit - pali language matches from parallels
for neural network training

"""
import os
import re
import json

dhppath = os.environ['HOME']+'/sc-data/html_text/pli/sutta/kn/dhp.html'
sagpath = os.environ['HOME']+'/sc-data/html_text/san/sutta/ybs/sag.html'
uvpath = os.environ['HOME']+'/sc-data/html_text/san/sutta/uv/'
pmpath = os.environ['HOME']+'/sc-data/html_text/pli/vinaya/pli-tv-bu-pm.html'
sanpmpath = os.environ['HOME']+'/sc-data/html_text/san/vinaya/san-lo-bu-pm.html'

parallelpath = os.environ['HOME']+'/sc-data/relationship/parallels.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/sanpli/'

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
                        outputdict[name[:-5]+'#'+number.group()] = removehtml(line)
    return outputdict


# retrieving sag, dhp and uv lines and numbers
sagdict = retrieve_dictionary_single(sagpath, 'sag([0-9]+\.*[0-9]*)', '')
dhpdict = retrieve_dictionary_single(dhppath, 'dhp([0-9]+)', '')
uvdict = retrieve_dictionary_multiple(uvpath, '([0-9]+\.[0-9]+[A-Z]*)')
pmdict = retrieve_dictionary_single(pmpath, '[a-z][a-z][0-9]+', 'pli-tv-bu-pm-')
sanpmdict = retrieve_dictionary_single(sanpmpath, '[a-fh-z][a-z][0-9]+', 'san-lo-bu-pm-')

# temp. writing data to file. This code can be commented out after done once.
# outputpmfile = open(outputpath+'pm.json','w', encoding='utf8')
# outputpmfile.write('[\n')
# outputpmfile.write(json.dumps(pmdict, ensure_ascii=False, indent=2))
# outputpmfile.write('\n]')
# outputpmfile.close()

# outputsanpmfile = open(outputpath+'sanpm.json','w', encoding='utf8')
# outputsanpmfile.write('[\n')
# outputsanpmfile.write(json.dumps(sanpmdict, ensure_ascii=False, indent=2))
# outputsanpmfile.write('\n]')
# outputsanpmfile.close()

# retrieving data from the parallels file.
parallelfile = open(parallelpath,'r', encoding='utf8').read()
outputparallelfile = open(outputpath+'parallel.json','w', encoding='utf8')
outputparallelfile.write('[\n')

outputsanfile = open(outputpath+'san.json','w', encoding='utf8')
outputsanfile.write('[\n')

paralleljson = json.loads(parallelfile)
for parallel in paralleljson:
    try:
        dhpnr = re.compile('^dhp[0-9]+')
        uvnr = re.compile('^uv[0-9]+#[0-9]+\.[0-9]+[A-Z]*')
        if any(dhpnr.match(x) for x in parallel["parallels"]) and any(uvnr.match(y) for y in parallel["parallels"]):
            dhpuvparallel = []
            paralleldict = {}
            for item in parallel["parallels"]:
                if dhpnr.match(item) or uvnr.match(item):
                    dhpuvparallel.append(item)
            dhpuvparallel = sorted(dhpuvparallel)
            paralleldict["pli"] = dhpdict[dhpuvparallel[0]]
            paralleldict["skt"] = uvdict[dhpuvparallel[1]]
            outputparallelfile.write(json.dumps(paralleldict, ensure_ascii=False, indent=2))
            outputparallelfile.write(',\n')

        sagnr = re.compile('^sag#[0-9]+\.[0-9]+$')
        if any(sagnr.match(x) for x in parallel["parallels"]):
            for item in parallel["parallels"]:
                paralleldict = {}
                if sagnr.match(item):
                    item = item.replace('#','')
                    paralleldict["pli"] = ""
                    paralleldict["skt"] = sagdict[item]
                    paralleldict["matches"] = parallel["parallels"]
                    outputsanfile.write(json.dumps(paralleldict, ensure_ascii=False, indent=2))
                    outputsanfile.write(',\n')

        sannr = re.compile('^arv|^avs|^divy|^lal|^mkv|^sf|^san-')
        if any(sannr.match(x) for x in parallel["parallels"]):
            paralleldict["pli"] = ""
            paralleldict["skt"] = ""
            paralleldict["matches"] = parallel["parallels"]
            outputsanfile.write(json.dumps(paralleldict, ensure_ascii=False, indent=2))
            outputsanfile.write(',\n')

        pmnr = re.compile('^pli-tv-bu-pm-[a-z]+[0-9]+')
        sanpmnr = re.compile('^san-lo-bu-pm-[a-z]+[0-9]+')
        if any(pmnr.match(x) for x in parallel["parallels"]) and any(sanpmnr.match(y) for y in parallel["parallels"]):
            plisanpmparallel = []
            paralleldict = {}
            for item in parallel["parallels"]:
                if pmnr.match(item) or sanpmnr.match(item):
                    plisanpmparallel.append(item)
            plisanpmparallel = sorted(plisanpmparallel)
            paralleldict["pli"] = pmdict[plisanpmparallel[0]]
            paralleldict["skt"] = sanpmdict[plisanpmparallel[1]]
            outputparallelfile.write(json.dumps(paralleldict, ensure_ascii=False, indent=2))
            outputparallelfile.write(',\n')

    except:
        continue

outputparallelfile.write('\n]')
outputparallelfile.close()
outputsanfile.write('\n]')
outputsanfile.close()

