class Group:

    def __init__(self):
        self.borders = [7744]

    def out_group_of_file(self, doc_dic, index_dic):
        docInd = []
        positions = []
        for key in doc_dic.keys():
            for docId in doc_dic[key]:
                docInd.append(self.unpacking_index(docId, key))
            positions = positions + index_dic[key]
        return docInd, positions

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
        if file_num == 0:
            return doc_id
        did = doc_id + self.borders[file_num - 1]
        return did

    def pack_id(self, tot_id):
        fnum = next(x[0] for x in enumerate(self.borders) if x[1] > tot_id)
        if fnum == 0:
            return fnum, tot_id
        id = tot_id - self.borders[fnum - 1]
        return fnum, id