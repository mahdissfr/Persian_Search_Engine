import math
import pandas as pd
import operator
from BusinessLayer.Heap import MaxHeap, DocNode
from BusinessLayer.query import QueryProc
from BusinessLayer.similarity import Similiarity
from DataLayer.docIO import FileInOut, writeClassesF0
from collections import Counter
import re


def find(s, pat):
    pat = r'(\w*%s\w*)' % pat  # Not thrilled about this line
    return re.findall(pat, s)


class Group:
    def __init__(self, borders):
        self.borders = borders

    def grouping_by_file(self, docList, indexList):
        doc_ids = {}
        indexes_dic = {}
        for i in range(len(docList)):
            fnum, id = self.pack_id(docList[i])
            if doc_ids.get(fnum) is None:
                doc_ids[fnum] = []
                indexes_dic[fnum] = []
            doc_ids[fnum].append(id)
            indexes_dic[fnum].append(indexList[i])
        return doc_ids, indexes_dic

    def unpacking_index(self, doc_id, file_num):
        did = doc_id + self.borders[file_num - 1]
        return did

    def pack_id(self, tot_id):
        fnum = next(x[0] for x in enumerate(self.borders) if x[1] > tot_id)
        if fnum == 0:
            return fnum, tot_id
        id = tot_id - self.borders[fnum - 1]
        return fnum, id


class Train_data:
    def __init__(self):
        self.sheet = pd.read_excel(
            r'C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train.xlsx')

    def get_cat(self, docID):
        tmp = self.sheet.loc[docID - 1][7]
        if tmp == 'culutre-art' or tmp == 'culture-art':
            tmp = 'cultureart'
        print("tmp")
        print(type(tmp))
        print(tmp)
        if isinstance(tmp, str):
            return tmp.lower()
        print("khaaaaaaaaaaaaaaallllllllllliiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        return self.get_cat(docID - 1)


class Classifier:
    def __init__(self, algorithm):
        self.train_data = Train_data()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        self.input = FileInOut()
        self.k = 5
        # self.train_data = self.input.N
        self.docVectorList, self.vectorsIds = self.input.readDocsVector()
        print("222222222222222222222")
        self.trainVectorList, self.trainvectorsIds = self.input.readTrainDocsVector()
        print("33333333333333333333333333333")
        self.num_ov_results = 100
        self.gp = Group([7745])
        print("ta ghable knn umaaaaaaad")
        self.classes = self.KNN()
        # self.classes = self.NB()
        # self.classes = self.input.readClasses(algorithm)


    def KNN(self):
        classes = {"science": [], "cultureart": [], "politics": [], "economy": [], "social": [], "international": [],
                   "sport": [], "multimedia": []}

        for key in classes.keys():
            classes[key].append([])
        print("for size : " + str(len(self.docVectorList)))
        for j in range(len(self.docVectorList)):
            # for j in range(2):
            print("j: " + str(j))
            kbest = []
            for t in range(len(self.trainVectorList)):
                similarity = self.compute_similarity(self.docVectorList[j], self.trainVectorList[t])
                if len(kbest) < self.k:
                    kbest.append([similarity, self.train_data.get_cat(self.trainvectorsIds[t])])
                else:
                    minimum = min(kbest, key=lambda x: x[0])
                    if similarity > minimum[0]:
                        kbest[kbest.index(minimum)] = [similarity, self.train_data.get_cat(self.trainvectorsIds[t])]
            cat = [Counter(col).most_common(1)[0][0] for col in zip(*kbest)][1]
            fnum, id = self.gp.pack_id(self.vectorsIds[j])
            classes[cat][fnum].append(id)
        # self.input.writeClasses(classes, "KNN")
        writeClassesF0()
        return classes

    def NB(self):
        classes = {"science": [], "cultureart": [], "politics": [], "economy": [], "social": [], "international": [],
                   "sport": [], "multimedia": []}
        print("for size : " + str(len(self.docVectorList)))
        class_tf, nci, tf_tid = self.get_classes_tf()
        for key in classes.keys():
            classes[key].append([])
        for j in range(len(self.docVectorList)):
            # print("j: " + str(j))
            cat = self.determine_category(self.docVectorList[j], class_tf, nci, tf_tid)
            fnum, id = self.gp.pack_id(self.vectorsIds[j])
            classes[cat][fnum].append(id)
        self.input.writeClasses(classes, "NB")
        return classes

    def get_classes_tf(self):
        class_tf = {"science": 0, "cultureart": 0, "politics": 0, "economy": 0, "social": 0, "international": 0,
                    "sport": 0, "multimedia": 0}
        nci = {"science": 0, "cultureart": 0, "politics": 0, "economy": 0, "social": 0, "international": 0,
               "sport": 0, "multimedia": 0}
        tf_tid = {"science": {}, "cultureart": {}, "politics": {}, "economy": {}, "social": {}, "international": {},
                    "sport": {}, "multimedia": {}}
        for t in range(len(self.trainVectorList)):
            td_cat = self.train_data.get_cat(self.trainvectorsIds[t])
            for tid in self.trainVectorList[t].keys():
                if tf_tid[td_cat].get(tid, None) is None:
                    tf_tid[td_cat][tid] = self.trainVectorList[t][tid]
                else:
                    tf_tid[td_cat][tid] += self.trainVectorList[t][tid]
            nci[td_cat] += 1
            # alpha = 1
            class_tf[td_cat] += sum(self.trainVectorList[t].values()) + 1 * len(self.trainVectorList[t])
        print("LLLLLLLLLLLLLLLLLLFFFFFFFFFFFFFFFFFFFFFFFFFFLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLFFFFFFFFFFFFFFFFFFFFFFFF")
        print(tf_tid)
        return class_tf, nci, tf_tid

    def determine_category(self, docVector, class_tf, nci, tf_tid):
        c_score = {"science": 0, "cultureart": 0, "politics": 0, "economy": 0, "social": 0, "international": 0,
                   "sport": 0, "multimedia": 0}
        for cat in c_score.keys():
            c_score[cat] += math.log10(nci[cat] / 1000)
            for tid in docVector.keys():
                if tf_tid[cat].get(tid, None) is None:
                    c_score[cat] += math.log10((1) / class_tf[cat])
                else:
                    c_score[cat] += math.log10((tf_tid[cat][tid] + 1) / class_tf[cat])
        print("score for each class:")
        print(c_score)
        determined_cat = max(c_score.items(), key=operator.itemgetter(1))[0]
        return determined_cat

    def process_cat(self, query):
        cat_inq = find(query, "cat")
        category = cat_inq[0].split(":")[1]
        query = query.replace(cat_inq[0], '')
        q1 = QueryProc()
        notEliminated = query.replace("!", "")
        docList, indexList = q1.processQueryBySimilarity(notEliminated)
        doc_dic, index_dic = self.gp.grouping_by_file(docList, indexList)
        for key in doc_dic.keys():
            for docId in doc_dic[key]:
                if not docId in self.classes[category][key]:
                    to_remove = doc_dic[key].index(docId)
                    doc_dic[key].pop(to_remove)
                    index_dic[key].pop(to_remove)
        max_heap = self.make_heap(doc_dic, index_dic, query)
        return self.getKbest(max_heap, self.num_ov_results)

    def make_heap(self, doc_dic, index_dic, query):
        maxHeap = MaxHeap()
        queryVector = self.compute_query_wieght(Similiarity.get_query_termList(query))
        for key in doc_dic.keys():
            for i in range(len(doc_dic[key])):
                # if docList[i]==7744:
                #     continue
                tot_did = self.gp.unpacking_index(doc_dic[key][i], key)
                k = self.vectorsIds.index(tot_did)
                similarity = self.compute_similarity(queryVector, self.docVectorList[k])
                if not Similiarity.is_similsrity_zero(similarity):
                    maxHeap.insert(DocNode(tot_did, index_dic[k][i], similarity))
        return maxHeap

    def getKbest(self, maxHeap, k):
        docList = []
        indexList = []
        for i in range(k):
            docNode = maxHeap.extractMax()
            if docNode is None:
                break
            docList.append(docNode.docId)
            indexList.append(docNode.indexList)
        doc_ids, indexes = self.gp.grouping_by_file(docList, indexList)
        return doc_ids, indexes

    def compute_similarity(self, query_vector, doc_vector):
        sum = 0
        for term_id in query_vector.keys():
            sum += query_vector.get(term_id) * doc_vector.get(term_id, 0)
        similarity = sum / (self.get_size(query_vector) * self.get_size(doc_vector))
        return similarity

    def get_size(self, vector):
        tfs = vector.values()
        sum = 0
        for tf in tfs:
            sum += pow(tf, 2)
        return math.sqrt(sum)

    def compute_query_wieght(self, termsList):
        dictionary = self.input.readDic()
        docIDs = self.input.readDocID()
        vector = {}
        negative = []
        indices = [i for i, x in enumerate(termsList) if x == '!']
        indices.sort(reverse=True)
        for i in indices:
            negative.append(termsList.pop(i + 1))
            termsList.pop(i)
        for x in termsList:
            term_id = dictionary.index(x) + 1 if x in dictionary else -1
            if term_id != -1 and vector.get(term_id) is None:
                tf = termsList.count(x)
                vector[term_id] = (1 + math.log10(tf)) * math.log10(self.input.N / len(docIDs[term_id]))
                # vector[term_id] = weighting_scheme2_query(len(docIDs[term_id]), self.N)
                # vector[term_id] = weighting_scheme3_query(tf, len(docIDs[term_id]), self.N)
        for y in negative:
            term_id = dictionary.index(y) if y in dictionary else -1
            if term_id != -1 and vector.get(term_id) is None:
                tf = negative.count(y)
                value = (1 + math.log10(tf)) * math.log10(self.input.N / len(docIDs[term_id]))
                # value = weighting_scheme2_query(len(docIDs[term_id]), self.N)
                # value = weighting_scheme3_query(tf, len(docIDs[term_id]), self.N)
                vector[term_id] = -1 * value
        return vector


classofier = Classifier("KNN")
# print(find('cat:social ????????????????', "cat"))
