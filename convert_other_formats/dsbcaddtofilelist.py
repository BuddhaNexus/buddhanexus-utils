#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
adds files to a filelist for use in BN 
"""

import re
import os
import json


base_dir = os.environ['HOME']+'/buddhanexus-utils/convert_other_formats/'
output_dir = os.environ['HOME']+'/buddhanexus-utils/convert_other_formats/'

with open(os.environ['HOME']+"/buddhanexus-utils/convert_other_formats/dsbc.json") as json_file:
    booklist = json.load(json_file)

output_list = []
# filenr_list = []
fileOut = open('dsbcfiles.json','w', encoding='utf8')

for bookname in booklist:
    bnfiles = booklist[bookname]["filelist"]
    bnlink = booklist[bookname]["url"]
    for key in bnfiles.keys():
        category, filenr = key.split('n',1)
        # filenr_list.append(int(filenr))
        output_dict = {}
        output_dict["displayName"] = bnfiles[key]
        output_dict["textname"] = category + ' ' + filenr
        output_dict["filename"] = key
        output_dict["category"] = category
        output_dict["filenr"] = int(filenr)
        output_dict["gretil_link"] = re.sub(r'<filenr>', filenr, bnlink)
        output_list.append(output_dict)

newlist = sorted(output_list, key=lambda k: k['filenr']) 

fileOut.write(json.dumps(newlist, ensure_ascii=False, indent=4))
fileOut.close()

# sortedlist = sorted(filenr_list)

