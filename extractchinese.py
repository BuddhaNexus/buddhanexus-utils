#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Extract chinese cbeta html files from the cbeta directory
and converts them into json segmented files

"""
import re
import os
import json
import asciitable_chinese

path = os.environ['HOME']+'/buddhanexus-utils/cbeta/'
outputpath = os.environ['HOME']+'/buddhanexus-utils/cbeta_segmented/'
headerfile = open('cbeta_headers.json','w', encoding='utf8')
headers = {}
errorlog = open('cbeta_errors.txt','w', encoding='utf8')
collections_done = open('cbeta_collections_done.txt','w', encoding='utf8')

# asciicodelist = []
asciicodelist2 = []

def clean_tline(segment):
    newsegment = re.sub(r'<span class="gaiji">&#x[0-9A-Z]+;<!--gaiji,,1(.*?),2.*?;,3--></span>', r'\1', segment)
    newsegment = re.sub(r'<span class="gaiji">&#x[0-9A-Z]+;<!--gaiji,(.*?),1.*?,2.*?;,3--></span>', r'\1', newsegment)
    newsegment = re.sub(r'<.*?>', '', newsegment)
    newsegment = re.sub(r'\[[0-9a-z]+\] ', '', newsegment)
    newsegment = re.sub(r'\[[0-9a-z]+\]', '', newsegment)
    newsegment = newsegment.replace('\u3000',' ')
    asciicode = re.findall(r'(&#x.*?;)', newsegment)
    if asciicode:
        for item in asciicode:
            # if not item in asciicodelist:
            #         asciicodelist.append(item)
            if item in asciitable_chinese.codes_dict.keys():
                newsegment = re.sub(item, asciitable_chinese.codes_dict[item],newsegment)
            elif not item in asciicodelist2:
                asciicodelist2.append(item)

    return newsegment

for root, dirs, files in os.walk(path):
    for name in files:
        if re.search(r"^[TX][0-9]+n[0-9a-zA-Z]+\.html", name):
            collections_done.write(name+"\n")
            totalfiles = open(root+name,'r', encoding='utf8').read()
            files = re.findall(r"([TX][0-9]+n[0-9a-gA-G]+_[0-9a-gA-G]+)", totalfiles)
            testfiles = re.findall(r"([TX][0-9]+n[0-9a-gA-G]+_)", totalfiles)
            if files == []:
                errorlog.write("empty: "+name+"\n")
            if len(testfiles) != len(files):
                errorlog.write("different length: "+name+"\n")
            for file in files:
                try:
                    segments = {}
                    headers[file] = "TITLE NOT FOUND"
                    print(root+file+'.html')
                    filetext = open(root+file+'.html','r', encoding='utf8')
                    if not filetext:
                        filetext = open(root+file,'r', encoding='utf8')
                    for line in filetext:
                        fileheader = re.findall(r'<h1 class="title">(.*?)</h1>', line)
                        if fileheader:
                            headers[file] = fileheader[0].split(' ',1)[-1]
                            break
                    counter = 0
                    for line in filetext:
                        tline = re.findall(r'name="([0-9]+.*?)" .*?></a>(.*?)<a \n',line)
                        if tline:
                            segment = clean_tline(tline[0][1])
                            if segment != '':
                                segments[file.split('.')[0]+":"+tline[0][0]] = segment

                        if re.search(r'<span class="juanname">',line):
                            counter += 1
                        if counter == 2:
                            break

                    outputfile = open(outputpath+file.split('.')[0]+'.json','w', encoding='utf8')
                    outputfile.write(json.dumps(segments, ensure_ascii=False, indent=4))
                    outputfile.close()
                except:
                    errorlog.write(file+"\n")


headers_sorted = {}
for i in sorted(headers.keys()):
    headers_sorted[i] = headers[i]

headerfile.write(json.dumps(headers_sorted, ensure_ascii=False, indent=4))
headerfile.close()
errorlog.close()
collections_done.close()
print(sorted(asciicodelist))
print(sorted(asciicodelist2))

