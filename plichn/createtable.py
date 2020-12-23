#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Creates a table from the files with the BN numbers of all files in it.
"""
import os
import re
import json

parallelpath = os.environ['HOME']+'/buddhanexus-utils/plichn/files/'
outputpath = os.environ['HOME']+'/buddhanexus-utils/plichn/'
outputfile = open(outputpath+'bntable.json','w', encoding='utf8')

def getparallels(filename):
  bnnumberlist = []
  for sourcedir, partialdir, names in os.walk(parallelpath+filename):
    if partialdir == ['partial']:
      for name in names:
        with open(sourcedir+'/'+name) as json_file:
          data = json.load(json_file)
          bnnumbers = list(data.keys())
          firstbnnr = bnnumbers[0]
          lastbnnr = bnnumbers[-1]
          bnnumberlist.append(firstbnnr+'-'+lastbnnr)

  return bnnumberlist

bnparallels = {}

i = 1
while i < 35:
  parallels = getparallels('dn'+str(i))
  if len(parallels) > 0:
    bnparallels['dn'+str(i)] = parallels
  i += 1

i = 1
while i < 153:
  parallels = getparallels('mn'+str(i))
  if len(parallels) > 0:
    bnparallels['mn'+str(i)] = parallels
  i += 1


outputfile.write(json.dumps(bnparallels, ensure_ascii=False, indent=2))
outputfile.close()






            
