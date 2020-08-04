#!/usr/bin/python
# -*- coding: utf-8 -*-

""" High precision hyphenator for sanskrit

Uses a list of segments to attempt to hyphenate words

Then performs corrections to move hyphens in between double consonants
and such

"""

import re
import regex
import os

base_dir = os.environ['HOME']+'/Desktop/vi/skt-mu-kd/' 
output_dir = os.environ['HOME']+'/Desktop/sktoutput/' 
segments = {
    "dhamma",
    "śunya",
    "hīna",
    "putta",
    "deva",
    "khema",
    "vibhaṅga",
    "suñña",
    "mutta",
    "gotta",
    "yata",
    "mogga",
    "sevi",
    "saṅk",
    "rīsa",
    "mahā",
    "pari",
    "bodhi",
    "vitakka",
    "bahu",
    "khemā",
    "ratha",
    'rāja',
    'nibbāna',
    'sati',
    'dukkha',
    'vinī',
    'gatā',
    'cūḷa',
    'sacca',
    'rāhu',
    'piṇḍi',
    'Ānanda',
    'bhadde',
    'kaḷā',
    'bara',
    'indriya',
    'sakula',
    'samaṇa',
    'giri',
    'kumāra',
    'bala',
    'thulla',
    'caṇḍala',
    'pokkha',
    'loma',
    'kana',
    'iccha',
    'aṅguttara',
    'kattha',
    'koccha',
    'nimmā',
    'eka',
    'hatthi',
    'pada',
    'saka',
    'bāla',
    'komāra',
    'sammā',
    'diṭṭhi',
    'tiṭṭhi',
    'patti',
    'janīya',
    'thaddha',
    'kopama',
    'gamā',
    'dūpama',
    'bhacca',
    'khamma',
    'kacca',
    'puṇḍa',
    'sattva',
    'saṃ',
    'buddhā',
    'bhāvenā',
    'gaṇa',
    'pura',
    'buddha',
    'dharma',
    'dharmā',
    'tathāga',
    'karma',
    'bhūmi',
    'bhāva',
    'karma',
    'karmā',
    'yaṃ',
    'bhūva',
    'vaddā',
    'ṣānti',
    'vīrya',
    'mantrā',
    'ṇasthā',
    'nānā',
    'saraḥ',
    'brahmaloka',
    'bhikṣu',
    'dhama',
    'dhura',
    'mano',
    'rama',
    'bhūta',
    'candrā',
    'brahma',
    'patra',
    'gupta',
    'jīvakā',
    'yūra',
    'kūṭā',
    'gāra',
    'rūpya',
    'maṇi',
    'muktā',
    'dūrya',
    'śaṅkha',
    'śilā',
    'pravā',
    'divyā','guru','canda','vilepana','mālo','ḍayanti',
    'pāda',
    'bhadra',
    'jāti','jarā','maraṇa','duḥkha','samudayā','vajra','cakra','bhavana','bhāṣitā','bhāṣitā','tuṣita','gara','yantā','śastre',
    'indukā','śarasā','paṭā','jñāna','vipula','dhāra','bhāṣita','dhāra','pitta','parya','lokitā','loke','loki','koṭina','yuta','śata','saha',
    'yudā','kāma','kānta','yāna','maṇḍala','prajña','bodhya','prasā','māra','mara','akuśala','mūlā','yathā','raja','dhātu','samya',
    'prāya','manna','pānā','vastrā','jīvika','śānta','citta','jaṭā','vividha','pana', 'prahāṇa','endriya', 'pād','māna','kusuma','manā', 'kama',
    'mantra', 'vicāra','pāṣāṇa'
}

cons = "(?:br|[kgcjtṭdḍbp]h|[kgcjtṭḍp](?!h)|[mnyrlvshṅṇṃṃñḷ]|b(?![rh]))";
vowel_chars = 'aioueāīū'
vowel_pattern = '[' + vowel_chars.lower() + ']'
vowel_antipattern = '[^' + vowel_chars.lower() + '-]'

segments_revoweled = [regex.sub(vowel_pattern + '$', vowel_pattern, segment, flags=regex.I) for segment in sorted(segments, key=len, reverse=True)]

segment_rex = regex.compile('({})'.format("|".join(segments)), flags=regex.I)

alpha_rex = regex.compile(r'\p{alpha}+')

def fix_hyphens(word):
    word = word.replace('sv','s-v')
    word = word.replace('tk','t-k')
    word = word.replace('ṭv','ṭ-v')
    for i in range(0, 2):
        word = regex.sub(r'-({})({})'.format(cons, cons), r'\1-\2', word, flags=regex.I)
        word = regex.sub(r'([kgcjḍṭdtpb])-(h{})'.format(vowel_pattern), r'\1\2-', word, flags=regex.I)
    word = regex.sub(r'^(\p{alpha}{0,3})-', r'\1', word)
    word = regex.sub(r'-(\p{alpha}{0,3})$', r'\1', word)
    word = re.sub(r'r-([kgḍṭdtpb])',r'r\1',word)
    word = re.sub(r'-([ṃṁḥh])',r'\1',word)
    word = re.sub(r'([ṃṁ])',r'\1-',word)
    word = word.replace('p-r','pr')
    word = word.replace('k-s', 'ks')
    word = word.replace('k-ṣ','kṣ')
    word = word.replace('k-ś','kś')
    word = word.replace('ñ-j','ñj')
    word = word.replace('r-ṇ','rṇ')
    word = word.replace('n-j','nj')
    word = word.replace('-aṅ','aṅ')
    word = word.replace('-an','an')
    word = re.sub(r'-(.)-',r'\1-',word)
    word = word.replace('--','-')
    return word.strip('-')
    
def hyphenate(word, max_length):
    if len(word) <= max_length:
        return word

    word = segment_rex.sub(r'-\1-', word)
    word = word.replace('--', '-')
    word = word.strip('-')
    word = fix_hyphens(word)
    
    for segment in alpha_rex.findall(word):
        if len(segment) > max_length:
            print('Segment too long: {}'.format(segment))
    word = re.sub(r'([>’—])-',r'\1',word)
    word = re.sub(r'-([<—])',r'\1',word)
    word = re.sub(r'-(.)-',r'\1-',word)
    return word.replace('-', '\xad')


for name in os.listdir(base_dir):
    print(name)
    fileOpen = open(base_dir+name,'r')
    fileOut = open(output_dir+name,'w')

    for line in fileOpen:
        fileOut.write(line)
        if line.startswith('</div>'):
            break
    for line in fileOpen:
        if line.startswith('</article>'):
            fileOut.write(line)
            break
        lineout = ""
        wordlist = re.split(r' ',line.strip())
        for word in wordlist:
            newword = hyphenate(word, 25)
            newword = re.sub('gatha\xadnumber','gatha-number',newword)
            lineout +=newword
            lineout +=" "
        fileOut.write(lineout.rstrip(' ')+'\n') 

    for line in fileOpen:
        fileOut.write(line)

    fileOut.close()