#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Break json segments that are too long into two segments.
Breaks on spaces only.

"""
import os
import json
import re

inpath = os.environ['HOME']+'/buddhanexus-utils/testout/'
outpath = os.environ['HOME']+'/buddhanexus-utils/testout2/'

def splitsegment(inputstring):
    inputstring = re.sub(r' ([/\|])', r'\1', inputstring)
    outputstrings = []
    words = inputstring.split()
    newstring = ''
    for word in words:
        if '//' in word or '||' in word:
            word = re.sub(r'(//|\|\|)', r' \1', word)
        elif '/' in word or '|' in word:
            word = re.sub(r'(/|\|)', r' \1', word)
        newstring += " " + word
        if len(newstring) > 80:
            outputstrings.append(newstring.strip())
            newstring = ''
    if newstring != '':
        outputstrings.append(newstring.strip())

    if len(outputstrings[-1]) < 20:
        outputstrings[-2] += ' '+outputstrings[-1]
        outputstrings.remove(outputstrings[-1])

    return outputstrings


for root, dirs, files in os.walk(inpath):
    for name in files:
        newdictionary = {}
        filetext = open(root+"/"+name).read()
        jsonobject = json.loads(filetext)
        for item in jsonobject:
            if len(jsonobject[item]) > 180:
                outputstrings = splitsegment(jsonobject[item])
                counter = 0
                for outputstring in outputstrings:
                    newdictionary[item+"_"+str(counter)] = outputstring
                    counter += 1
            else:
                newdictionary[item] = jsonobject[item]
        
        fileOut = open(outpath+"/"+name,'w', encoding='utf8')
        fileOut.write(json.dumps(newdictionary, ensure_ascii=False, indent=2))
        fileOut.close()


errorFile = open('errorfile.txt','w', encoding='utf8')

for root, dirs, files in os.walk(outpath):
    for name in files:
        filetext = open(root+"/"+name).read()
        jsonobject = json.loads(filetext)
        for item in jsonobject:
            if len(jsonobject[item]) > 200:
                errorFile.write("\nFILENAME:"+name+"\n")
                errorFile.write(jsonobject[item])