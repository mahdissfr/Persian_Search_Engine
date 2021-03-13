import math

# from BusinessLayer.Heap import MaxHeap
from BusinessLayer.Heap import MaxHeap, DocNode
from BusinessLayer.query import QueryProc
from BusinessLayer.textOperations import FormWords
from DataLayer.constants import ConstantVars
from DataLayer.docIO import FileInOut


def weighting_scheme1_doc(tf, nt, N):
    return tf * math.log10(N / nt)


def weighting_scheme2_doc(tf):
    return 1 + math.log10(tf)


def weighting_scheme3_doc(tf, nt, N):
    return (1 + math.log10(tf)) * math.log10(N / nt)


def find_tfmax(termsList):
    tfmax = 0
    for x in termsList:
        tf = termsList.count(x)
        if tf > tfmax:
            tfmax = tf
    return tfmax


def weighting_scheme1_query(tf, nt, N, tfmax):
    return (0.5 + 0.5 * (tf / tfmax)) * math.log10(N / nt)


def weighting_scheme2_query(nt, N):
    return math.log10(1 + N / nt)


def weighting_scheme3_query(tf, nt, N):
    return (1 + math.log10(tf)) * math.log10(N / nt)


class DocumentVector:
    def __init__(self, doc_id):
        self.docId = doc_id
        self.vector = {}

    def fill_vector(self, term, tf, nt, N, doc_ids):
        df = len(doc_ids)
        idf = math.log10(N / df)
        if idf > 0.2:
            self.vector[term] = weighting_scheme3_doc(tf, nt, N)
            # self.vector[term] = weighting_scheme2_doc(tf)
            # self.vector[term] = weighting_scheme3_doc(tf, nt, N)


class Similiarity:

    def __init__(self):
        self.input = FileInOut()
        self.N = self.input.N
        # self.docVectorList, self.vectorsIds = self.input.readpDocsVector()

    def get_size(self, vector):
        tfs = vector.values()
        sum = 0
        for tf in tfs:
            sum += pow(tf, 2)
        return math.sqrt(sum)

    def compute_similarity(self, query_vector, doc_vector):
        sum = 0
        for term_id in query_vector.keys():
            sum += query_vector.get(term_id) * doc_vector.get(term_id, 0)
        similarity = sum / (self.get_size(query_vector) * self.get_size(doc_vector))
        return similarity

    def get_index(self, doc_vectors, value):
        for x in doc_vectors:
            if x.docId == value:
                return doc_vectors.index(x)
        return -1
        # doc = next((x for x in doc_vectors if x.docid == value), None)
        # return doc_vectors.index(doc) if doc != None else -1

    @staticmethod
    def get_query_termList(query):
        wordFormer = FormWords()
        constants = ConstantVars()
        query = wordFormer.normalize(query)
        query_tokens = wordFormer.tokenize(query)
        for token in query_tokens:
            if token in constants.punctuations() or token in constants.StopWords():
                query_tokens.remove(token)
        query_tokens = wordFormer.uniform(query_tokens)
        # postaged_tokens = wordFormer.posTagging(query_tokens)
        stemmed_tokens = wordFormer.stemmWords(query_tokens)
        lemmatized_tokens = wordFormer.lemmatizeWords(stemmed_tokens)

        lemmatized_tokens = list(filter(lambda a: a != '"', lemmatized_tokens))
        return lemmatized_tokens


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
                vector[term_id] = (1 + math.log10(tf)) * math.log10(self.N / len(docIDs[term_id]))
                # vector[term_id] = weighting_scheme2_query(len(docIDs[term_id]), self.N)
                # vector[term_id] = weighting_scheme3_query(tf, len(docIDs[term_id]), self.N)
        for y in negative:
            term_id = dictionary.index(y) if y in dictionary else -1
            if term_id != -1 and vector.get(term_id) is None:
                tf = negative.count(y)
                value = (1 + math.log10(tf)) * math.log10(self.N / len(docIDs[term_id]))
                # value = weighting_scheme2_query(len(docIDs[term_id]), self.N)
                # value = weighting_scheme3_query(tf, len(docIDs[term_id]), self.N)
                vector[term_id] = -1 * value
        return vector

    def compute_docs_wieghts(self):
        docIDs = self.input.readDocID()
        postings = self.input.readPostingList()
        doc_vectors = []
        for i in range(115148):
            print(i)
            for j in range(len(docIDs[i])-1):
                index = self.get_index(doc_vectors, docIDs[i][j])
                if index == -1:
                    doc_vectors.append(DocumentVector(docIDs[i][j]))
                    index = self.get_index(doc_vectors, docIDs[i][j])
                doc_vectors[index].fill_vector(i + 1, len(postings[i][j]), len(docIDs[i]), self.N, docIDs[i])
        doc_vectors.sort(key=lambda x: int(x.docId))
        self.input.writepDocsVector(doc_vectors)
        return doc_vectors

    def process_query(self, query, k):
        q1 = QueryProc()
        notEliminated = query.replace("!", "")
        docList, indexList = q1.processQueryBySimilarity(notEliminated)
        max_heap = self.make_heap(docList, indexList, query)
        return self.getKbest(max_heap, k)

    def make_heap(self, docList, indexList, query):
        maxHeap = MaxHeap()
        queryVector = self.compute_query_wieght(self.get_query_termList(query))
        for i in range(len(docList)):
            if docList[i]==7744:
                continue
            k = self.vectorsIds.index(docList[i])
            similarity = self.compute_similarity(queryVector, self.docVectorList[k])
            if not self.is_similsrity_zero(similarity):
                maxHeap.insert(DocNode(docList[i], indexList[i], similarity))

        return maxHeap

    @staticmethod
    def is_similsrity_zero(similarity):
        return similarity == 0.0

    def getKbest(self, maxHeap, k):
        simsum = 0
        docList = []
        indexList = []
        for i in range(k):
            docNode = maxHeap.extractMax()
            if docNode is None:
                break
            simsum += docNode.similarity
            docList.append(docNode.docId)
            indexList.append(docNode.indexList)
        return docList, indexList


# s = Similiarity()
# s.compute_docs_wieghts()
