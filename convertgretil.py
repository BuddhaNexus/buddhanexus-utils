#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
converts gretil xml files to files used in buddhanexus before tokanization.
"""

import re
import os
import json
from removediacritics import remove_diacritics 


base_dir = os.environ['HOME']+'/segmented-sanskrit/xml/valid/'
output_dir = os.environ['HOME']+'/buddhanexus-utils/testout/'

filenames = open(os.environ['HOME']+'/buddhanexus-utils/filenames.json','w')
file_names = {}

def cleanline(line):
    newline = re.sub(r"<pb ed='#(.*?)' n='(.*?)'/>", r' [\1_\2]', line)
    newline = re.sub(r'<.*?>', '', newline)
    newline = re.sub(r'\u0007', '', newline)
    newline = newline.replace('&amp;', '')
    newline = newline.replace('  ', ' ')
    return newline

for root, dirs, files in os.walk(base_dir):
    for file in files:
        filename = file.split('.')[0]
        fileIn = open(base_dir+file,'r', encoding='utf8')
        fileOut = open(output_dir+filename+'.json','w', encoding='utf8')
        output_dict = {}

        for line in fileIn:
            file_title = re.findall(r"<title>(.*?)</title>",line)
            if file_title and file_title[0] != '':
                file_names[filename] = file_title[0]
            elif re.search('</teiHeader>', line):
                break

        xml_number = '0'
        old_xml_number = '0'
        counter = 0
        line_parts = []
        for line in fileIn:
            xml_id = re.findall(r'xml:id="(.*?)"',line)
            if xml_id:
                xml_number = remove_diacritics(xml_id[0].strip())
                if xml_number == old_xml_number:
                    print(xml_number, " is double in ", file)
                old_xml_number = xml_number
                counter = 0
            else:
                clean_line = cleanline(line)
                if clean_line and clean_line != '':
                    if len(clean_line) > 100:
                        line_parts = re.split('(.*?[/,:;.\n])', clean_line)[1::2]
                        if line_parts == []:
                            line_parts.append(clean_line)
                        short_part = ''
                        new_line_parts = []
                        for part in line_parts:
                            if len(part) < 30:
                                short_part += part
                            else:
                                new_line_parts.append(short_part+part)
                                short_part = ''

                        for newpart in new_line_parts:
                            output_dict[filename+":"+xml_number+"_"+str(counter)] = newpart.strip()
                            counter += 1
                    elif len(clean_line.strip()) > 0:
                        output_dict[filename+":"+xml_number+"_"+str(counter)] = clean_line.strip()
                        counter += 1

        fileOut.write(json.dumps(output_dict, ensure_ascii=False, indent=2))
        fileOut.close()

sorted_file_names = {}
for i in sorted (file_names.keys()) :
    sorted_file_names[i] = file_names[i]

filenames.write(json.dumps(sorted_file_names, ensure_ascii=False, indent=4))
filenames.close()

