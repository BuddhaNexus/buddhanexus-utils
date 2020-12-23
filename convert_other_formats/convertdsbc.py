#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
converts dsbc html files to files used in buddhanexus before tokanization.
"""

import re
import os
import json
from functools import reduce

base_dir = os.environ['HOME']+'/buddhanexus-utils/convert_other_formats/dsbc_content/'
output_dir = os.environ['HOME']+'/buddhanexus-utils/convert_other_formats/dsbc_out/'

with open(os.environ['HOME']+"/buddhanexus-utils/convert_other_formats/dsbc_book.json") as json_file:
    directorylist = json.load(json_file)

MAXLENGTH = 10
MINLENGTH = 10

def cleanline(line):
    if re.search(r'Parallel|version|<a href="\.\./', line):
        newline = ''
    else:
        newline = re.sub(r'<[A-Za-z-/].*?>', ' ', line)
        newline = newline.replace('&nbsp;',' ')
        newline = newline.replace('&ntilde;','ñ')
        newline = newline.replace('&#039;','’')
        newline = newline.replace('"', '“')
        newline = newline.replace('  ', ' ')
        newline = re.sub(r'[ ]{2,}', ' ', newline)
    return newline.strip(' ')

def splitline_on_danda(line_array, typeDanda):
    partslist = []
    for line in line_array:
        if len_without_chars(line) > MAXLENGTH:
            partslist = list(filter(None,splitkeepsep(line.strip(), typeDanda)))
        else:
            partslist.append(line)

    for part in partslist:
        if part == typeDanda:
            if partslist.index(part) > 0:
                thispartindex = partslist.index(part)
                partslist[thispartindex-1] += typeDanda
            else:
                partslist[1] = partslist[0] + partslist[1]
            partslist.remove(part) 

    partslist = remove_small_segments(partslist)
    partslist = remove_small_segments(partslist)
    return partslist

def len_without_chars(line):
    stripped_line = re.sub(r'([^a-zāīūēṭḍṅṇñḷṃṁśṣḥṛṝḹ])', '', line)
    return len(stripped_line)

def splitkeepsep(s, sep):
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])

def remove_small_segments(partslist):
    if len(partslist) >= 2:
        if len_without_chars(partslist[-1]) < MINLENGTH:
            partslist[-2] += partslist[-1]
            partslist.remove(partslist[-1])
        if len_without_chars(partslist[0]) < MINLENGTH:
            partslist[0] += partslist[1]
            partslist.remove(partslist[1])
    return partslist

def splitline(line_array, sep):
    partslist = []
    for part in line_array:
        if len_without_chars(part) > MAXLENGTH:
            newparts = list(filter(None,splitkeepsep(part.strip(), sep)))
            newparts = remove_small_segments(newparts)
            newparts = remove_small_segments(newparts)
            for newpart in newparts:
                partslist.append(newpart)
        else:
            partslist.append(part)

    return partslist

for directoryname in directorylist:
    sourcedir = base_dir+directoryname+"/"
    for root, dirs, files in os.walk(sourcedir):
        for file in files:
            fileIn = open(root+'/'+file,'r', encoding='utf8')
            fileOut = open(output_dir+file[:-5]+'.json','w', encoding='utf8')
            output_dict = {}
            counter = 0
            filename = file[:-5]

            for line in fileIn:
                if re.search(r'<!-- end of title information -->', line):
                    break

            for line in fileIn:
                clean_line_array = []
                new_line_parts = []
                clean_line = cleanline(line)
                if clean_line and len(clean_line.strip()) > 0:
                    new_line_parts.append(clean_line)
                    if len_without_chars(clean_line) > MAXLENGTH:
                        if re.search('|', clean_line):
                            new_line_parts = splitline_on_danda(new_line_parts, '|')
                        new_line_parts = splitline(new_line_parts, ")")
                        new_line_parts = splitline(new_line_parts, "?")
                        new_line_parts = splitline(new_line_parts, ",")
                        new_line_parts = splitline(new_line_parts, ":")
                        new_line_parts = splitline(new_line_parts, ";")

                    for newpart in new_line_parts:
                        output_dict[filename+":"+str(counter)] = newpart.strip()
                        counter += 1

                if re.search(r'callout large secondary mycallout', line):
                    break

            fileOut.write(json.dumps(output_dict, ensure_ascii=False, indent=4))
            fileOut.close()
