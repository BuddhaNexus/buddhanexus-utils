#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
creates a title list for DSBC 
"""

import re
import os
import json
from functools import reduce

base_dir = os.environ['HOME']+'/buddhanexus-utils/convert_other_formats/dsbc_book/'
output_dir = os.environ['HOME']+'/buddhanexus-utils/convert_other_formats/dsbc_out/'

with open(os.environ['HOME']+"/buddhanexus-utils/convert_other_formats/dsbc_book.json") as json_file:
    booklist = json.load(json_file)

output_dict = {}
fileOut = open('dsbc.json','w', encoding='utf8')

def cleanline(line):
    newline = re.sub(r'<[A-Za-z-/].*?>', ' ', line)
    newline = newline.replace('&nbsp;',' ')
    newline = newline.replace('&ntilde;','ñ')
    newline = newline.replace('&#039;','’')
    newline = newline.replace('"', '“')
    newline = newline.replace('  ', ' ')
    newline = re.sub(r'[ ]{2,}', ' ', newline)
    return newline.strip(' ')


for bookname in booklist:
    bncategory = booklist[bookname]["bncategory"]
    sourcefile = base_dir+bookname+".html"
    fileIn = open(sourcefile,'r', encoding='utf8')
    filelist = {}

    for line in fileIn:
        if re.search(r'Book Links', line):
            break

    for line in fileIn:
        filenr = re.findall(r'<a href=".*?/([0-9]*)">', line)
        if not filenr:
            filenr = re.findall(r'<a href=".*?/([0-9]*)\.html">', line)
        if filenr:
            clean_line = cleanline(line)
            filelist[bncategory+"n"+filenr[0]] = clean_line.strip()
            testFile = open(output_dir+bncategory+"n"+filenr[0]+'.json','r', encoding='utf8')

        if re.search(r'</table>', line):
            break

    if filelist:
        output_dict[bookname] = booklist[bookname]
        output_dict[bookname]["filelist"] = filelist


fileOut.write(json.dumps(output_dict, ensure_ascii=False, indent=4))
fileOut.close()
