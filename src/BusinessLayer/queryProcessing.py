from .textOperations import FormWords
from DataLayer.constants import ConstantVars
import numpy as np


class Query:
    def __init__(self, i):
        self.wordFormer = FormWords()
        self.indexTasks = i
        self.constants = ConstantVars()
        self.relatedDocs = np.array([dict() for i in range(100)])
        self.notRelatedDocs = np.array([dict() for i in range(100)])
        self.notRelatedCounts = 0

    def processQuery(self, query):
        query_tokens = self.wordFormer.tokenize(query)
        for token in query_tokens:
            if token in self.constants.punctuations() or token in self.constants.StopWords():
                query_tokens.remove(token)
        print('query tokens')
        print(query_tokens)
        postaged_tokens = self.wordFormer.posTagging(query_tokens)
        stemmed_tokens = self.wordFormer.stemmWords(query_tokens, len(query_tokens))
        lemmatized_tokens = self.wordFormer.lemmatizeWords(stemmed_tokens, postaged_tokens, len(query_tokens))
        i = j = 0
        k = -1
        not_include = False
        order = False
        orderTokens = [[] for i in range(5)]
        for token in lemmatized_tokens:
            if token == "\"" and order == False:
                k += 1
                order = True
                continue
            if token == "\"" and order == True:
                order = False
                continue
            if order:
                orderTokens[k].append(token)
                continue
            if token == "!":
                not_include = True
                self.notRelatedCounts += 1
                continue
            if not_include:
                self.notRelatedDocs[j] = self.indexTasks.getRelatedDocs(token)
                not_include = False
            else:
                self.relatedDocs[i] = self.indexTasks.getRelatedDocs(token)
                i += 1
        print('related docs')
        print(self.relatedDocs)
        related_result, relatedPos = self.merge(self.relatedDocs, i)
        docs = np.array([dict() for i in range(10)])
        doc_pos = np.array([dict() for i in range(10)])
        j = 0
        if related_result != []:
            docs[j] = related_result
            doc_pos[j] = relatedPos
            j += 1
        for i in range(0, k-1):
            phrase_container, phrase_pos = self.phraseContainerDocs(orderTokens[i])
            docs[j] = phrase_container
            doc_pos[j] = phrase_pos
            print('phrase')
            print(phrase_container)
            print(phrase_pos)
            j += 1
        final_result, final_pos = self.finalMerge(docs, doc_pos, j)
        relateds_and_not_unrelateds, related_pos = self.notMerge(final_result, final_pos)
        print(relateds_and_not_unrelateds)
        print(related_pos)
        return relateds_and_not_unrelateds, related_pos

    def merge(self, docs, len):
        answer = []
        postingAns = []
        if len == 0:
            return [], []
        elif len == 1:
            return list(docs[0].keys()), list(docs[0].values())
        else:
            p2 = list(docs[0].keys())
            postings2 = []
            for docID in p2:
                postings2.append(docs[0][docID])
            i = 1
            while i < len:
                p1 = list(docs[i].keys())
                postings1 = []
                for docID in p1:
                    postings1.append(docs[i][docID])
                i += 1
                while p1 != [] and p2 != []:
                    if p1[0] == p2[0]:
                        answer.append(p1[0])
                        postingAns.append(postings1[0] + postings2[0])
                        p1.remove(p1[0])
                        p2.remove(p2[0])
                        postings1.remove(postings1[0])
                        postings2.remove(postings2[0])
                    elif p1[0] < p2[0]:
                        p1.remove(p1[0])
                        postings1.remove(postings1[0])
                    else:
                        p2.remove(p2[0])
                        postings2.remove(postings2[0])
                p2 = answer
                postings2 = postingAns
        print('docc')
        print(answer)
        print(postingAns)
        return answer, postingAns

    def finalMerge(self, docs, docPos, length):
        answer = []
        docPosAns = []
        if length == 0:
            return [],[]
        elif length == 1:
            return list(docs[0]), list(docPos[0])
        else:
            p2 = list(docs[0])
            docPos2 = list(docPos[0])
            i = 1
            while i < length:
                p1 = list(docs[i])
                docPos1 = list(docPos[i])
                i += 1
                while p1 != [] and p2 != []:
                    if p1[0] == p2[0]:
                        answer.append(p1[0])
                        docPosAns.append(docPos1[0] + docPos2[0])
                        p1.remove(p1[0])
                        p2.remove(p2[0])
                        docPos1.remove(docPos1[0])
                        docPos2.remove(docPos2[0])
                    elif p1[0] < p2[0]:
                        p1.remove(p1[0])
                        docPos1.remove(docPos1[0])
                    else:
                        p2.remove(p2[0])
                        docPos2.remove(docPos2[0])
                p2 = answer
                docPos2 = docPosAns
        print('docc and double quote')
        print(answer)
        print(docPosAns)
        return answer, docPosAns

    def notMerge(self, relatedDocs, relatedPos):
        print('no relate')
        print(self.notRelatedDocs)
        answer = []
        postingAns = []
        if self.notRelatedCounts == 0:
            if len(relatedDocs) != 0:
                return relatedDocs, list(relatedPos)
            else:
                return [], []
        else:
            p1 = relatedDocs
            posting1 = relatedPos
            i = 0
            while i < self.notRelatedCounts:
                p2 = list(self.notRelatedDocs[i].keys())
                i += 1
                while p1 != [] and p2 != []:
                    if p1[0] == p2[0]:
                        p1.remove(p1[0])
                        posting1.remove(posting1[0])
                        p2.remove(p2[0])
                    elif p1[0] < p2[0]:
                        answer.append(p1[0])
                        postingAns.append(posting1[0])
                        posting1.remove(posting1[0])
                        p1.remove(p1[0])
                    else:
                        p2.remove(p2[0])
        for p in p1:
            answer.append(p)
        for posting in posting1:
            postingAns.append(posting)
        print('finall docc')
        return answer, postingAns

    def phraseContainerDocs(self, pharase):
        # to numbers of pharase length
        docs = np.array([dict() for i in range(10)])
        i = 0
        for p in pharase:
            docs[i] = self.indexTasks.getRelatedDocs(p)
            i += 1
        answer = []
        answer_posting = [[] for i in range(50)]
        length = len(docs)
        if length == 0:
            return [],[]
        elif length == 1:
            return list(docs[0].keys()), list(docs[0].values())
        else:
            p2 = list(docs[0].keys())
            posting2 = list(docs[0].values())
            i = 1
            index = -1
            while i < length:
                p1 = list(docs[i].keys())
                posting1 = list(docs[i].values())
                i += 1
                while p1 != [] and p2 != []:
                    if p1[0] == p2[0]:
                        for posting in posting2[0]:
                            if (posting + 1) in posting1[0]:
                                if p1[0] not in answer:
                                    answer.append(p1[0])
                                    index += 1
                                answer_posting[index].append(posting + 1)
                        # print({p1[0] : docs[i - 1][p1[0]]})
                        p1.remove(p1[0])
                        p2.remove(p2[0])
                        posting1.remove(posting1[0])
                        posting2.remove(posting2[0])
                    elif p1[0] < p2[0]:
                        p1.remove(p1[0])
                        posting1.remove(posting1[0])
                    else:
                        p2.remove(p2[0])
                        posting2.remove(posting2[0])
                p2 = answer
                posting2 = answer_posting
        print('double qoute')
        print(answer)
        print(answer_posting)
        return answer, answer_posting