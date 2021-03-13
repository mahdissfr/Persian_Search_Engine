from DataLayer.constants import ConstantVars
from DataLayer.docIO import FileInOut
from .textOperations import FormWords
import numpy as np
import re
import time


class Index:

    def __init__(self):
        self.input = FileInOut()
        self.wordFormer = FormWords()
        self.constants = ConstantVars()
        self.dictionary = dict()
        self.posting_list = np.array([dict() for j in range(150000)])
        self.dicIndex = 0
        self.docIndex = 0
        self.c = 0

    def Filter(self, string, substr):
        return [str if not any(sub == str for sub in substr) else '**' for str in string]

    def makeDic(self, value, j):
        if value not in self.dictionary.keys() and value != '**':
            # print(self.dicIndex)
            # print(value)
            if '\n' in value:
                pass
            else:
                self.dictionary[value] = 1
                self.input.writeDic([value])
                self.posting_list[self.dicIndex][self.docIndex] = [j]
                self.dicIndex += 1
        elif value in self.dictionary.keys() and value != '**':
            if self.docIndex in self.posting_list[list(self.dictionary.keys()).index(value)].keys():
                self.posting_list[list(self.dictionary.keys()).index(value)][self.docIndex].append(j)
            else:
                self.posting_list[list(self.dictionary.keys()).index(value)][self.docIndex] = [j]

    def indexData(self):
        for n in range(15):
            data = self.input.readData('ir-news-'+str(n)+'.csv')
            for d in data["content"]:
                print(self.docIndex)
                self.docIndex += 1
                d = self.cleanContent(d)
                d = self.wordFormer.normalize(d)
                tokens = self.wordFormer.tokenize(d)
                self.c += len(tokens)
                tokens = list(filter(lambda a: a != '\n', tokens))
                tokens = self.wordFormer.uniform(tokens)
                # postaged_tokens = self.wordFormer.posTagging(tokens)
                stemmed_tokens = self.wordFormer.stemmWords(tokens)
                lemmatized_tokens = self.wordFormer.lemmatizeWords(stemmed_tokens)
                lemmatized_tokens = self.Filter(lemmatized_tokens, self.constants.punctuations() + ['\"','\"', '!', '', '\n'] + self.constants.StopWords())
                list(map(self.makeDic, lemmatized_tokens, [i for i in range(0, len(lemmatized_tokens))]))
            print('doc'+str(n)+': '+ str(self.docIndex))
        # for i in range(len(list(self.dictionary.keys()))):
        #     print(i)
        #     print(list(self.dictionary.keys()).pop(i))
        for i in range(0, len(self.posting_list)):
            self.input.writeDocID(self.posting_list[i])
            self.input.writePostingList([self.stringmaker(self.posting_list[i][key]) for key in self.posting_list[i].keys()])
        print('number of tokens')
        print(self.c)
        print(time.time())

    def getRelatedDocs(self, token):
        if token in self.dictionary:
            return self.posting_list[np.where(self.dictionary == token)][0]
        else:
            return {}

    def cleanContent(self, raw):
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleanText = re.sub(cleaner, ' ', raw)
        return cleanText

    def stringmaker(self, list):
        stri = ''
        for i in list:
            stri = stri + str(i) + ' '
        return stri
