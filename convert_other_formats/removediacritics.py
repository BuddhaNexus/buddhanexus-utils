""" 
Function to remove diacriticals from Pali and Sanskrit text.
[ā,ī,ū,ē,ṭ,ḍ,ṅ,ṇ,ñ,ḷ,ṃ,ṁ,ś,ṣ,ḥ,ṛ,ṝ,ḹ]
"""

diacritics_conversion_dict = {
    'ā': 'a',
    'ī': 'i',
    'ū': 'u',
    'ē': 'e',
    'ṭ': 't',
    'ḍ': 'd',
    'ṅ': 'n',
    'ṇ': 'n',
    'ñ': 'n',
    'ḷ': 'l',
    'ṃ': 'm',
    'ṁ': 'm',
    'ś': 's',
    'ṣ': 's',
    'ḥ': 'h',
    'ṛ': 'r',
    'ṝ': 'r',
    'ḹ': 'l'
}

def remove_diacritics(line):
    newline = ''
    for character in line.lower():
        if character in diacritics_conversion_dict.keys():
            newline += diacritics_conversion_dict[character]
        else:
            newline += character
    return(newline)

