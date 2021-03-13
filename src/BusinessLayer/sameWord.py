import re

compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]


class Samer():
    def __init__(self):
        self.expression = []

    def makeSame(self, word):
        with open("C:/Users/mahdis/PycharmProjects/phase2/BusinessLayer/data/same.dat", 'r', newline='\n') as default_words:
            for w in default_words:
                s = w.split(',')
                s[-1] = s[-1][:-2]
                if word in s:
                    return s[0]
            return word
