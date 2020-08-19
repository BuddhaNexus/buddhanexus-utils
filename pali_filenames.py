#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
finding additional info on display names in commentaries pali
"""

import re
import os
import json

path = os.environ['HOME']+'/segmented-pali/inputfiles/'
filetitlespath = os.environ['HOME']+'/buddhanexus/data/pli-files.json'
filetitles = json.loads(open(filetitlespath).read())

newtitles = []

for item in filetitles:
  if re.search(r'^atk|tika|anya', item['filename']):
      for root, dirs, files in os.walk(path):
          for name in files:
              filename = name[:-17]
              if filename != item['filename']:
                continue
              else:
                filetext = open(root+"/"+name).read()
                jsonobject = json.loads(filetext)
                firstline = jsonobject[next(iter(jsonobject))]

                firsttest = re.search(r'^[0-9-().]+ [0-9-().]+ (.*?)$', firstline)
                secondtest = re.search(r'^[0-9-().]+ (.*?)$', firstline)
                thirdtest = re.search(r'Namo tassa bhagavato arahato sammāsambuddhassa', firstline)

                if firsttest:
                    item['displayName'] += ' / ' + firsttest.group(1)
                elif secondtest:
                    item['displayName'] += ' / ' + secondtest.group(1)
                elif thirdtest:
                    secondline = jsonobject[list(jsonobject)[1]]
                    firsttest = re.search(r'^[0-9-().]+ [0-9-().]+ (.*?)$', secondline)
                    secondtest = re.search(r'^[0-9-().]+ (.*?)$', secondline)
                    if firsttest:
                        item['displayName'] += ' / ' + firsttest.group(1)
                    elif secondtest:
                        item['displayName'] += ' / ' + secondtest.group(1)
                    else:
                        item['displayName'] += ' / ' + secondline
                else:
                    item['displayName'] += ' / ' + firstline
  
  newtitles.append(item)


filepath_Out = open('pli-titles.json','w', encoding='utf8')
filepath_Out.write(json.dumps(newtitles, ensure_ascii=False, indent=2))

