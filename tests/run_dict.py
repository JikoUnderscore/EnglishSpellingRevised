import unittest
from program.EnglishSpellingRevised import PrevodGovor
import json


prg = PrevodGovor()


with open('../program/data/TSR.json', 'r', encoding='utf=8') as dr:
    tsrDict: dict = json.load(dr)


class DictTests(unittest.TestCase):

    def test__prevod(self):
        for k, v in tsrDict.items():
            self.assertEqual(v, prg._prevod(k))


if __name__ == '__main__':
    unittest.main()
