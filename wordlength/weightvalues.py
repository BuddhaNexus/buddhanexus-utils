#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Calculating weight values
ctc = collection total characters
ctw = collection total words
ftc = file total characters
ftw = file total words

AWL = total characters / total words for either collection or file

fcw = file character weight = ftc / ctc *100%
fww = file word weight = ftw / ctw * 100%

"""
import os
import re
import json

ctc_values = {   "dn":1069312,
    "mn":1831996,
    "sn":1938061,
    "an":2265089,
    "kp":8084,
    "ud":149408,
    "iti":86293,
    "snp":143876,
    "vv":90621,
    "pv":73704,
    "thag":114841,
    "thig":44663,
    "tha-ap":527841,
    "thi-ap":102314,
    "bv":82295,
    "cp":30411,
    "ja":603618,
    "mnd":595202,
    "cnd":411550,
    "ps":650602,
    "ne":219450,
    "pe":252862,
    "mil":550482,
    "pli-tv-bu-vb":901281,
    "pli-tv-bi-vb":258865,
    "pli-tv-kd":1499093,
    "pli-tv-pvr":501186,
    "ds":378734,
    "vb":624164,
    "dt":126514,
    "pp":110541,
    "kv":587861,
    "ya":1409893,
    "patthana":3340948,
    "atk-s":21273354,
    "atk-vin":2021143,
    "atk-abh":2164336,
    "tika-s":8553018,
    "tika-vin":9946585,
    "tika-abh":4533515,
    "anya-e":11018844
}

ctw_values = {
    "dn":139325,
    "mn":239205,
    "sn":252659,
    "an":291950,
    "kp":1116,
    "ud":19462,
    "iti":11276,
    "snp":19916,
    "vv":12327,
    "pv":10384,
    "thag":15541,
    "thig":6099,
    "tha-ap":65401,
    "thi-ap":13276,
    "bv":10414,
    "cp":4125,
    "ja":87008,
    "mnd":76032,
    "cnd":50996,
    "ps":72311,
    "ne":27409,
    "pe":32795,
    "mil":70452,
    "pli-tv-bu-vb":114792,
    "pli-tv-bi-vb":31882,
    "pli-tv-kd":189357,
    "pli-tv-pvr":60158,
    "ds":48950,
    "vb":74328,
    "dt":16060,
    "pp":14180,
    "kv":74311,
    "ya":177143,
    "patthana":375375,
    "atk-s":2583704,
    "atk-vin":244526,
    "atk-abh":244461,
    "tika-s":918572,
    "tika-vin":1135715,
    "tika-abh":476637,
    "anya-e":1297187
}

# "dn2":[54845,6891,7.96],
# ctc = collection total characters
# ctw = collection total words
# ftc = file total characters
# ftw = file total words

# AWL = total characters / total words for either collection or file

# fcw = file character weight = ftc / ctc *100%
# fww = file word weight = ftw / ctw * 100%

filedatapath = os.environ['HOME']+'/buddhanexus-utils/wordlength/filestotaldata.json'
outputpath = os.environ['HOME']+'/buddhanexus-utils/wordlength/'

# retrieving data from the filedata file.
filedata = json.loads(open(filedatapath,'r', encoding='utf8').read())
outputdata = open(outputpath+'weightvalues.csv','w', encoding='utf8')

for collection in ctc_values.keys():
    ctc = ctc_values[collection]
    ctw = ctw_values[collection]
    for key,value in filedata.items():
        if re.search(r"^"+collection+r"[0-9-]", key):
            ftc = value[0]
            ftw = value[1]
            fcw = ftc*100/ctc
            fww = ftw*100/ctw

            outputdata.write(key+","+str(fcw)+","+str(fww)+"\n")

outputdata.close()

