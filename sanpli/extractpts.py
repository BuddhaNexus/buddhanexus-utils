#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
extracting sanskrit words from PTS dictionary for use with neural network training

"""
import os
import re
import json

pts_path = os.environ['HOME']+'/buddhanexus-utils/sanpli/pts.json'
output_path = os.environ['HOME']+'/buddhanexus-utils/sanpli/'
error_file = open(output_path+'pli_san_errors.txt','w', encoding='utf8')

# retrieving pts entries with etimological data <p class='eti'>
pts_json = json.loads(open(pts_path,'r', encoding='utf8').read())
output_file = open(output_path+'pli_san_words.json','w', encoding='utf8')
output_file.write("[\n")

for word in pts_json:
    try:
        ethymology = re.findall("<p class='eti'>(.*?)</p>", word["text"])
        if ethymology and "Sk." in ethymology[0] or "Vedic" in ethymology[0]:
            sanskrit_words = re.findall(r"Vedic (.*?)[;, ]|Sk. (.*?)(?:\s+|$)|Vedic (.*?)(?:|$)", ethymology[0])

            if sanskrit_words:
                pts_dict = {}
                for ref in range(3):
                    if sanskrit_words[0][ref] == '':
                        continue
                    else:
                        if re.search(r"-$", sanskrit_words[0][ref]):
                            error_file.write("Weird character found in: "+word["word"]+": "+ethymology[0]+"\n")
                        pts_dict["original"] = ethymology[0]
                        pts_dict["pli"] = word["word"]
                        pts_dict["skt"] = sanskrit_words[0][ref].strip("*")

                        output_file.write(json.dumps(pts_dict, ensure_ascii=False, indent=4))
                        output_file.write(",\n")
            else:
                error_file.write("REFERENCE NOT FOUND: "+word["word"]+": "+ethymology[0]+"\n")
    except:
        continue



output_file.write("\n]")
output_file.close()
error_file.close()