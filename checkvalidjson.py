#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
check json input files for pali to make sure they are valid

"""
import os
import json

path = os.environ['HOME']+'/buddhanexus-utils/testout/'

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
		if k.split(':')[0] != name:
			raise ValueError("wrong name: %r" % (k,))

for root, dirs, files in os.walk(path):
    for name in files:
        filetext = open(root+"/"+name).read()
        print(name.split('_')[0])
        jsonobject = json.loads(filetext,object_pairs_hook=dict_raise_on_duplicates)
        check_segment_names(jsonobject,name.split('_')[0])






