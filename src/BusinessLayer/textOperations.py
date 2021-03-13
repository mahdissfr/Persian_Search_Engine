from hazm import *
from .stemmer import Stemer
from .lemmatizer import Lematizer
from .tokenizer import Tokenizer
from .normalizer import Normalizer
from .sameWord import Samer
import numpy as np


class FormWords:
    def __init__(self):
        self.lemma = Lematizer()
        self.stem = Stemer()
        self.Normalizer = Normalizer()
        self.tokenizer = Tokenizer()
        self.samer = Samer()
        # self.tagger = StanfordPOSTagger(model_filename='E:\pythonProjects/IRsystem/resources/models/persian.tagger',
        #                                 path_to_jar='E:\pythonProjects/IRsystem/resources/stanford-postagger.jar')

    def lemmatize(self, word):
        if word == '':
            print('vaaaaaaaaaaaaaaa')
            return ''
        return self.lemma.lemmatize(word)

    def stemming(self, word):
        return self.stem.stem(word)

    def tokenize(self, sentence):
        return self.tokenizer.word_tokenize(sentence)

    def normalize(self, sentence):
        return self.Normalizer.normaliz(sentence)

    # def posTagging(self, tokens):
    #     return self.tagger.tag(tokens)

    def stemmWords(self, words):
        # stemmedWords = np.array([{} for i in range(length)])
        # i = 0
        # for word in words:
        #     stemmedWords[i] = self.stemming(word)
        #     i += 1
        word = map(self.stemming, words)
        return list(word)

    def lemmatizeWords(self, words):
        # lemmatizedWords = []
        # for i in range(0, length):
        #     # if self.lemmatize(words[i], pos_of_word[i][1]) != '':
        #     lemmatizedWords.append(self.lemmatize(words[i], pos_of_word[i][1]))
        # pos_of_word = [pos_of_word[i][1] for i in range(len(pos_of_word))]
        word = map(self.lemmatize, words)
        return list(word)

    def uniform(self, tokens):
        # uniformWords = []
        # for token in tokens:
        #     uniformWords.append(self.samer.makeSame(token))
        token = map(self.samer.makeSame, tokens)
        return list(token)