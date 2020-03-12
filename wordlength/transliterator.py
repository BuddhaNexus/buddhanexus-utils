
def toDevanagari(word):
        l = word.lower() + ' '
        m = { 'a': ' अ', 'i': ' इ', 'u': ' उ', 'ā': ' आ', 'ī': ' ई', 'ū': ' ऊ', 'o': " ओ", 'e': ' ए' }
        n = {
            'ā': 'ा',
            'i': 'ि',
            'ī': 'ी',
            'u': 'ु',
            'ū': 'ू',
            'e': 'े',
            'o': 'ो',
            'ṃ': 'ं',
            'k': 'क',
            'kh': 'ख',
            'g': 'ग',
            'gh': 'घ',
            'ṅ': 'ङ',
            'c': 'च',
            'ch': 'छ',
            'j': 'ज',
            'jh': 'झ',
            'ñ': 'ञ',
            'ṭ': 'ट',
            'ṭh': 'ठ',
            'ḍ': 'ड',
            'ḍh': 'ढ',
            'ṇ': 'ण',
            't': 'त',
            'th': 'थ',
            'd': 'द',
            'dh': 'ध',
            'n': 'न',
            'p': 'प',
            'ph': 'फ',
            'b': 'ब',
            'bh': 'भ',
            'm': 'म',
            'y': 'य',
            'r': 'र',
            'l': 'ल',
            'ḷ': 'ळ',
            'v': 'व',
            's': 'स',
            'h': 'ह'
        }
        k = ''
        h = ''
        g = ''
        f = ''
        e = ''
        d = ''
        b = ''
        c = ''
        a = 0
        j = 0
        while j < len(l):
            if j > 1: 
                k = l[j - 2]
            else: 
                k = ''
            if j > 0: 
                h = l[j - 1]
            else: 
                h = ''
            g = l[j]
            if j+1 < len(l): 
                f = l[j + 1]
            else: 
                f = ''
            if j+2 < len(l): 
                e = l[j + 2]
            else: 
                e = ''
            if j+3 < len(l): 
                d = l[j + 3]
            else: 
                d = ''
            if j+4 < len(l): 
                b = l[j + 4]
            else: 
                b = '' 
            if j == 0 and g in m:
                c = c + m[g]
                j += 1
            else:
                if f == 'h' and (g + f) in n:
                    c = c + n[g + f]
                    if e and not e in m and f != 'ṃ': 
                        c = c + '्'
                    j += 2
                else:
                    if g in n:
                        c = c + n[g]
                        if f and not f in m and not g in m and g != 'ṃ':
                            c = c + '्'
                        j += 1
                    else:
                        if g != 'a':
                            c = c + g
                            j += 1
                            if f in m:
                                c = c + m[f]
                                j += 1
                        else:
                            j += 1

        c = re.sub(r'\`+', '"', c)
        return c

def toSinhala(word):
        l = word.lower() + ' '
        m = { "a": 'අ', 'ā': 'ආ', "i": 'ඉ', 'ī': 'ඊ', "u": 'උ', 'ū': 'ඌ', "e": 'එ', "o": 'ඔ' }
        b = {
            'ā': 'ා',
            "i": 'ි',
            'ī': 'ී',
            "u": 'ු',
            'ū': 'ූ',
            "e": 'ෙ',
            "o": 'ො',
            'ṃ': 'ං',
            "k": 'ක',
            "g": 'ග',
            'ṅ': 'ඞ',
            "c": 'ච',
            "j": 'ජ',
            'ñ': 'ඤ',
            'ṭ': 'ට',
            'ḍ': 'ඩ',
            'ṇ': 'ණ',
            "t": 'ත',
            "d": 'ද',
            "n": 'න',
            "p": 'ප',
            "b": 'බ',
            "m": 'ම',
            "y": 'ය',
            "r": 'ර',
            "l": 'ල',
            'ḷ': 'ළ',
            "v": 'ව',
            "s": 'ස',
            "h": 'හ'
        }
        j = {
            "kh": 'ඛ',
            "gh": 'ඝ',
            "ch": 'ඡ',
            "jh": 'ඣ',
            'ṭh': 'ඨ',
            'ḍh': 'ඪ',
            "th": 'ථ',
            "dh": 'ධ',
            "ph": 'ඵ',
            "bh": 'භ',
            'jñ': 'ඥ',
            'ṇḍ': 'ඬ',
            "nd": 'ඳ',
            "mb": 'ඹ',
            "rg": 'ඟ'
        }
        a = {
            "k": 'ක',
            "g": 'ග',
            'ṅ': 'ඞ',
            "c": 'ච',
            "j": 'ජ',
            'ñ': 'ඤ',
            'ṭ': 'ට',
            'ḍ': 'ඩ',
            'ṇ': 'ණ',
            "t": 'ත',
            "d": 'ද',
            "n": 'න',
            "p": 'ප',
            "b": 'බ',
            "m": 'ම',
            "y": 'ය',
            "r": 'ර',
            "l": 'ල',
            'ḷ': 'ළ',
            "v": 'ව',
            "s": 'ස',
            "h": 'හ'
        }
        k = ''
        h = 0
        g = ''
        f = ''
        e = ''
        d = ''
        c = ''

        while h < len(l):
            if h > 1: 
                k = l[h - 2]
            else: 
                k = ''
            if h > 0: 
                g = l[h - 1]
            else: 
                g = ''
            f = l[h]
            if h+1 < len(l): 
                e = l[h + 1]
            else: 
                e = ''
            if h+2 < len(l): 
                d = l[h + 2]
            else: 
                d = ''

            if f in m:
                if h == 0 or g == 'a':
                    c += m[f]
                else:
                    if f != 'a': 
                        c += b[f]
                h += 1;
            else:
                if (f + e) in j:
                    c += j[f + e]
                    h += 2
                    if d in a:
                        c += '්'
                else:
                    if f in b and f != 'a':
                        c += b[f]
                        h += 1
                        if e in a and f != 'ṃ':
                            c += '්'
                    else:
                        if not f in b:
                            if g in a or (g == 'h' and k in a):
                                c += '්'
                            c += f
                            h += 1
                            if e in m:
                                c += m[e]
                                h += 1
                        else:
                            h += 1
        if f in a:
            c += '්'

        c = re.sub(r"ඤ්ජ", 'ඦ', c)
        c = re.sub(r"ණ්ඩ", 'ඬ', c)
        c = re.sub(r"න්ද", 'ඳ', c)
        c = re.sub(r"ම්බ", 'ඹ', c)
        c = re.sub(r"්ර", '්ර', c)
        c = re.sub(r"\`+", '"', c)
        return c


def toThai(word):
        m = word.lower() + ' '
        n = { "a": '1', 'ā': '1', "i": '1', 'ī': '1', 'iṃ': '1', "u": '1', 'ū': '1', "e": '2', "o": '2' }
        j = {
            "a": 'อ',
            'ā': 'า',
            "i": 'ิ',
            'ī': 'ี',
            'iṃ': 'ึ',
            "u": 'ุ',
            'ū': 'ู',
            "e": 'เ',
            "o": 'โ',
            'ṃ': 'ํ',
            "k": 'ก',
            "kh": 'ข',
            "g": 'ค',
            "gh": 'ฆ',
            'ṅ': 'ง',
            "c": 'จ',
            "ch": 'ฉ',
            "j": 'ช',
            "jh": 'ฌ',
            'ñ': 'ญ',
            'ṭ': 'ฏ',
            'ṭh': 'ฐ',
            'ḍ': 'ฑ',
            'ḍh': 'ฒ',
            'ṇ': 'ณ',
            "t": 'ต',
            "th": 'ถ',
            "d": 'ท',
            "dh": 'ธ',
            "n": 'น',
            "p": 'ป',
            "ph": 'ผ',
            "b": 'พ',
            "bh": 'ภ',
            "m": 'ม',
            "y": 'ย',
            "r": 'ร',
            "l": 'ล',
            'ḷ': 'ฬ',
            "v": 'ว',
            "s": 'ส',
            "h": 'ห'
        }
        a = {
            "k": '1',
            "g": '1',
            'ṅ': '1',
            "c": '1',
            "j": '1',
            'ñ': '1',
            'ṭ': '1',
            'ḍ': '1',
            'ṇ': '1',
            "t": '1',
            "d": '1',
            "n": '1',
            "p": '1',
            "b": '1',
            "m": '1',
            "y": '1',
            "r": '1',
            "l": '1',
            'ḷ': '1',
            "v": '1',
            "s": '1',
            "h": '1'
        }
        k = 0
        l = ''
        h = ''
        g = ''
        f = ''
        e = ''
        d = ''
        b = ''
        c = ''
        while k < len(m):
            if k > 1: 
                l = m[k - 2]
            else: 
                l = ''
            if k > 0: 
                h = m[k - 1]
            else: 
                h = ''
            g = m[k]
            if k+1 < len(m): 
                f = m[k + 1]
            else: 
                f = ''
            if k+2 < len(m): 
                e = m[k + 2]
            else: 
                e = ''
            if k+3 < len(m): 
                d = m[k + 3]
            else: 
                d = ''
            if k+4 < len(m): 
                b = m[k + 4]
            else: 
                b = '' 

            if g in n:
                if g == 'o' or g == 'e':
                    c += j[g] + j['a']
                    k += 1
                else:
                    if k == 0:
                        c += j['a']

                    if g == 'i' and f == 'ṃ':
                        c += j[g + f]
                        k += 1
                    else:
                        if g != 'a':
                            c += j[g]
                    k += 1

            else:
                if (g+f) in j and f == 'h':
                    if e == 'o' or e == 'e':
                        c += j[e]
                        k += 1
                    c += j[g + f]
                    if e in a:
                        c += 'ฺ'
                    k = k + 2
                else:
                    if g in j and g != 'a':
                        if f == 'o' or f == 'e':
                            c += j[f]
                            k += 1
                        c += j[g]
                        if f in a and g != 'ṃ':
                            c += 'ฺ'
                        k += 1
                    else:
                        if not g in j:
                            c += g
                            if h in a or (h == 'h' and l in a):
                                c += 'ฺ'
                            k += 1
                            if f == 'o' or f == 'e':
                                c += j[f]
                                k += 1
                            if f in n:
                                c += j["a"]
                        else:
                            k += 1

        if g in a:
            c += 'ฺ'
        c = re.sub(r"\`+", '"', c)
        return c