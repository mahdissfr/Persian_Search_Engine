import re
import math
from BusinessLayer.query import QueryProc
from BusinessLayer.Heap import MaxHeap, DocNode
from BusinessLayer.group import Group
from BusinessLayer.similarity import Similiarity
from DataLayer.docIO import FileInOut
import numpy as np
from .textOperations import FormWords


class QueryProcByCluster:
    def __init__(self):
        self.g = Group()
        self.input = FileInOut()
        self.classes = self.input.readClasses("KNN")
        # self.classes = self.input.readClasses("NB")
        self.docVectorList, self.vectorsIds = self.input.readDocsVector()
        self.wordFormer = FormWords()

    def find(self, s, pat):
        pat = r'(\w*%s\w*)' % pat  # Not thrilled about this line
        return re.findall(pat, s)

    def process_cat(self, query, num_ov_results):
        cat_inq = self.find(query, "cat")
        category = cat_inq[0].split(":")[1]
        query = query.replace(cat_inq[0], '')
        q1 = QueryProc()
        notEliminated = query.replace("!", "")
        docList, indexList = q1.processQueryBySimilarity(notEliminated)
        doc_dic, index_dic = self.g.grouping_by_file(docList, indexList)
        for key in doc_dic.keys():
            for docId in doc_dic[key]:
                if not docId in self.classes[category][key]:
                    to_remove = doc_dic[key].index(docId)
                    doc_dic[key].pop(to_remove)
                    index_dic[key].pop(to_remove)
        max_heap = self.make_heap(doc_dic, index_dic, query)
        return self.getKbest(max_heap, num_ov_results)

    def make_heap(self, doc_dic, index_dic, query):
        maxHeap = MaxHeap()
        simi = Similiarity()
        queryVector = self.compute_query_wieght(simi.get_query_termList(query))
        for key in doc_dic.keys():
            for i in range(len(doc_dic[key])):
                tot_did = self.g.unpacking_index(doc_dic[key][i], key)
                # if tot_did > 7743:
                #     continue
                k = self.vectorsIds.index(tot_did)
                similarity = self.compute_similarity(queryVector, self.docVectorList[k])
                if not simi.is_similsrity_zero(similarity):
                    maxHeap.insert(DocNode(tot_did, index_dic[key][i], similarity))
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
        doc_ids, indexes = self.g.grouping_by_file(docList, indexList)
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

    def nearestCentroids(self, query):
        centers, labels = self.input.readCenters()
        distances = []
        for center in centers:
            distances.append(self.compute_similarity(query, center))
        maximum = np.max(distances)
        nearestNeabeor = distances.index(maximum)
        distances2 = distances
        distances.remove(maximum)
        maximum2 = np.max(distances)
        if maximum == maximum2:
            nearestNeabeor2 = distances.index(maximum2, nearestNeabeor+1)
        else:
            nearestNeabeor2 = distances.index(maximum2)
        # distances2.remove(minimum2)
        return [str(nearestNeabeor) , str(nearestNeabeor2)]

    def mergeDocs(self, doc1, doc2, index1):
        if not doc1:
            return [], []
        # print('type')
        # print(doc1)
        # print(type(doc1))
        withOutQoute = list(set(doc2) - set(doc1))
        doc2 = list(set(doc2))
        for d in withOutQoute:
            doc2.remove(d)
        positions = []
        for d in doc2:
            positions.append(index1[doc1.index(d)])
        return doc2, positions

    def processQueryByCluster(self, query, num_ov_results):
        cat = False
        if "cat" in query:
            cat_inq = self.find(query, "cat:")
            category = cat_inq[0].split(":")[1]
            query = query.replace(cat_inq[0], '')
            cat = True
        q1 = QueryProc()
        docList, indexList = q1.processQueryBySimilarity(query)
        term_list = Similiarity.get_query_termList(query)
        queryVec = self.compute_query_wieght(term_list)
        if queryVec == {}:
            return {0:[]} , {0:[]}, []
        nearestCentroids = self.nearestCentroids(queryVec)
        print('center')
        print(nearestCentroids)
        docs = []
        for neabors in nearestCentroids:
            a = list(self.input.readClusters()[neabors])
            docs = docs + a
        print('doclist')
        print(docList)
        mergeDocs, positions  = self.mergeDocs(docList, docs, indexList)
        if not mergeDocs:
            return {0:[]} , {0:[]}, nearestCentroids
        doc_dic, index_dic = self.g.grouping_by_file(mergeDocs, positions)
        print("boolean cat fffffffffffff")
        print(cat)
        if cat:
            # result_doc_dic = {}
            # result_indexes = {}
            # print("cat tttttttttttt")
            # print(category)
            # print("Class kkkkkkkkkkkkk")
            # print(self.classes)
            # if category.lower() in self.classes.keys():
                for key in doc_dic.keys():
                    # result_doc_dic[key] = []
                    # result_indexes[key] = []
                    print("qabl hazffffff: "+str(len(doc_dic[key])))
                    print(doc_dic[key])
                    print("category.lower()")
                    print(category.lower())
                    # print(self.classes[category.lower()][key])
                    to_remove = []
                    for t in range(len(doc_dic[key])):###doc_dic[key][t]=docid
                        # print("docidll : "+str(doc_dic[key][t]))
                        if doc_dic[key][t] not in self.classes[category.lower()][key]:
                            # print(str(doc_dic[key][t])+" not in fffffffffffffffff ")
                            # in_cat = doc_dic[key].index(docId)
                            # result_doc_dic[key].append(doc_dic[key].pop(in_cat))
                            # result_indexes[key].append(index_dic[key].pop(in_cat))
                            # doc_dic[key].pop(in_cat)
                            to_remove.append(t)
                            # print(doc_dic[key].pop(t))
                            # index_dic[key].pop(t)
                    to_remove.sort(reverse=True)
                    for f in range(len(to_remove)):
                        index_dic[key].pop(to_remove[f])
                        doc_dic[key].pop(to_remove[f])
                    print("bad hazffffff: " + str(len(doc_dic[key])))
                    print(doc_dic)
        max_heap = self.make_heap(doc_dic, index_dic, query)
        kbest1, kbest2 = self.getKbest(max_heap, num_ov_results)
        return kbest1, kbest2, nearestCentroids

