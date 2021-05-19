from functools import cache
from tkinter import *
from tkinter import messagebox, filedialog, colorchooser
from datetime import datetime
from threading import Timer
# import subprocess as subpc
import os
import re
import json
from nltk.tokenize import SyllableTokenizer
try:
    from .dishonest_phonetics import get_phonetics
    SSP = SyllableTokenizer()
except:
    from dishonest_phonetics import get_phonetics
import time
import configparser
from itertools import zip_longest

# https://www.ontrackreading.com/wordlists/one-syllable-words-by-vowel-sound



class PrevodGovor:

    punctuation: str = '''
                    "'!@#█½-$%’''^&*( '){}[]¿|._-`/?:;«»‹›—\,“”~ \n
                        '''
    with open(r'../program/data/exceptions.dict', 'r', encoding='utf=8') as exr:
        exceptionList: list = exr.read().split()

    with open(r'../program/data/exceptions.json', 'r', encoding='utf=8') as exr_js:
        exceptionDict: dict = json.load(exr_js)

    with open(r'../program/data/TSR.json', 'r', encoding='utf=8') as dr:
        tsrDict: dict = json.load(dr)

    with open(r'../program/data/phonetic_dict.json', 'r', encoding='utf=8') as phon:
        dctPhon: dict = json.load(phon)

    cons = ['b', 'd', 'dj', 'dʒ', 'ð', 'f', 'ɡ', 'h', 'hw', 'j', 'k', 'l', 'lj', 'm', 'n', 'nj', 'ŋ', 'p', 'r', 's',
            'sj', 'ʃ', 't', 'tj', 'tʃ', 'θ', 'θj', 'v', 'w', 'z', 'zj', 'ʒ', 'x', 'ʔ']

    vowels = ['ɑː', 'ɑ', 'ɒ', 'æ', 'aɪ', 'aʊ', 'ɛ', 'eɪ', 'ɪ', 'iː', 'e',
              'oʊ', 'ɔː', 'ɔɪ', 'ʊ', 'uː', 'ʌ', 'ə', 'i', 'u', 'əʊ']

    regexSerch = r"zj|θj|nj|lj|dʒ|dj|b|d|ð|f|ɡ|h|j|k|l|m|n|ŋ|p|r|s|sj|ʃ|t|tj|tʃ|θ|v|w|z|ʒ|x|ʔ|əʊ|uː|ɔɪ|ɔː|oʊ|iː|eɪ|eə|aʊ|aɪ|ɑː|ɑ|ɒ|æ|ɛ|ɪ|ʊ|ʌ|ə|i|u|e"

    popToggle = False
    popInfo = {}


    @staticmethod
    def _is_doble_cons(charSpisyk):
        a = ''
        for i in charSpisyk:
            if i[0] == a:
                return True
            a = i[-1]
        return False

    def _has_this_sounds(self, excludeSounds, soundsOfTheWord):
        b = []
        for nvowel in self.vowels:
            if nvowel not in excludeSounds:
                b.append(nvowel)
        a = []
        for sound in soundsOfTheWord:
            if sound in b:
                a.append(True)
        return a

    @cache
    def _prevod(self, word: str):
        if tsrWord := self.dctPhon.get(word):
            rawPhonee = tsrWord.replace('ˈ', "ˈ'")
        else:
            rawPhonee = get_phonetics(word)
            if rawPhonee is not None:
                rawPhonee = rawPhonee.replace('ˈ', "ˈ'")

        if rawPhonee is None:
            self.popToggle = True
            self.popInfo[word] = rawPhonee
            return 'ERROR'
            # raise Exception(f"'{phonee}' is not a word, try again --Custom error")

        phonee = rawPhonee.strip().replace("ˈ'", '').replace('.', '')


        # print([nvowel for nvowel in self.vowels if nvowel != 'eɪ' and nvowel != 'ə'])

        soundsOfTheWord = re.findall(self.regexSerch, phonee)
        print(word, soundsOfTheWord, phonee, rawPhonee)


        if ('əʊ' or 'oʊ') == soundsOfTheWord[-1] and word.endswith('ow'):
            word = re.sub(r"ow$", r"o", word, 1)
        elif 'se' == word[-2:] and 's' == soundsOfTheWord[-1]:
            word = re.sub(r"se$", r"ss", word, 1)

        if word[0] == 'k' != soundsOfTheWord[0]:
            word = word.replace("k", "'")
        elif word[0] == 'h' != soundsOfTheWord[0]:
            word = word.replace("h", "'")
        elif word[:2] == 'wh' and 'h' == soundsOfTheWord[0]:
            word = word.replace("wh", "'h")
        elif word[:2] == 'wr' and 'r' == soundsOfTheWord[0]:
            word = word.replace("wr", "'r")
        elif word[:2] == 'rh':
            word = word.replace('rh', 'r')
        elif word[:2] == 'th' and 't' == soundsOfTheWord[0]:
            word = word.replace('th', 't')
            if word[-1] == 'e':
                word = word.replace('e', '')

        if word.endswith('ough') and phonee.endswith('uː'):
            word = re.sub(r"ough$", r"oo", word, 1)

        if 'eə' in soundsOfTheWord:
            word = word.replace('ea', 'ai')
        if 'əʊl' in phonee and 'e' != word[-1]:
            word = re.sub(r"o[^a|e]", "oel", word, 1)
        if 'əʊ' in soundsOfTheWord and 'e' != word[-1] and not phonee.endswith('əʊ') and not word.endswith('ll'):
            word = re.sub(r"o", "oe", word, 1)
        if 'uː' in soundsOfTheWord:
            if not bool(re.compile(r"oo").findall(word)):
                word = re.sub(r"oe|o", "oo", word, 1)
        if phonee.endswith('uː'):
            word = re.sub(r"ue", "oo", word, 1)
        if word.endswith('gue') and (phonee.endswith('g') or phonee.endswith('ŋ')):
            word = re.sub(r"gue$", "g", word, 1)

        if len(spisykSfonemi := [x for x in re.split(r'ˈ|\.', rawPhonee) if x]) > 1 and not word.endswith('sure'):
            if bool(list(filter(re.compile(r"^'[^ɒæɛɪʊue]+([ɒæɛɪʊue])[^ɒæɛɪʊue]").match, spisykSfonemi))) and not self._is_doble_cons(charSpisyk := SSP.tokenize(word)):
                print('here')
                nooword = ''
                dble = False
                for phoneWord, charWord in zip_longest(spisykSfonemi, charSpisyk, fillvalue='none'):
                    if dble:
                        dble = False
                        charWord = charWord[0] + charWord
                    if bool(re.compile(r"^'[^ɒæɛɪʊʌəiue]+([ɒæɛɪʊʌəiue])[^ɒæɛɪʊʌəiue]").findall(phoneWord)):
                        dble = True

                    nooword += charWord
                word = nooword
                del nooword
                del dble
        if 'ea' in word and 'e' in soundsOfTheWord:
            nooword = ''
            for charWord, phoneWord in zip_longest(SSP.tokenize(word), SSP.tokenize(phonee), fillvalue='none'):
                if 'ea' in charWord and 'e' in phoneWord:
                    charWord = re.sub(r"ea", "e", charWord, 1)
                nooword += charWord
            word = nooword
            del nooword
        if 'ʊ' in phonee and len(spisykSfonemi) <= 1:
            word = re.sub(r'u(.)+', r'uu\1', word, 1)
        if 'ɜː' in phonee:
            word = re.sub(r"ir|ear", "er", word, 1)
        print(spisykSfonemi, SSP.tokenize(word))





        if ('eɪ' or 'eɪ' and 'ə') in soundsOfTheWord and not any(self._has_this_sounds(['eɪ', 'ə'], soundsOfTheWord)):
            if bool(re.compile(r"ay|ai|a.+e|eigh|aigh|ey|ei").findall(word)):
                if word.endswith(("eigh", "eighs", "eighed", "eighing")):
                    result = re.sub(r"eigh", "ay", word, 1)
                    return result
                if bool(re.compile(r"(ei)g([^h])").findall(word)):
                    result = re.sub(r"g", "'", word, 1)
                    return result
                return word
            result = re.sub(r"ea", "ai", word, 1)
            return result
        elif 'aɪ' in soundsOfTheWord and not any(self._has_this_sounds(['aɪ', 'ə'], soundsOfTheWord)):
            if not bool(re.compile(r"i.+e|ie|y|ye|igh|uy").findall(word)):
                result = re.sub(r"ig|i", "y", word, 1)
                return result
        elif 'iː' in soundsOfTheWord and not any(self._has_this_sounds(['iː', 'ə'], soundsOfTheWord)):
            if bool(re.compile(r"ie|ei|e").findall(word)):
                result = re.sub(r"ie|ei|e([ou])", "ee", word, 1)
                return result
        elif 'ʌ' in soundsOfTheWord and not any(self._has_this_sounds(['ʌ', 'ə'], soundsOfTheWord)):
            if not bool(re.compile(r"u").findall(word)) and len(spisykSfonemi) <= 1:
                result = re.sub(r"[ayouei]+(.)", r"u\1\1", word, 1)
                if result[-1] == 'e':
                    result = result.replace('e', '')
                return result
            elif bool(re.compile(r"ou").findall(word)):
                result = re.sub(r"[aouei]+", "u", word, 1)
                if result[-1] == 'e':
                    result = result.replace('e', '')
                return result
            elif len(spisykSfonemi) > 1:
                result = re.sub(r"[ou]", r"u", word, 1)
                if result[-1] == 'e':
                    result = result.replace('e', '')
                return result

        elif 'ʊ' in soundsOfTheWord and not any(self._has_this_sounds(['ʊ', 'ə'], soundsOfTheWord)):
            if bool(re.compile(r"oo").findall(word)):
                result = re.sub(r"oo", "uu", word, 1)
                return result
        elif 'ɪ' in soundsOfTheWord and not any(self._has_this_sounds(['ɪ', 'ə'], soundsOfTheWord)):
            if bool(re.compile(r"i.+e").findall(word)):
                result = re.sub(r"i(.+)e", r"i\1", word, 1)
                return result

        if 'full' in word:
            word = re.sub(r"full", "fuul", word, 1)

        nooword = ''
        for partPhonee, partWord in zip_longest(spisykSfonemi, SSP.tokenize(word), fillvalue='none'):
            if 'ɪ' in partPhonee:
                partWord = re.sub(r"u", "i", partWord, 1)
            elif 'ɔːk' in partPhonee and 'al' in partWord:
                partWord = re.sub(r"al", "au", partWord, 1)
            nooword += partWord

        word = nooword
        return word



    def govorene(self, *varr, **kvPair):
        print(' govorene', self, varr, kvPair)

    def prevod(self, *varr, **kvPair):
        initialText = mw.entryText.get("0.0", 'end-1c').lower()
        listOfwords = re.findall(r"\w+\b'\w+|[\w]+|\W", str(initialText))



        start = time.perf_counter()

        endText = ""
        for word in listOfwords:
            if word in self.punctuation:
                endText += word
            elif self.exceptionDict.get(word):
                endText += '<' + word + '>'
            # elif tsrWord := self.tsrDict.get(word):
            #     endText += tsrWord + '*'
            else:
                endText += self._prevod(word)
        print(time.perf_counter() - start)

        print(' prevod', self, varr, kvPair)
        mw.outText.delete(0.0, END)
        mw.outText.insert(0.0, endText)
        if self.popToggle:
            nword = ''
            nphonee = ''
            for k, v in self.popInfo.items():
                nword += ' ' + k
                nphonee += ' ' + str(v)
            messagebox.showinfo(title='Word erorr!', message=f"'{nword}' is not a word, try again \n\nFound '{nphonee}' expected 'IPA'")
            self.popToggle = False
            self.popInfo.clear()


class MenuBar:
    def __init__(self, mainScreen):
        menubar = Menu(mainScreen.root)
        mainScreen.root.config(menu=menubar)

        fileMenu = Menu(menubar, tearoff=0)
        fileMenu.add_command(label='Save rules', accelerator="Ctrl+S", command=self.seva_now)
        fileMenu.add_command(label='Show in explorer save folder', command=self.seva_folder)
        fileMenu.add_separator()
        fileMenu.add_command(label='Save rules as...', command=self.save_var)
        fileMenu.add_command(label='Load rules as...', command=self.load_var)
        fileMenu.add_separator()
        fileMenu.add_command(label='Open...', command=mainScreen.open_new)
        fileMenu.add_command(label='Save output txt as...')
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=lambda: mainScreen.destroy())
        menubar.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(menubar, tearoff=0)
        editMenu.add_command(label="Cut", accelerator="Ctrl+X",
                             command=lambda: mainScreen.focus_get().event_generate('<<Cut>>'))
        editMenu.add_command(label="Copy", accelerator="Ctrl+C",
                             command=lambda: mainScreen.focus_get().event_generate('<<Copy>>'))
        editMenu.add_command(label="Paste", accelerator="Ctrl+V",
                             command=lambda: mainScreen.focus_get().event_generate('<<Paste>>'))
        editMenu.add_command(label="Select all", accelerator="Ctrl+A",
                             command=lambda: mainScreen.focus_get().event_generate('<<SelectAll>>'))
        editMenu.add_separator()
        editMenu.add_command(label="Undo", accelerator="Ctrl+Z", command=mainScreen.entryText.edit_undo)
        editMenu.add_command(label="Redo", accelerator="Ctrl+Y", command=mainScreen.entryText.edit_redo)
        menubar.add_cascade(label="Edit", menu=editMenu)

        # View = Menu(menubar, tearoff=0)
        #
        # menubar.add_cascade(label="View", menu=View)

        manage = Menu(menubar, tearoff=0)
        # manage.add_checkbutton(label='Save not found words', var=root.ddump)
        # manage.add_command(label='Update dump number !!!', command=mainScreen.dump_filen_update)
        # manage.add_command(label='Open dump file...', command=mainScreen.otvori_dump_file)
        # manage.add_separator()
        manage.add_checkbutton(label='enable auto converter', var=mainScreen.autoTranslator, command=mainScreen.automatic_translator)
        manage.add_separator()
        manage.add_command(label="Change background color", command=mainScreen.chose_a_colour)
        # manage.add_checkbutton(label='Synchronize vertical scrolling', command=root.sinc_scroll, var=root.sinc_gh)
        menubar.add_cascade(label="Options", menu=manage)

        # somenu = Menu(menubar, tearoff=0)
        # somenu.add_command(label="Do nothing...", command=mainScreen.mnoff)
        # somenu.add_command(label="Change background color", command=mainScreen.izberi_color)
        # menubar.add_cascade(label="So...", menu=somenu)

        elp = Menu(menubar, tearoff=0)
        elp.add_command(label='get to programing')
        mee = Menu(elp, tearoff=0)
        mee.add_command(label='What a does')
        mee.add_command(label='What b does')
        mee.add_command(label='What c does')
        mee.add_command(label='What d does')
        elp.add_cascade(label='Explain', menu=mee)
        menubar.add_cascade(label="HELP", menu=elp)

        mainScreen.root.bind('<Control-s>', self.seva_now)

    @staticmethod
    def seva_folder():
        currentDir = os.getcwd()
        try:
            os.mkdir(currentDir + "\\data\\")
            os.mkdir(currentDir + "\\data\\saved\\")
        except FileExistsError as erer:
            print(erer)

        os.startfile(f"{currentDir}\\data\\saved")

    def seva_now(self, *args):
        print(args)

        timeYearMonthDay = "".join(datetime.now().strftime("%Y-%m-%d h%H%M%S"))

        currentDir = os.getcwd()
        try:
            os.mkdir(currentDir + "\\data\\")
            os.mkdir(currentDir + "\\data\\saved\\")
        except FileExistsError as erer:
            print(erer)

        with open(f"data\\saved\\saved at {timeYearMonthDay}.dat", "w", encoding='utf-8') as s:
            self.zapyzi(s)

    def save_var(self):
        sf = filedialog.asksaveasfilename(
            initialfile="Untitle.dat",
            defaultextension=".dat",
            filetypes=[("All files", "*.*"),
                       ("Data files", "*.dat")])
        if sf:
            with open(sf, "w", encoding='utf-8') as s:
                self.zapyzi(s)

    @staticmethod
    def zapyzi(s):
        print('zapyzi', s)

        # from checkboxes import chw
        # s.write(str(chw.ch1()) + ' ' + str(chw.n1.get()) + '\n')
        # s.write(str(chw.ch2()) + ' ' + str(chw.n2.get()) + '\n')
        # s.write(str(chw.ch3()) + ' ' + str(chw.n3.get()) + '\n')
        # s.write(str(chw.ch4()) + ' ' + str(chw.n4.get()) + '\n')
        # s.write(str(chw.ch5()) + ' ' + str(chw.n5.get()) + '\n')
        # s.write(str(chw.ch6()) + ' ' + str(chw.n6.get()) + '\n')
        # s.write(str(chw.ch7()) + ' ' + str(chw.n7.get()) + '\n')
        # s.write(str(chw.ch8()) + ' ' + str(chw.n8.get()) + '\n')
        # s.write(str(chw.ch9()) + ' ' + str(chw.n9.get()) + '\n')
        # s.write(str(chw.ch10()) + ' ' + str(chw.n10.get()) + '\n')
        # s.write(str(chw.ch11()) + ' ' + str(chw.n11.get()) + '\n')
        # s.write(str(chw.ch12()) + ' ' + str(chw.n12.get()) + '\n')
        # s.write(str(chw.ch13()) + ' ' + str(chw.n13.get()) + '\n')
        # s.write(str(chw.ch1301()) + ' '+str(chw.n1301.get()) + '\n')
        # s.write(str(chw.ch14()) + ' ' + str(chw.n14.get()) + '\n')
        # s.write(str(chw.ch15()) + ' ' + str(chw.n15.get()) + '\n')
        # s.write(str(chw.ch16()) + ' ' + str(chw.n16.get()) + '\n')
        # s.write(str(chw.ch17()) + ' ' + str(chw.n17.get()) + '\n')
        # s.write(str(chw.ch18()) + ' ' + str(chw.n18.get()) + '\n')
        # s.write(str(chw.ch19()) + ' ' + str(chw.n19.get()) + '\n')
        # s.write(str(chw.ch20()) + ' ' + str(chw.n20.get()) + '\n')
        # s.write(str(chw.ch21()) + ' ' + str(chw.n21.get()) + '\n')
        # s.write(str(chw.ch22()) + ' ' + str(chw.n22.get()) + '\n')
        # s.write(str(chw.ch23()) + ' ' + str(chw.n23.get()) + '\n')
        # s.write(str(chw.ch24()) + ' ' + str(chw.n24.get()) + '\n')
        # s.write(str(chw.ch25()) + ' ' + str(chw.n25.get()) + '\n')
        # s.write(str(chw.ch26()) + ' ' + str(chw.n26.get()) + '\n')
        # s.write(str(chw.ch2601()) + ' '+str(chw.n2601.get()) + '\n')
        # s.write(str(chw.ch27()) + ' ' + str(chw.n27.get()) + '\n')
        # s.write(str(chw.ch28()) + ' ' + str(chw.n28.get()) + '\n')
        # s.write(str(chw.ch29()) + ' ' + str(chw.n29.get()) + '\n')
        # s.write(str(chw.ch30()) + ' ' + str(chw.n30.get()) + '\n')
        # s.write(str(chw.ch31()) + ' ' + str(chw.n31.get()) + '\n')
        # s.write(str(chw.ch32()) + ' ' + str(chw.n32.get()) + '\n')
        # s.write(str(chw.ch33()) + ' ' + str(chw.n33.get()) + '\n')
        # s.write(str(chw.ch34()) + ' ' + str(chw.n34.get()) + '\n')
        # s.write(str(chw.ch35()) + ' ' + str(chw.n35.get()) + '\n')
        # s.write(str(chw.ch36()) + ' ' + str(chw.n36.get()) + '\n')
        # s.write(str(chw.ch37()) + ' ' + str(chw.n37.get()) + '\n')
        # s.write(str(chw.ch38()) + ' ' + str(chw.n38.get()) + '\n')
        # s.write(str(chw.ch39()) + ' ' + str(chw.n39.get()) + '\n')
        # s.write(str(chw.ch40()) + ' ' + str(chw.n40.get()) + '\n')
        # s.write(str(chw.ch41()) + ' ' + str(chw.n41.get()) + '\n')
        # s.write(str(chw.ch42()) + ' ' + str(chw.n42.get()) + '\n')
        # s.write(str(chw.air()) + ' ' +     str(chw.nr1.get()) + '\n')
        # s.write(str(chw.ar()) + ' ' +      str(chw.nr2.get()) + '\n')
        # s.write(str(chw.eer()) + ' ' +     str(chw.nr3.get()) + '\n')
        # s.write(str(chw.oor()) + ' ' +     str(chw.nr4.get()) + '\n')
        # s.write(str(chw.sp_oundt()) + ' ' +str(chw.nsp0.get()) + '\n')
        # s.write(str(chw.sp_kw()) + ' ' +   str(chw.nsp1.get()) + '\n')
        # s.write(str(chw.sp_ngk()) + ' ' +  str(chw.nsp2.get()) + '\n')
        # s.write(str(chw.sp_ago()) + ' ' +  str(chw.nsp3.get()) + '\n')
        # s.write(str(chw.sp_yoo()) + ' ' +  str(chw.nsp4.get()) + '\n')
        # s.write(str(chw.sp_ki_ke_k()) +' '+str(chw.nsp5.get()) + '\n')
        # s.write(str(chw.sp_tion()) + ' ' + str(chw.nsp6.get()) + '\n')
        # s.write(str(chw.sp_sion()) + ' ' + str(chw.nsp7.get()) + '\n')
        # s.write(str(chw.sp_orro()) + ' ' + str(chw.nsp8.get()) + '\n')
        # s.write(str(chw.sp_egzx()) + ' ' + str(chw.nsp9.get()) + '\n')
        # s.write(str(chw.sp_a_bout()) + ' '+str(chw.nsp10.get()) + '\n')
        # s.write(str(chw.sp_sof_a()) + ' '+ str(chw.nsp11.get()) + '\n')
        # s.write(str(chw.sp_eezz()) + ' ' + str(chw.nsp12.get()) + '\n')
        # s.write(str(chw.sp_esz()) + ' ' +  str(chw.nsp13.get()) + '\n')
        # s.write(str(chw.sp_s_e_i_y()) + ' ' + str(chw.nsp14.get()) + '\n')
        # s.write(str(chw.sp_edd()) + ' ' +  str(chw.nsp15.get()) + '\n')
        # s.write(str(chw.sp_ett()) + ' ' +  str(chw.nsp16.get()) + '\n')
        # s.write(str(chw.sp_eedd()) + ' ' + str(chw.nsp17.get()) + '\n')
        # s.write(str(chw.sp_x_end()) + ' ' +str(chw.nsp18.get()) + '\n')
        # s.write(str(chw.nsp19.get()) + '\n')
        # s.write(str(','.join(chw.excld())) + ' ' + str(chw.nsp20.get()) + '\n')
        # s.write(str(chw.nsp21.get()) + '\n')
        # s.write(str(chw.nsp22.get()) + '\n')

    def load_var(self):
        print(' zaredi', self)
        # from checkboxes import chw
        loadFileName = filedialog.askopenfilename(
            defaultextension=".dat",
            filetypes=[("Data files", "*.dat")])
        if loadFileName:
            with open(loadFileName, "r", encoding='utf-8') as loadf:
                ll = loadf.read().split()

        #     chw.t1.set(ll[0]);      chw.n1.set(ll[1])
        #     chw.t2.set(ll[2]);      chw.n2.set(ll[3])
        #     chw.t3.set(ll[4]);      chw.n3.set(ll[5])
        #     chw.t4.set(ll[6]);      chw.n4.set(ll[7])
        #     chw.t5.set(ll[8]);      chw.n5.set(ll[9])
        #     chw.t6.set(ll[10]);     chw.n6.set(ll[11])
        #     chw.t7.set(ll[12]);     chw.n7.set(ll[13])
        #     chw.t8.set(ll[14]);     chw.n8.set(ll[15])
        #     chw.t9.set(ll[16]);     chw.n9.set(ll[17])
        #     chw.t32.set(ll[18]);    chw.n32.set(ll[19])
        #     chw.t11.set(ll[20]);    chw.n11.set(ll[21])
        #     chw.t12.set(ll[22]);    chw.n12.set(ll[23])
        #     chw.t13.set(ll[24]);    chw.n13.set(ll[25])
        #     chw.t1301.set(ll[26]);  chw.n1301.set(ll[27])
        #     chw.t14.set(ll[28]);    chw.n14.set(ll[29])
        #     chw.t15.set(ll[30]);    chw.n15.set(ll[31])
        #     chw.t16.set(ll[32]);    chw.n16.set(ll[33])
        #     chw.t17.set(ll[34]);    chw.n17.set(ll[35])
        #     chw.t18.set(ll[36]);    chw.n18.set(ll[37])
        #     chw.t19.set(ll[38]);    chw.n19.set(ll[39])
        #     chw.t20.set(ll[40]);    chw.n20.set(ll[41])
        #     chw.t21.set(ll[42]);    chw.n21.set(ll[43])
        #     chw.t22.set(ll[44]);    chw.n22.set(ll[45])
        #     chw.t23.set(ll[46]);    chw.n23.set(ll[47])
        #     chw.t24.set(ll[48]);    chw.n24.set(ll[49])
        #     chw.t25.set(ll[50]);    chw.n25.set(ll[51])
        #     chw.t26.set(ll[52]);    chw.n26.set(ll[53])
        #     chw.t2601.set(ll[54]);  chw.n2601.set(ll[55])
        #     chw.t27.set(ll[56]);    chw.n27.set(ll[57])
        #     chw.t28.set(ll[58]);    chw.n28.set(ll[59])
        #     chw.t29.set(ll[60]);    chw.n29.set(ll[61])
        #     chw.t30.set(ll[62]);    chw.n30.set(ll[63])
        #     chw.t31.set(ll[64]);    chw.n31.set(ll[65])
        #     chw.t10.set(ll[66]);    chw.n10.set(ll[67])
        #     chw.t33.set(ll[68]);    chw.n33.set(ll[69])
        #     chw.t34.set(ll[70]);    chw.n34.set(ll[71])
        #     chw.t35.set(ll[72]);    chw.n35.set(ll[73])
        #     chw.t36.set(ll[74]);    chw.n36.set(ll[75])
        #     chw.t37.set(ll[76]);    chw.n37.set(ll[77])
        #     chw.t38.set(ll[78]);    chw.n38.set(ll[79])
        #     chw.t39.set(ll[80]);    chw.n39.set(ll[81])
        #     chw.t40.set(ll[82]);    chw.n40.set(ll[83])
        #     chw.t41.set(ll[84]);    chw.n41.set(ll[85])
        #     chw.t42.set(ll[86]);    chw.n42.set(ll[87])
        #     chw.tr1.set(ll[88]);    chw.nr1.set(ll[89])
        #     chw.tr2.set(ll[90]);    chw.nr2.set(ll[91])
        #     chw.tr3.set(ll[92]);    chw.nr3.set(ll[93])
        #     chw.tr4.set(ll[94]);    chw.nr4.set(ll[95])
        #     chw.tsp0.set(ll[96]);   chw.nsp0.set(ll[97])
        #     chw.tsp1.set(ll[98]);   chw.nsp1.set(ll[99])
        #     chw.tsp2.set(ll[100]);  chw.nsp2.set(ll[101])
        #     chw.tsp3.set(ll[102]);  chw.nsp3.set(ll[103])
        #     chw.tsp4.set(ll[104]);  chw.nsp4.set(ll[105])
        #     chw.tsp5.set(ll[106]);  chw.nsp5.set(ll[107])
        #     chw.tsp6.set(ll[108]);  chw.nsp6.set(ll[109])
        #     chw.tsp7.set(ll[110]);  chw.nsp7.set(ll[111])
        #     chw.tsp8.set(ll[112]);  chw.nsp8.set(ll[113])
        #     chw.tsp9.set(ll[114]);  chw.nsp9.set(ll[115])
        #     chw.tsp10.set(ll[116]); chw.nsp10.set(ll[117])
        #     chw.tsp11.set(ll[118]); chw.nsp11.set(ll[119])
        #     chw.tsp12.set(ll[120]); chw.nsp12.set(ll[121])
        #     chw.tsp13.set(ll[122]); chw.nsp13.set(ll[123])
        #     chw.tsp14.set(ll[124]); chw.nsp14.set(ll[125])
        #     chw.tsp15.set(ll[126]); chw.nsp15.set(ll[127])
        #     chw.tsp16.set(ll[128]); chw.nsp16.set(ll[129])
        #     chw.tsp17.set(ll[130]); chw.nsp17.set(ll[131])
        #     chw.tsp18.set(ll[132]); chw.nsp18.set(ll[133])
        #     chw.nsp19.set(ll[134])
        #     chw.tsp20.set(ll[135]); chw.nsp20.set(ll[136])
        #     chw.nsp21.set(ll[137])
        #     chw.nsp22.set(ll[138])


class MainWindow:
    def __init__(self, window):
        try:
            config.read('data/settings.ini')
            xLoc = config.get('window_location', 'x')
            yLoc = config.get('window_location', 'y')
        except Exception:
            xLoc = 150
            yLoc = 100

        window.title("Text converter - INPROGRESS BUILD")
        window.geometry(f"1280x630+{xLoc}+{yLoc}")
        # window.iconbitmap('data/ico/icon2.ico')
        # self.img2 = PhotoImage(file='data/speaker2.png')
        self.root = window
        # self.r_d = IntVar()
        self.autoTranslator = IntVar()
        # self.ddump = IntVar()
        # self.sinc_gh = IntVar()
        font_specs = ("ubuntu", 14, "bold")

        self.f_i = "#606060"
        window.config(bg=self.f_i)

        self.pyrvi_red = Frame(window, bg=self.f_i)  # , bg='red'
        self.pyrvi_red.pack(fill=X, side=TOP)
        self.vtori_red = Frame(window, bg=self.f_i)  # , bg='black'
        self.vtori_red.pack(fill=X, side=TOP)
        self.treti_red = Frame(window, bg=self.f_i)  # , bg='blue'
        self.treti_red.pack(side=TOP)
        # self.cetvyrti_red = Frame(window, bg=self.f_i)  # , bg='yellow'
        # self.cetvyrti_red.pack(fill=X, side=TOP)

        self.leftLabel = Label(self.pyrvi_red, text="Enter Text Below:", font=font_specs, bg=self.f_i)
        self.leftLabel.pack(expand=True, side=LEFT, anchor=SE)
        self.enterButton = Button(self.pyrvi_red, state=NORMAL, text="Enter!", command=prg.prevod, height=1, width=8,
                                  font=("Times New Roman", 16, "bold"), bg=self.f_i)
        self.enterButton.pack(expand=True, side=LEFT)

        self.rightLablel = Label(self.pyrvi_red, text="Output Text Below:", font=font_specs, bg=self.f_i)
        self.rightLablel.pack(expand=True, side=LEFT, anchor=SW)

        self.entryText = Text(self.vtori_red, undo=True, wrap=WORD)  # ,  width=78, height=24,
        self.entryText.pack(expand=True, side=LEFT, anchor=E)
        self.scrBar = Scrollbar(self.vtori_red, orient="vertical")
        self.scrBar.pack(side=LEFT, fill=Y)
       # self.spkbt = Button(master=self.entryText, text='SPEAK!', command=prg.govorene, image=self.img2, bg=self.f_i)
       # self.spkbt.place(relx=0.956, rely=0.926)
        self.outText = Text(self.vtori_red, wrap=WORD)
        self.outText.pack(expand=True, side=LEFT, anchor=W)

        # self.dop1 = Label(self.treti_red, text="word1/word2/word3/word4", bg=self.f_i)
        # self.dop1.grid(row=1, column=5, columnspan=4)
        # self.dop2 = Label(self.treti_red, text="Apply choses word to all words with dashes!", bg=self.f_i)
        # self.dop2.grid(row=1, column=0, columnspan=2)
        # self.dop3 = Label(self.treti_red, text="default", bg=self.f_i)
        # self.dop3.grid(row=2, column=0, sticky=E)
        # self.rbb1 = Radiobutton(self.treti_red, var=self.r_d, value=0, bg=self.f_i)
        # self.rbb1.grid(row=2, column=1, sticky=W)
        # self.rbb2 = Radiobutton(self.treti_red, var=self.r_d, value=3, bg=self.f_i)
        # self.rbb2.grid(row=2, column=5)
        # self.rbb3 = Radiobutton(self.treti_red, var=self.r_d, value=2, bg=self.f_i)
        # self.rbb3.grid(row=2, column=6)
        # self.rbb4 = Radiobutton(self.treti_red, var=self.r_d, value=1, bg=self.f_i)
        # self.rbb4.grid(row=2, column=8)
        # self.rbb5 = Radiobutton(self.treti_red, var=self.r_d, value=4, bg=self.f_i)
        # self.rbb5.grid(row=2, column=7)
        # self.v_dump = StringVar()
        # self.dump = Label(self.treti_red, text="Dump:(number)   //Manage -> Update dump count//", bg=self.f_i)
        # self.dump.grid(row=1, column=20, sticky=E, padx=200)

        # Label(self.cetvyrti_red, text="Raw Text Below:").pack(side=LEFT)
        # self.btr = Button(self.cetvyrti_red, text="Show raw text!",
        #                   command=lambda: [self.textboxraw.delete(0.0, END), self.textboxraw.insert(0.0, prg.prevod())],
        #                   bg=self.f_i)
        # self.btr.pack(side=LEFT)
        # self.textboxraw = Text(self.cetvyrti_red, width=50, height=2, wrap=WORD)
        # self.textboxraw.pack(side=LEFT)

        # self.customLetterWindow = Button(self.cetvyrti_red, text="Open custom \n letters window!",
        #                                  command=self._togol_custom_letters_button, font=("Times New Roman", 12, "bold"),
        #                                  bg=self.f_i)
        # self.customLetterWindow.pack(side=RIGHT)

        self.mRightButton = Menu(window, tearoff=False)
        self.mRightButton.add_command(label="Cut", accelerator="Ctrl+X",
                                      command=lambda: window.focus_get().event_generate('<<Cut>>'))
        self.mRightButton.add_command(label="Copy", accelerator="Ctrl+C",
                                      command=lambda: window.focus_get().event_generate('<<Copy>>'))
        self.mRightButton.add_command(label="Paste", accelerator="Ctrl+V",
                                      command=lambda: window.focus_get().event_generate('<<Paste>>'))
        self.mRightButton.add_command(label="Select all", accelerator="Ctrl+A",
                                      command=lambda: window.focus_get().tag_add("sel", "1.0", "end"))

        self.entryText.bind('<Button-3>', self._right_mouse_button_click)
        self.outText.bind('<Button-3>', self._right_mouse_button_click)
        # self.textboxraw.bind('<Button-3>', self.desen_btn)
        self.entryText.bind('<Shift-Return>', lambda x: print(x))
        self.entryText.bind('<Return>', prg.prevod)


        self.lineAtBottom = Label(window, text='Welcome to text converter 9000', relief=SUNKEN, anchor=W, bg=self.f_i)
        self.lineAtBottom.place(anchor=S, relx=0.50, rely=1, relwidth=1)
        self.menubar = MenuBar(self)


    def _right_mouse_button_click(self, ev: EventType):
        print(ev)
        self.mRightButton.tk_popup(ev.x_root, ev.y_root)

    def chose_a_colour(self):
        backroundColour = colorchooser.askcolor()[1]
        print(backroundColour)
        self.f_i = backroundColour
        self.root.configure(bg=f"{backroundColour}")
        self.pyrvi_red.configure(bg=f"{backroundColour}")
        self.vtori_red.configure(bg=f"{backroundColour}")
        self.treti_red.configure(bg=f"{backroundColour}")
        # self.cetvyrti_red.configure(bg=f"{backroundColour}")
        self.leftLabel.configure(bg=f"{backroundColour}")
        self.enterButton.configure(bg=f"{backroundColour}")
        self.rightLablel.configure(bg=f"{backroundColour}")
        # self.dop1.configure(bg=f"{backroundColour}")
        # self.dop2.configure(bg=f"{backroundColour}")
        # self.dop3.configure(bg=f"{backroundColour}")
        # self.rbb1.configure(bg=f"{backroundColour}")
        # self.rbb2.configure(bg=f"{backroundColour}")
        # self.rbb3.configure(bg=f"{backroundColour}")
        # self.rbb4.configure(bg=f"{backroundColour}")
        # self.rbb5.configure(bg=f"{backroundColour}")
        # self.dump.configure(bg=f"{backroundColour}")
        # self.btr.configure(bg=f"{backroundColour}")
        # self.customLetterWindow.configure(bg=f"{backroundColour}")
        self.lineAtBottom.configure(bg=f"{backroundColour}")
        # self.spkbt.configure(bg=f"{backroundColour}")

    # def _togol_custom_letters_button(self):
    #     print(' toggle buton', self)
    #     # from checkboxes import ruw
    #     # ruw.open_window()
    #     # self.customLetterWindow.config(text='Toggle custom \n letters window!', command=ruw.toggle_window)

    def automatic_translator(self):

        if self.autoTranslator.get() == 1:
            self.entryText.unbind('<Return>')
            self.entryText.unbind('<Shift-Return>')
            # self.enterButton.config(state=DISABLED)
            prg.prevod()
            Timer(0.1, self.automatic_translator).start()
            print('..RUNNING..')
        else:
            self.entryText.bind('<Shift-Return>', lambda x: print(x))
            self.entryText.bind('<Return>', prg.prevod)
            # self.enterButton.config(state=NORMAL)
            self.lineAtBottom["text"] = 'Welcome to text converter 9000 - AUTOMATIC CONVERTER IS DISABLED'
            self.lineAtBottom["bg"] = self.f_i
            print('not runnig')
        self.lineAtBottom["text"] = 'Welcome to text converter 9000 - AUTOMATIC CONVERTER IS ACTIVE'
        self.lineAtBottom["bg"] = '#9b3335'

    # def remove_dash(self) -> int:
    #     a = self.r_d.get()
    #     return a

    # def otvori_dump_file(self):
    #     subpc.Popen(["Notepad.exe", "MISSING_WORDS/missing_word_list.txt"])

    # def dump_filen_update(self):
    #     with open("MISSING_WORDS/missing_word_list.txt", "r") as llc:
    #         c = len(list(llc))
    #         self.dump.config(text=f"Dump file size is {c} lines long")

    # def mnoff(self):
    #     for c in range(0, 100):
    #         if messagebox.askretrycancel(title="WOT", message=str(c) + " |What did you expext") is True:
    #             messagebox.showwarning(title="WARNING", message="you dun goofed")
    #         else:
    #             if messagebox.askyesno(title="HAHAHAHAHAHAHA", message="DO YOU WANT TO ~QUIT~") is True:
    #                 quit()
    #             else:
    #                 messagebox.showwarning(title="WARNING", message="you dun goofed AGAIN")
    #         c += 1

    def open_new(self):
        fileName = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All files", "*.*"),
                       ("Text files", "*.txt")])
        if fileName:
            self.entryText.delete(1.0, END)
            with open(fileName, "r") as f:
                self.entryText.insert(1.0, f.read())

    # def sinc_scroll(self):
    #     if self.sinc_gh.get() == 0:
    #         print('sinhron ne raboti')
    #     else:
    #
    #
    #         # self.entryText.bind('<MouseWheel>', self.scrBar)
    #         # self.outText.bind('<MouseWheel>', self.scrBar)
    #         self.scrBar.config(command=lambda *args: [self.entryText.yview(*args), self.outText.yview(*args)])
    #         self.entryText.config(yscrollcommand=self.scrBar.set)
    #         self.outText.config(yscrollcommand=self.scrBar.set)
    #         # self.entryText.unbind("<MouseWheel>", lambda e: print(e))
    #         # self.outText.unbind("<MouseWheel>", lambda e: print(e))
    #
    #         # self.outText.config(command=self.entryText.yview)
    #         # def OnMouseWheel(e):
    #         #     self.scrBar.yview(-1*(e.delta/120), "units")
    #         # self.entryText.bind('<MouseWheel>', OnMouseWheel)
    #
    #         print('sinhron raboti')


def close_window():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        config['window_location'] = {'x': rt.winfo_x(), 'y': rt.winfo_y()}
        with open('data/settings.ini', 'w') as setgs:
            config.write(setgs)
        rt.destroy()



if __name__ == "__main__":
    rt = Tk()
    SSP = SyllableTokenizer()
    config = configparser.ConfigParser()
    prg = PrevodGovor()
    mw = MainWindow(rt)
    rt.protocol("WM_DELETE_WINDOW", close_window)
    rt.mainloop()
