#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
converts gretil xml files to files used in buddhanexus before tokanization.
"""

import re
import os
import json
from functools import reduce


base_dir = os.environ['HOME']+'/segmented-sanskrit/xml/valid/'
output_dir = os.environ['HOME']+'/buddhanexus-utils/test/'

with open(os.environ['HOME']+"/buddhanexus-utils/sanskrit_data/skt-categories_buddhist.json") as json_file:
    categorylist = json.load(json_file)

MAXLENGTH = 10
MINLENGTH = 10

def len_without_chars(line):
    stripped_line = re.sub(r'([^a-zāīūēṭḍṅṇñḷṃṁśṣḥṛṝḹ])', '', line)
    return len(stripped_line)


def cleanline(line):
    newline = re.sub(r"<pb ed='#(.*?)' n='(.*?)'/>", r' [\1_\2]', line)
    newline = re.sub(r'<.*?>', '', newline)
    newline = re.sub(r'\u0007', '', newline)
    newline = newline.replace('&amp;', '')
    newline = newline.replace('  ', ' ')
    return newline


def remove_small_segments(partslist):
    if len(partslist) >= 2:
        if len_without_chars(partslist[-1]) < MINLENGTH:
            partslist[-2] += partslist[-1]
            partslist.remove(partslist[-1])
        if len_without_chars(partslist[0]) < MINLENGTH:
            partslist[0] += partslist[1]
            partslist.remove(partslist[1])
    return partslist


def splitline_on_danda(line_array):
    partslist = []
    for line in line_array:
        if len_without_chars(line) > MAXLENGTH:
            partslist = list(filter(None,splitkeepsep(line.strip(), "/")))
        else:
            partslist.append(line)

    for part in partslist:
        if part == '/':
            if partslist.index(part) > 0:
                thispartindex = partslist.index(part)
                partslist[thispartindex-1] += '/'
            else:
                partslist[1] = partslist[0] + partslist[1]
            partslist.remove(part) 

    partslist = remove_small_segments(partslist)
    partslist = remove_small_segments(partslist)
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


def splitkeepsep(s, sep):
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])


for root, dirs, files in os.walk(base_dir):
    for file in files:
        try:
            filename = categorylist[file.split('.')[0]]
        except:
            filename = 'ZZZ'+file.split('.')[0]
        fileIn = open(base_dir+file,'r', encoding='utf8')
        fileOut = open(output_dir+filename+'.json','w', encoding='utf8')
        output_dict = {}

        for line in fileIn:
            if re.search('</teiHeader>', line):
                break

        xml_number = ''
        counter = 0

        for line in fileIn:
            clean_line_array = []
            new_line_parts = []
            xml_id = re.findall(r'xml:id="(.*?)"',line)
            if xml_id:
                xml_number = xml_id[0].strip()
                if re.match(r"^[0-9]*$", xml_number):
                    xml_number = ''
                else:
                    xml_number += ' '
            else:
                clean_line = cleanline(line)
                if clean_line and len(clean_line.strip()) > 0:
                    new_line_parts.append(clean_line)
                    if len_without_chars(clean_line) > MAXLENGTH:
                        new_line_parts = splitline_on_danda(new_line_parts)
                        new_line_parts = splitline(new_line_parts, ")")
                        new_line_parts = splitline(new_line_parts, "?")
                        new_line_parts = splitline(new_line_parts, "!")
                        new_line_parts = splitline(new_line_parts, ",")
                        new_line_parts = splitline(new_line_parts, ":")
                        new_line_parts = splitline(new_line_parts, ";")

                    for newpart in new_line_parts:
                        output_dict[filename+":"+str(counter)] = xml_number+newpart.strip()
                        counter += 1
                        xml_number = ''

        fileOut.write(json.dumps(output_dict, ensure_ascii=False, indent=2))
        fileOut.close()
