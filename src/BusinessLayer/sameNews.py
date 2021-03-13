from BusinessLayer.queryProcessByClustering import QueryProcByCluster
from DataLayer.docIO import FileInOut
from BusinessLayer.group import Group
from BusinessLayer.similarity import Similiarity
import numpy as np
from .sort import Time


class SimilarNews():
    def __init__(self):
        self.inOut = FileInOut()
        self.clusters = self.inOut.readClusters()
        self.g = Group()
        self.similarity = Similiarity()
        self.v, self.d = self.inOut.readDocsVector()

    def minusDocs(self, doc1, doc2):
        if not doc1:
            return []
        return list(set(doc1) - set(doc2))

    def findSimilarNews(self,query, no_news):
        queryProcess = QueryProcByCluster()
        docs , positions, nearestCentroids = queryProcess.processQueryByCluster(query, no_news)
        if docs:
            docIds, positionsIds = self.g.out_group_of_file(docs, positions)
            c = 0
            relatedDocs = []
            for doc in docIds:
                t2 = Time(doc)
                c += 1
                if doc in self.clusters[nearestCentroids[0]]:
                    similarities = []
                    for d in self.minusDocs(self.clusters[nearestCentroids[0]], docs[0]):
                        t1 = Time(d+1)
                        if t1.year == t2.year and t1.month == t2.month and abs(t1.day - t2.day) < 3 and d not in relatedDocs:
                            index = self.d.index(d)
                            index_doc = self.d.index(doc)
                            similarities.append(self.similarity.compute_similarity(self.v[index], self.v[index_doc]))
                    if similarities:
                        maximum = np.max(similarities)
                        docindex = similarities.index(maximum)
                        relatedDocs.append(docindex)
                    if len(relatedDocs) == 5:
                        break
                else:
                    similarities = []
                    for d in self.minusDocs(self.clusters[nearestCentroids[1]], docs[0]):
                        t1 = Time(d+1)
                        if t1.year == t2.year and t1.month == t2.month and abs(t1.day - t2.day) < 3 and d not in relatedDocs:
                            index = self.d.index(d)
                            index_doc = self.d.index(doc)
                            # docVec = self.v[index]
                            similarities.append(self.similarity.compute_similarity(self.v[index], self.v[index_doc]))
                    if similarities:
                        maximum = np.max(similarities)
                        docindex = similarities.index(maximum)
                        relatedDocs.append(docindex)
                    if len(relatedDocs) == 5:
                        break
            return docs, positions, relatedDocs
        else:return {0:[]} , {0:[]}, []

