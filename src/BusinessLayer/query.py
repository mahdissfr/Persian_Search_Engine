from .textOperations import FormWords
from DataLayer.constants import ConstantVars
from DataLayer.docIO import FileInOut
import numpy as np


class QueryProc:
    def __init__(self):
        self.input = FileInOut()
        self.Dic = self.input.readDic()
        self.DocID_file = self.input.readDocID()
        self.posting_file = self.input.readPostingList()
        self.wordFormer = FormWords()
        self.constants = ConstantVars()
        self.relatedDocs = []
        self.notRelatedDocs = []
        self.relatedDocsPos = []
        self.notRelatedDocsPos = []
        self.notRelatedCounts = 0

    def initializing(self, query):
        print(query)
        query = self.wordFormer.normalize(query)
        print(query)
        query_tokens = self.wordFormer.tokenize(query)
        for token in query_tokens:
            if token in self.constants.punctuations() or token in self.constants.StopWords():
                query_tokens.remove(token)
        query_tokens = self.wordFormer.uniform(query_tokens)
        # postaged_tokens = self.wordFormer.posTagging(query_tokens)
        stemmed_tokens = self.wordFormer.stemmWords(query_tokens)
        lemmatized_tokens = self.wordFormer.lemmatizeWords(stemmed_tokens)
        i = j = 0
        k = 0
        not_include = False
        order = False
        orderTokens = [[] for i in range(5)]
        for token in lemmatized_tokens:
            print(token)
            if token == "«" and order == False:
                print('first')
                k += 1
                order = True
                continue
            if token == "»" and order == True:
                print('second')
                order = False
                continue
            if order:
                orderTokens[k - 1].append(token)
                continue
            if token == "!":
                not_include = True
                self.notRelatedCounts += 1
                continue
            if not_include:
                self.notRelatedDocs.append(self.getRelatedSavedDocs(token))
                self.notRelatedDocsPos.append(self.getRelatedSavedpos(token))
                not_include = False
            print('order')
            print(order)
            if not not_include and not order:
                print('hahahaha')
                self.relatedDocs.append(self.getRelatedSavedDocs(token))
                self.relatedDocsPos.append(self.getRelatedSavedpos(token))

            # related_result, relatedPos = self.merge(self.relatedDocs, i)
        related_result = []
        relatedPos = []
        for res in range(len(self.relatedDocs)):
            related_result = related_result + self.relatedDocs[res]
            relatedPos = relatedPos + self.relatedDocsPos[res]
        related_result = list(set(related_result))
        relatedPos = relatedPos[:len(related_result)]
        docs = []
        doc_pos = []
        j = 0
        if related_result != []:
            docs.append(related_result)
            doc_pos.append(relatedPos)
            j += 1
        for i in range(0, k):
            phrase_container, phrase_pos = self.phraseContainerDocs(orderTokens[i])
            docs.append(phrase_container)
            doc_pos.append(phrase_pos)
            j += 1
        final_result, final_pos = self.finalMerge(docs, doc_pos, j)

        relateds_and_not_unrelateds, related_position = self.notMerge(final_result, final_pos)
                # i += 1
        return relateds_and_not_unrelateds,related_position

    def merge_common_docs(self, common_list, docList1, docList2, indexList1, indexList2):
        for doc in common_list:
            i1 = docList1.index(doc)
            i2 = docList2.index(doc)
            docList2.pop(i2)
            indexList1[i1] = indexList1[i1] + indexList2.pop(i2)
        indexList1 = indexList1 + indexList2
        docList1 = docList1 + docList2
        return indexList1, docList1

    def similarity_merge(self, docLists, indexLists):
        if len(docLists) == 0:
            return None, None
        docs = docLists.pop(0)
        indexes = list(filter(lambda n: n != [], indexLists.pop(0)))
        if len(docLists) == 0:
            return docs, indexes
        for doc in docLists:
            i = docLists.index(doc)
            doci = docLists.pop(i)
            dociPos = list(filter(lambda n: n != [], indexLists.pop(i)))
            common = list(set(doci) & set(docs))
            indexes, docs = self.merge_common_docs(common, docs, doci, indexes, dociPos)
        return docs, indexes

    def processQueryBySimilarity(self, query):
        print('queryyy')
        print(query)
        docList, indexList = self.initializing(query)
        # related_result, related_pos = self.relatedDocs, self.relatedDocsPos
        # j = 0
        # if related_result != []:
        #     j += 1
        # for i in range(0, k):
        #     phrase_container, phrase_pos = self.phraseContainerDocs(orderTokens[i])
        #     related_result.append(phrase_container)
        #     related_pos.append(phrase_pos)
        #     j += 1
        # relateds_and_not_unrelateds, related_position = self.finalMerge(related_result, related_pos, j)
        # # relateds_and_not_unrelateds, related_position = self.similarity_merge(related_result, related_pos)
        # docList, indexList = self.notMerge(relateds_and_not_unrelateds, related_position)
        return docList, indexList

    def processQuery(self, query):
        query = self.wordFormer.normalize(query)
        query_tokens = self.wordFormer.tokenize(query)
        for token in query_tokens:
            if token in self.constants.punctuations() or token in self.constants.StopWords():
                query_tokens.remove(token)
        query_tokens = self.wordFormer.uniform(query_tokens)
        # postaged_tokens = self.wordFormer.posTagging(query_tokens)
        stemmed_tokens = self.wordFormer.stemmWords(query_tokens)
        lemmatized_tokens = self.wordFormer.lemmatizeWords(stemmed_tokens)
        i = j = 0
        k = 0
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
                orderTokens[k - 1].append(token)
                continue
            if token == "!":
                not_include = True
                self.notRelatedCounts += 1
                continue
            if not_include:
                self.notRelatedDocs.append(self.getRelatedSavedDocs(token))
                self.notRelatedDocsPos.append(self.getRelatedSavedpos(token))
                not_include = False
            else:
                self.relatedDocs.append(self.getRelatedSavedDocs(token))
                self.relatedDocsPos.append(self.getRelatedSavedpos(token))
                i += 1
        # print('related docs')
        # print(self.relatedDocs)
        related_result, relatedPos = self.merge(self.relatedDocs, i)
        docs = []
        doc_pos = []
        j = 0
        if related_result != []:
            docs.append(related_result)
            doc_pos.append(relatedPos)
            j += 1
        for i in range(0, k):
            phrase_container, phrase_pos = self.phraseContainerDocs(orderTokens[i])
            docs.append(phrase_container)
            doc_pos.append(phrase_pos)
            j += 1
        final_result, final_pos = self.finalMerge(docs, doc_pos, j)
        # print("self.notRelatedCounts")
        # print(self.notRelatedCounts)
        # print('no relate')
        # print(self.notRelatedDocs)
        relateds_and_not_unrelateds, related_position = self.notMerge(final_result, final_pos)
        # for i in range(len(related_pos)):
        #     related_pos[i] = related_pos[i]
        # print(relateds_and_not_unrelateds)
        # print(related_position)
        return relateds_and_not_unrelateds, related_position

    def merge(self, docs, leng):
        answer = []
        postingAns = []
        if leng == 0:
            return [], []
        elif leng == 1:
            return docs[0], self.relatedDocsPos[0]
        else:
            p2 = docs[0]
            postings2 = []
            for j in range(len(p2)):
                postings2.append(self.relatedDocsPos[0][j])
            i = 1
            while i < leng:
                p1 = docs[i]
                postings1 = []
                for j in range(len(p1)):
                    postings1.append(self.relatedDocsPos[i][j])
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
            return [], []
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
        # print('docc and double quote')
        # print(answer)
        # print(docPosAns)
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
                p2 = self.notRelatedDocs[i]
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
        docs = []
        docsPos = []
        for p in pharase:
            docs.append(self.getRelatedSavedDocs(p))
            docsPos.append(self.getRelatedSavedpos(p))
        answer = []
        answer_posting = [[] for k in range(50)]
        length = len(docs)
        if length == 0:
            return [], []
        elif length == 1:
            # print(docs[0])
            return docs[0], docsPos[0]
        else:
            p2 = docs[0]
            posting2 = docsPos[0]
            i = 1
            while i < len(pharase):
                index = -1
                answer = []
                answer_posting = [[] for k in range(50)]
                p1 = docs[i]
                posting1 = docsPos[i]
                i += 1
                while (p1 != [] and p2 != []):
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
                # print('ans')
                # print(answer)
                # print(answer_posting)
                posting2 = answer_posting
        # print('double qoute')
        # print(answer)
        # print(answer_posting)
        return answer, answer_posting

    def getRelatedSavedDocs(self, token):
        i = 0
        if token in self.Dic:
            # print(self.Dic.index(token))
            posting = list(map(int, self.DocID_file[self.Dic.index(token)]))
            i += 1
            print(posting)
            return posting
        return []

    def getRelatedSavedpos(self, token):
        i = 0
        if token in self.Dic:
            # print(self.Dic.index(token))
            posting = [list(map(int, self.posting_file[self.Dic.index(token)][j].split(' '))) for j in
                       range(len(self.posting_file[self.Dic.index(token)]))]
            i += 1
            return posting
        return []
