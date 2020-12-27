#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
From the parallellist created with plichn.py, extract the BN numbers for all the matches
"""
import os
import re
import json

parallelpath = os.environ['HOME']+'/buddhanexus-utils/plichn/plichn_parallel_list.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/plichn/files/'

# retrieving data from the parallels file.
parallelfile = open(parallelpath,'r', encoding='utf8').read()
paralleljson = json.loads(parallelfile)

pali_regex = re.compile('^[asmd]n[0-9]+|^iti|^mil|^snp|^[ck]p|^ud|^[bpv]v|^th[ai]|^[mc]nd|^[np]e|^ps|^ja')
sn_an_regex = re.compile('^[as]n[0-9]')
chn_regex = re.compile('^[mds]a[0-9]+|^t[0-9]+[a-z1-9\.]*|^[es]a-[2-3]\.[0-9]+|ea[0-9]+\.[0-9]+')
skt_regex = re.compile('^arv|^avs|^divy|^lal|^san|^sf|^mkv')

palifilespath = os.environ['HOME']+'/segmented-pali/inputfiles/'
chinesefilespath = os.environ['HOME']+'/sc-data/html_text/lzh/sutta/'
chinesefilespath2 = os.environ['HOME']+'/segmented-chinese/files/'
chinesefilespath3 = os.environ['HOME']+'/buddhanexus-utils/chn_files/'
sanskritfiles = open('sanfiles.json','r', encoding='utf8').read()
sanskritjson = json.loads(sanskritfiles)

outputlist = []
outputfile = open('bntable.json','w', encoding='utf8')

for parallel in paralleljson:
    sutta_outputlist = []
    for sutta in parallel:
        bn_segnrs=''
        if pali_regex.match(sutta):
            an_sn_suttanr = ''
            if sn_an_regex.match(sutta):
                suttaname = sutta.split('.')[0]
                try:
                    an_sn_suttanr = sutta.split('.')[1]
                except:
                    an_sn_suttanr = '0'
                    print(sutta+" does not have a section")
            else: suttaname = sutta
            for root, dirs, files in os.walk(palifilespath):
                for name in files:
                    if name[:-17] == suttaname:
                        filetext = open(root+"/"+name).read()
                        filejson = json.loads(filetext)
                        segmentnrs = list(filejson.keys())
                        
                        if an_sn_suttanr:
                            if '-' in an_sn_suttanr:
                                an_sn_range = list(range(int(an_sn_suttanr.split('-')[0]), int(an_sn_suttanr.split('-')[1])+1))
                            else:
                                an_sn_range = [int(an_sn_suttanr)]

                            an_sn_segmentnrs = []
                            for rangenr in an_sn_range:
                                for number in segmentnrs:
                                    if re.match(suttaname+':'+str(rangenr)+'\.', number):
                                        an_sn_segmentnrs.append(number)
                                if an_sn_segmentnrs:
                                    bn_segnrs = an_sn_segmentnrs[0]+'-'+an_sn_segmentnrs[-1]
                        else: 
                            bn_segnrs = segmentnrs[0]+'-'+segmentnrs[-1]

            if bn_segnrs:
                sutta_outputlist.append(bn_segnrs)
            else:
                sutta_outputlist.append(sutta)
                print(sutta+' not found')
                bn_segnrs=''


        if chn_regex.match(sutta):
            if sutta.startswith('t') and not sutta.startswith('t1670b2'):
                for root, dirs, files in os.walk(chinesefilespath2):
                    for name in files:
                        name_nr = re.findall('(?<=n)[0-9]+[a-hA-H]*(?=_)', name)[0]
                        while name_nr[0] == '0':
                            name_nr = name_nr[1:]
                        if name.startswith('T') and name_nr == sutta[1:].split('.')[0]:
                            filetext = open(root+"/"+name).read()
                            filejson = json.loads(filetext)
                            segmentnrs = list(filejson.keys())
                            bn_segnrs = segmentnrs[0]+'-'+segmentnrs[-1]
            
            else: 
                for root, dirs, files in os.walk(chinesefilespath):
                    for name in files:
                        if name[:-5] == sutta:
                            t_list = []
                            filetext = open(root+"/"+name, 'r')
                            for line in filetext:
                                t_nr = re.findall(r't[0-9]+[a-h][0-9]+', line)
                                for nr in t_nr:
                                    t_list.append(nr)

                if sutta.startswith('t1670b2'):
                    sutta_collection = 't1670b'
                else:
                    sutta_collection = re.findall(r'^[msde]a',sutta)[0]


                for root, dirs, files in os.walk(chinesefilespath3+'/'+sutta_collection):
                    segmentnrs = []
                    for name in files:
                        with open(root+"/"+name) as json_file:
                            data = json.load(json_file)
                            for item in sorted(t_list):
                                segment = name[:-5]+':'+item[1:]
                                if segment in data.keys():
                                    segmentnrs.append(segment)
                if segmentnrs:
                    bn_segnrs = sorted(segmentnrs)[0]+'-'+sorted(segmentnrs)[-1]

            if bn_segnrs:
                sutta_outputlist.append(bn_segnrs)
            else:
                sutta_outputlist.append(sutta)
                print(sutta+' not found')
                bn_segnrs=''


        if skt_regex.match(sutta):
            try:
                bn_segnrs = sanskritjson[sutta]
            except:
                print(sutta+' not found in list')

            if bn_segnrs:
                sutta_outputlist.append(bn_segnrs)
            else:
                sutta_outputlist.append(sutta)
                print(sutta+' not found')
                bn_segnrs=''

    outputlist.append(sutta_outputlist)


outputfile.write(json.dumps(outputlist, ensure_ascii=False, indent=2))
outputfile.close()
