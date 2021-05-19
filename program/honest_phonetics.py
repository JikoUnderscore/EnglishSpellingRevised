# #
# #
# # with open('prosesd.txt', 'r', encoding='utf-8') as rp:
# #     prosses = rp.read().split('\n')
# #
# # with open('non-prosesd.txt', 'r', encoding='utf-8') as rnp:
# #     nonprosses = rnp.read().split('\n')
# #
# # print(len(prosses),prosses)
# # print(len(nonprosses),nonprosses)
# #
# #
# # with open('end6.txt', 'w', encoding='utf-8') as end:
# #     for n in range(len(prosses)):
# #         if prosses[n].lower() != nonprosses[n].lower():
# #             end.write(f"{nonprosses[n].lower()} {prosses[n].lower()}\n")
#
#
# with open('cmudict2.dict', 'r', encoding=' utf-8') as cmu:
#     lst = cmu.read().split('\n')
#
# d = {}
#
# for line in lst:
#     data = line.split('\t')
#     k, v = data[0].strip(), data[1].strip()
#     d[k] = v
#
#
# import json
# with open('cmudict.json', 'w', encoding='utf-8') as jcmu:
#     json.dump(d, jcmu, indent=4)
import requests
import json
# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
# https://github.com/kiasar/Dictionary_crawler
from pprint import pprint






app_id = '654c4b04'                             # '<my app_id>'
app_key = 'd0e36ee214fcd3e71cc22f16f02b5f11'    # '<my app_key>'
language = 'en-gb'
word_id = 'cat'

url = 'https://od-api.oxforddictionaries.com/api/v2/entries/' + language + '/' + word_id.lower()
r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

res = json.loads(r.content)



unic_word = set()

for line in res["results"]:
    for line2 in line['lexicalEntries']:
        for line3 in line2['entries']:
            for line4 in line3['pronunciations']:
                unic_word.add(line4['phoneticSpelling'])
print(unic_word)

#print("code {}\n".format(r.status_code))
#print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))
