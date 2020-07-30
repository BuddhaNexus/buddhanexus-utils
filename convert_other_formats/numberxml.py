#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Number xml files consecutively

"""
import os
import re

filename = os.environ['HOME']+'/buddhanexus-utils/finished/valid/arhebt_u.xml'
fileout = os.environ['HOME']+'/Desktop/arhebt_u.xml'
fileIn = open(filename,'r', encoding='utf8')
fileOut = open(fileout,'w', encoding='utf8')
counter = 0

for line in fileIn:
	if re.search(r'<p xml:id="0">', line):
		line = line.replace('<p xml:id="0">','<p xml:id="'+str(counter)+'">')
		counter += 1
	fileOut.write(line)

fileOut.close()