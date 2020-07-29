""" 
Tokanizer for changing Bilara json files to be used in a neuronal network.
Based on hypenation code and pali lookup tool.

"""

import regex
import os
import re
from functools import reduce
import json
import paliwords


cons = "(?:br|[kgcjtṭdḍbp]h|[kgcjtṭdḍp](?!h)|[mnyrlvshṅṇṃṁkñḷ]|b(?![rh]))";
vowel_chars = 'aioueāīū'
vowel_pattern = '[' + vowel_chars.lower() + ']'
vowel_antipattern = '[^' + vowel_chars.lower() + '-]'

segments_revoweled = [regex.sub(vowel_pattern + '$', vowel_pattern, segment, flags=regex.I) for segment in sorted(paliwords.segments, key=len, reverse=True)]

segment_rex = regex.compile('({})'.format("|".join(segments_revoweled)), flags=regex.I)

alpha_rex = regex.compile(r'\p{alpha}+')

def fix_hyphens(word):
    for i in range(0, 2):
        word = regex.sub(r'-({})({})'.format(cons, cons), r'\1-\2', word, flags=regex.I)
        word = regex.sub(r'-({})-({})'.format(cons, cons), r'\1-\2', word, flags=regex.I)
        word = regex.sub(r'([kgcjḍṭdtpb])-(h{})'.format(vowel_pattern), r'\1\2-', word, flags=regex.I)
    word = regex.sub(r'^(\p{alpha}{0,3})-', r'\1', word)
    word = regex.sub(r'-(\p{alpha}{0,3})$', r'\1', word)
    return word

def cleanup_line(line):

        line = line.replace('-',' ')
        line = line.replace('      ',' ')
        line = regex.sub(r' ([a-zA-Z]) ',r' \1',line)
        line = regex.sub(r' ([a-zA-Z])([\.\,;:\?\!”’"\n—])',r'\1\2',line)
        line = regex.sub(r'([“‘]) ([a-zA-Z])',r'\1\2',line)
        line = regex.sub(r'([\—\”\’…])',r' ',line)
        line = line.replace('  ',' ')
        line = regex.sub(r'[\.\,;\?\!“‘‘]',r'',line)
        line = regex.sub(r'([a-z]):',r'\1',line)
        return line

def hyphenate(word, max_length):
    # if len(word) <= max_length:
    #     return word

    word = word.lower()
    word = word.replace('☑','')
    word = word.replace('☒','')
    word = segment_rex.sub(r'-\1-', word)
    word = word.replace('--', '-')
    word = word.strip('-')
    word = word.replace('"-','"')
    word = regex.sub(r'-([\.;,\?\!:”’"])', r'\1', word)
    word = fix_hyphens(word)
    
    # for segment in alpha_rex.findall(word):
        # if len(segment) > max_length:
            # print('Segment too long: {}'.format(segment))

    return unicode_to_internal_transliteration(word)

def unicode_to_internal_transliteration(s):
        for src,dst in paliwords.UNICODE_INTERN:
                s = s.replace(src,dst)
        out = s#ascii(s)
        return out

def splitkeepsep(s, sep):
    return reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == sep else acc + [elem], re.split("(%s)" % re.escape(sep), s), [])

path = os.environ['HOME']+'/segmented-pali/inputfiles/'
path_output = os.environ['HOME']+'/Desktop/convertbilara/cutsegments/'

for root, dirs, files in os.walk(path):
    for name in files:
        filetext = open(root+"/"+name).read()
        print(root+"/"+name)
        newobjectitem = {}
        jsonobject = json.loads(filetext)
        filepath_Out = open(path_output+name[:-17]+'.json','w', encoding='utf8')
        for item in jsonobject.items():
                if item[0] == '~':
                        continue
                seconditemlist = []
                itemlist = list(filter(None,splitkeepsep(item[1].strip(),".")))
                for things in itemlist:
                        thinglist = list(filter(None,splitkeepsep(things.strip(),",")))
                        for thingitem in thinglist:
                                seconditemlist.append(thingitem)
                newitemlist = []
                counter = 0
                for stuff in seconditemlist:
                        if len(stuff) < 30 and counter != 0:
                                newitemlist[counter-1] = newitemlist[counter-1]+' '+stuff.strip()
                        else:
                                newitemlist.append(stuff.strip())
                                counter = counter+1

                if (len(item[1]) > 50 and len(newitemlist) > 1):
                        newnumber = 0
                        for itempart in newitemlist:
                                newobjectitem[item[0]+'_'+str(newnumber)] = itempart.strip()
                                newnumber = newnumber+1
                else:
                        newobjectitem[item[0]+'_0'] = item[1]
                        
        filepath_Out.write(json.dumps(newobjectitem, ensure_ascii=False, indent=2))                

base_dir = os.environ['HOME']+'/Desktop/convertbilara/cutsegments/' 
output_dir = os.environ['HOME']+'/Desktop/convertbilara/outputfiles/'

for name in os.listdir(base_dir):
    print(name)
    fileOpen = open(base_dir+name,'r')
    fileOut = open(output_dir+name[:-4]+'txt','w')

    for line in fileOpen:
        lineout = ""
        linenumber = re.findall(r'"(.*?)": ',line)
        if linenumber:
                wordlist = re.split(r' ',line.strip())
                for word in wordlist:
                    newword = hyphenate(word,10)
                    lineout +=newword
                    lineout +=" "
                    line = line.replace('      ',' ')
                    lineout = cleanup_line(lineout)
                fileOut.write('LC'+linenumber[0]+'      '+re.findall(r'".*?": "(.*?)"',line)[0]+'      '+re.findall(r'".*?": "(.*?)"',lineout.strip(' '))[0]+'\n') 
    fileOut.close()

