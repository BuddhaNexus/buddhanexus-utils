#!/usr/bin/python
# -*- coding: utf-8 -*-
""" 
Extract file segments and places them in separate json

"""
import re
import os
import json
import gzip

base_dir = os.environ['HOME']+'/buddhanexus/json/skt/'
output_dir = os.environ['HOME']+'/segmented-sanskrit/files/'


def get_segments_from_gzipped_file(file_bytes: str) -> list:
    """
    Given a url to a .gz file:
    1. Download the file
    2. Unpack it in memory
    3. Return segments and parallels

    :param file_url: URL to the gzipped file
    """
    try:
        with gzip.open(file_bytes) as f:
            parsed = json.loads(f.read())
            segments, parallels = parsed[:2]
            f.close()
            return [segments, parallels]
    except OSError as os_error:
        print(f"Could not load the gzipped file {file_bytes}. Error: ", os_error)
        return [None, None]


def write_segments_to_file(root, file_name):
    file_segments = {}
    fileOut = open(output_dir+file_name[:-3],'w', encoding='utf8')
    [segments, parallels] = get_segments_from_gzipped_file(root+file_name)
    for segment in segments:
        file_segments[segment['segnr']] = segment['segtext']
    fileOut.write(json.dumps(file_segments, ensure_ascii=False, indent=4))
    fileOut.close()


for root, dirs, files in os.walk(base_dir):
    for name in files:
        write_segments_to_file(root, name)

