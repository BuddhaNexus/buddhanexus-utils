#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Check json for validity and segment numbers for validity within neural network

"""
import os
import json
import re

path = os.environ['HOME']+'/segmented-sanskrit/segmented_files/'

def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           raise ValueError("duplicate key: %r" % (k,))
        else:
           d[k] = v
    return d

def check_segment_names(jsonobject,name):
    for k in jsonobject.keys():
        filename, segmentnr = k.split(':')
        if filename != name:
            raise ValueError("wrong filename: %r" % (k,))
        if not re.search(r"^[\.A-Za-z0-9_-]*$", segmentnr):
            raise ValueError("wrong segmentnr: %r" % (k,))

for root, dirs, files in os.walk(path):
    for name in files:
        filetext = open(root+"/"+name).read()
        print(name[:-5])
        jsonobject = json.loads(filetext,object_pairs_hook=dict_raise_on_duplicates)
        check_segment_names(jsonobject,name[:-5])
