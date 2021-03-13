import re
from os import path

data_path = path.join(path.dirname(__file__), 'data')
default_words = path.join(data_path, 'words.dat')


class Stemer:
    def __init__(self):
        self.ends = ('ات', 'ان', 'ترین', 'تر','مان','مون','تان','تون','شون','شان','ند','ید','یم', 'م', 'ت', 'ش', 'یی', 'ی', 'های', 'ها', 'ٔ', '‌ا', '‌')
        self.words = default_words

    def stem(self, word):
        if len(word) == 0:
            print('vvvvvvvvvaaaaaaaaaaaa')
        for i in range(0, 2):
            for e in self.ends:
                if word.endswith(e) and len(word) > len(e) + 1:
                    word = word[:-len(e)]
        return word

    # def stem(self, word):
    #     bool = True
    #     while bool:
    #         if word.endswith('\u200c'):
    #             word = word[:-1]
    #         bool1 = word.endswith(('م', 'ت', 'ش', 'ی', 'ٔ', '‌ا'))
    #         if bool1:
    #             w = word[:-1]
    #             w.replace('ی','ي')
    #             if w in self.words:
    #                 word = word[:-1]
    #             else:
    #                 bool1 = False
    #         bool2 = word.endswith(('ات', 'ان', 'تر','ند','ید','یم', 'یی', 'ها'))
    #         if bool2:
    #             w = word[:-2]
    #             w.replace('ی','ي')
    #             if w in self.words:
    #                 word = word[:-2]
    #             else:
    #                 bool2 = False
    #
    #         bool3 = word.endswith(('مان','مون','تان','تون','شون','شان','های'))
    #         if bool3:
    #             w = word[:-3]
    #             w.replace('ی','ي')
    #             if w in self.words:
    #                 word = word[:-3]
    #             else:
    #                 bool3 = False
    #
    #         bool4 = word.endswith('ترین')
    #         if bool4:
    #             w = word[:-4]
    #             w.replace('ی','ي')
    #             if w in self.words:
    #                 word = word[:-4]
    #             else:
    #                 bool4 = False
    #         bool = bool1 or bool2 or bool3 or bool4
    #     return word
