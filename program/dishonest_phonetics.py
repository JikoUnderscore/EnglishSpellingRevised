from bs4 import BeautifulSoup
import requests
import json


def get_phonetics(word):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    try:
        html_text = requests.get(f'https://dictionary.cambridge.org/dictionary/english/{word}', headers=headers)

        soop = BeautifulSoup(html_text.content, features="lxml")

        n1 = soop.find('body')

        try:
            n2 = n1.find_all('span', {'class': 'usage dusage'})[0]
        except IndexError:
            n2 = n1.find_all('span', {'class': "pron dpron"})[0]

        ntootekst = n2.text
        if 'of' in ntootekst and 'past' not in ntootekst:
            redirect = n1.find_all('a', {'class': 'Ref'})[0]
            fin = get_phonetics(redirect.text)
        else:
            n2 = n1.find_all('span', {'class': "ipa dipa lpr-2 lpl-1"})[0]
            # n2 = n1.find_all('span', {'class': "ipa dipa lpr-2 lpl-1"})
            # fin = ntootekst.strip().replace('ˈ', '').replace('.', '')
            fin = n2.text

        with open('data/phonetic_dict.json', 'r+', encoding='utf-8') as js_file:
            data = json.load(js_file)
            data.update({word: fin})
            js_file.seek(0)
            json.dump(data, js_file, indent=4)

        return fin

        # for n in n2:
        #     print(n.text.strip())

    except Exception as ec:
        print(ec)


def __get_phonetics(word):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

    #
    # print('-----------------')
    # try:
    #     print('lexico\n'.upper())
    #     html_text = requests.get(f'https://www.lexico.com/en/definition/{word}')
    #
    #
    #     soop = BeautifulSoup(html_text.content, features="lxml")
    #
    #     n1 = soop.find('h3')
    #     n2 = n1.find_all('span')[1]
    #
    #     print(n2.text.replace('/', '').strip())
    #     # for n in n2:
    #     #     print(n.text.strip())
    #
    #
    # except IndexError as theError:
    #     print('not found\n', theError)
    #
    # print('-----------------')
    #
    # try:
    #     print('ldoceonline\n'.upper())
    #     html_text = requests.get(f'https://www.ldoceonline.com/dictionary/{word}', headers=headers)
    #
    #
    #     soop = BeautifulSoup(html_text.content, features="lxml")
    #     n1 = soop.find('body')
    #     n2 = n1.find_all('span', {'class': "PRON"})[0]
    #
    #     print(n2.text.strip())
    #     # for n in n2:
    #     #     print(n.text.strip())
    #
    # except Exception as ec:
    #     print(ec)

    print('-----------------')

    try:
        print('cambridge\n'.upper())
        html_text = requests.get(f'https://dictionary.cambridge.org/dictionary/english/{word}', headers=headers)

        soop = BeautifulSoup(html_text.content, features="lxml")

        n1 = soop.find('body')
        try:
            n2 = n1.find_all('span', {'class': 'usage dusage'})[0]
        except IndexError:
            n2 = n1.find_all('span', {'class': "pron dpron"})[0]

        print(n2)
        print(n2.text)
        if 'of' in n2.text and 'past' not in n2.text:
            redirect = n1.find_all('a', {'class': 'Ref'})[0]
            print(__get_phonetics(redirect.text))
        else:
            n2 = n1.find_all('span', {'class': "ipa dipa lpr-2 lpl-1"})[0]

            print(n2.text.strip())
        # for n in n2:
        #     print(n.text.strip())

    except Exception as ec:
        print(ec)

    print('-----------------')

    # # try:
    # #     print('merriam-webster\n'.upper())
    # #     html_text = requests.get(f'https://www.merriam-webster.com/dictionary/{word}')
    # #
    # #     soop = BeautifulSoup(html_text.content, features="lxml")
    # #
    # #     n1 = soop.find('body')
    # #     n2 = n1.find_all('span', {'class': 'pr'})
    # #
    # #     for n in n2:
    # #         print(n.text.strip())
    # # except Exception as ec:
    # #     print(ec)
    # #
    # # print('-----------------')
    #
    # try:
    #     print('collinsdictionary\n'.upper())
    #     html_text = requests.get(f'https://www.collinsdictionary.com/dictionary/english/{word}', headers=headers)
    #
    #     soop = BeautifulSoup(html_text.content, features="lxml")
    #
    #     n1 = soop.find('body')
    #     n2 = n1.find_all('span', {'class': 'pron type-'})[0]
    #
    #     print(n2.text.strip())
    #     # for n in n2:
    #     #     print(n.text.strip())
    #
    # except Exception as ec:
    #     print(ec)
    # print('-----------------')


if __name__ == '__main__':

    for word in ['took']:
        __get_phonetics(word)
