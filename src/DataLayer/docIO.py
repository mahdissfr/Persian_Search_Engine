import pandas as pd
import csv
import ast

class FileInOut():
    def __init__(self):
        self.i = 0
        self.N = self.getDataLen()

    def writeClasses(self, classes, algorithm):
        with open('C:/Users/mahdis/PycharmProjects/phase2/classes'+algorithm+'.csv', 'a', newline='', encoding='utf-8') as f2:
            f2.write(str(classes))
            f2.write('\n')
        f2.close()

    def readClasses(self, algorithm):
        with open('C:/Users/mahdis/PycharmProjects/phase2/classes'+algorithm+'.csv', 'r', newline='', encoding='utf-8') as f2:
            classes = []
            for line in f2:
                classes.append(ast.literal_eval(line))
        return classes[0]

    def writeTrainDocsVector(self, vectors):
        with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/traindocVectors.csv', 'a', newline='', encoding='utf-8') as f2:
            for i in range(0, len(vectors)):
                f2.write(str(vectors[i].docId) + "@" + str(vectors[i].vector))
                f2.write('\n')
        f2.close()

    def readTrainDocsVector(self):
        with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train-docpVectors.csv', 'r', newline='', encoding='utf-8') as f2:
            vectorsList = []
            docIds = []
            for line in f2:
                idnVec = line.split("@")
                docIds.append(int(idnVec[0]))
                vec = ast.literal_eval(idnVec[1])
                vectorsList.append(vec)
        return vectorsList, docIds

    def writepDocsVector(self, vectors):
        # with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train-docpVectors.csv', 'a', newline='', encoding='utf-8') as f2:
        with open('C:/Users/mahdis/PycharmProjects/phase2/docpVectors.csv', 'a', newline='', encoding='utf-8') as f2:
            for i in range(0, len(vectors)):
                f2.write(str(vectors[i].docId) + "@" + str(vectors[i].vector))
                f2.write('\n')
        f2.close()


    # def writeDic(self, result):
    #     with open('C:/Users/mahdis/PycharmProjects/phase2/dictionary.csv', 'a', newline='', encoding='utf-8') as f2:
    #         csvwriter = csv.writer(f2, delimiter=' ')
    #         csvwriter.writerow(result)
    #     f2.close()

    def readData(self, name):
        df = pd.read_csv("C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/"+name, encoding='utf-8')
        return df

    def getDataLen(self):
        sheet = pd.read_csv(r'C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/ir-news-0.csv')
        return len(sheet)

    def writeDocsVector(self, vectors):
        with open('C:/Users/mahdis/PycharmProjects/phase2/docVectors.csv', 'a', newline='', encoding='utf-8') as f2:
            for i in range(0, len(vectors)):
                f2.write(str(vectors[i].docId)+"@"+str(vectors[i].vector))
                f2.write('\n')
        f2.close()

    def readDocsVector(self):
        with open('C:/Users/mahdis/PycharmProjects/phase2/f0-docpVectors.csv', 'r', newline='', encoding='utf-8') as f2:
            vectorsList = []
            docIds = []
            for line in f2:
                idnVec = line.split("@")
                docIds.append(int(idnVec[0]))
                vec = ast.literal_eval(idnVec[1])
                vectorsList.append(vec)
        return vectorsList, docIds

    def writeDic(self, result):
        with open('C:/Users/mahdis/PycharmProjects/phase2/dictionary.csv', 'a', newline='', encoding='utf-8') as f2:
            csvwriter = csv.writer(f2, delimiter=' ')
            csvwriter.writerow(result)
        f2.close()

    def writeDocID(self, result):
        with open('C:/Users/mahdis/PycharmProjects/phase2/DocID.csv', 'a', newline='', encoding='utf-8') as f2:
            csvwriter = csv.writer(f2, delimiter=' ')
            csvwriter.writerow(result)
        f2.close()

    def writePostingList(self, result):
        with open('C:/Users/mahdis/PycharmProjects/phase2/postingList.csv', 'a', newline='', encoding='utf-8') as f2:
            csvwriter = csv.writer(f2, delimiter=' ')
            csvwriter.writerow(result)
        f2.close()

    def readDic(self):
        with open('C:/Users/mahdis/PycharmProjects/phase2/dictionary.csv', 'r', newline='', encoding='utf-8') as f2:
            lis = [line[:len(line)-2] for line in f2]  # create a list of lists
        return lis

    def readDocID(self):
        with open('C:/Users/mahdis/PycharmProjects/phase2/DocID.csv', 'r', newline='', encoding='utf-8') as f2:
            lis = []
            for line in f2:
                sp = line.split(' ')
                sp[-1] = sp[-1][:len(sp[-1])-2]
                lis.append(sp)
        return lis

    def readPostingList(self):
        with open('C:/Users/mahdis/PycharmProjects/phase2/postingList.csv', 'r', newline='', encoding='utf-8') as f2:
            lis = []
            for line in f2:
                sp = line.split('\"')
                sp[-1] = sp[-1][:len(sp[-1]) - 3]
                # print(sp)
                # for i in range(len(sp)):
                #     sp2 = sp[i].split(' ')
                #     print(sp2)
                sp2 = []
                for i in range(len(sp)):
                    if i%2 == 1:
                        sp2.append(sp[i][:len(sp[i])-1])
                lis.append(sp2)
                # sp.remove('\n')
        return lis

    def writeCentroids(self, center, k):
        with open('C:/Users/mahdis/PycharmProjects/phase2/centers'+str(k)+'.csv', 'w', newline='', encoding='utf-8') as f2:
            for i in list(center.keys()):
                f2.write(i+'@'+ str(center[i]))
                f2.write('\n')
        f2.close()

    def writeClusters(self, cluster,k):
        with open('C:/Users/mahdis/PycharmProjects/phase2/clusters'+str(k)+'.csv', 'w', newline='', encoding='utf-8') as f2:
            for i in list(cluster.keys()):
                f2.write(i+'@'+str(cluster[i]))
                f2.write('\n')
        f2.close()

    def readCenters(self):
        with open('C:/Users/mahdis/PycharmProjects/phase2/centers9.csv', 'r', newline='', encoding='utf-8') as f2:
            # centers = dict()
            # reader = csv.reader(f2, delimiter='\n')
            # reader = list(filter(None, reader))
            # for l in reader:
            #     idnVec = l[0].split("@")
            #     centers[idnVec[0]] = ast.literal_eval(idnVec[1])
            vectorsList = []
            centerLabel = []
            for line in f2:
                idnVec = line.split("@")
                centerLabel.append(int(idnVec[0]))
                vec = ast.literal_eval(idnVec[1])
                vectorsList.append(vec)
        return vectorsList, centerLabel

    def readClusters(self):
        with open('C:/Users/mahdis/PycharmProjects/phase2/clusters9.csv', 'r', newline='', encoding='utf-8') as f2:
            centers = dict()
            reader = csv.reader(f2, delimiter='\n')
            reader = list(filter(None, reader))
            for l in reader:
                idnVec = l[0].split("@")
                if idnVec[1]:
                    centers[idnVec[0]] = ast.literal_eval(idnVec[1])
                else:
                    centers[idnVec[0]] = ()
        return centers

def readCategories():
    with open('C:/Users/mahdis/PycharmProjects/phase2/cats/categories.csv', 'r', newline='',
              encoding='utf-8') as f2:
        classes = []
        for line in f2:
            splitted = line.split(",")
            classes.append([splitted[0], splitted[1]])
    return classes

def writeClassesF0():
    classes = {"science": [[]], "cultureart": [[]], "politics": [[]], "economy": [[]], "social": [[]],
               "international": [[]],
               "sport": [[]], "multimedia": [[]]}
    catIndex = ["science", "cultureart", "politics", "economy", "social", "international",
                "sport", "multimedia"]
    tot = readCategories()
    for i in range(1, len(tot)):
        print(i)
        print(tot[i][0])
        print(tot[i][1])
        if int(tot[i][0]) == 7744:
            break
        print("KK")
        cat = catIndex[int(tot[i][1]) - 1]
        classes[cat][0].append(int(tot[i][0]) + 1)
    with open('C:/Users/mahdis/PycharmProjects/phase2/classesKNN.csv', 'a', newline='',
              encoding='utf-8') as f2:
        f2.write(str(classes))
        f2.write('\n')
    f2.close()



# class FileInOut():
#     def __init__(self):
#         self.i = 0
#         # self.N = self.getDataLen()
#         self.N = 158270
#
#     def writeClasses(self, classes, algorithm):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/classes'+algorithm+'.csv', 'a', newline='', encoding='utf-8') as f2:
#             f2.write(str(classes))
#             f2.write('\n')
#         f2.close()
#
#     def readClasses(self, algorithm):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/classes'+algorithm+'.csv', 'r', newline='', encoding='utf-8') as f2:
#             classes = []
#             for line in f2:
#                 classes.append(ast.literal_eval(line))
#             print("classes:")
#             print(classes)
#         return classes[0]
#
#     def writeTrainDocsVector(self, vectors):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/traindocVectors.csv', 'a', newline='', encoding='utf-8') as f2:
#             for i in range(0, len(vectors)):
#                 f2.write(str(vectors[i].docId) + "@" + str(vectors[i].vector))
#                 f2.write('\n')
#         f2.close()
#
#     def readTrainDocsVector(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train-docpVectors.csv', 'r', newline='', encoding='utf-8') as f2:
#             vectorsList = []
#             docIds = []
#             for line in f2:
#                 idnVec = line.split("@")
#                 docIds.append(int(idnVec[0]))
#                 vec = ast.literal_eval(idnVec[1])
#                 vectorsList.append(vec)
#         return vectorsList, docIds
#
#
#     def writeDocsVector(self, vectors, testNum):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/docVectors.csv', 'a', newline='', encoding='utf-8') as f2:
#             for i in range(0, len(vectors)):
#                 f2.write(str(vectors[i].docId) + "@" + str(vectors[i].vector))
#                 f2.write('\n')
#         f2.close()
#
#     def readDocsVector(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/f0-docpVectors.csv', 'r', newline='',
#                   encoding='utf-8') as f2:
#             vectorsList = []
#             docIds = []
#             for line in f2:
#                 idnVec = line.split("@")
#                 docIds.append(int(idnVec[0]))
#                 vec = ast.literal_eval(idnVec[1])
#                 vectorsList.append(vec)
#         return vectorsList, docIds
#
#     # def readData(self):
#     #     # df = pd.read_excel("C:/Users/mahdis/PycharmProjects/phase2/news.xlsx", encoding='utf-8')
#     #     df = pd.read_excel("C:/Users/mahdis/PycharmProjects/phase2/nnews.xlsx", encoding='utf-8')
#     #     return df
#
#     def readData(self, name):
#         df = pd.read_csv("C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/" + name, encoding='utf-8')
#         # df = pd.read_excel("C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/" + name, encoding='utf-8')
#         return df
#
#     def getDataLen(self):
#         # sheet = pd.read_excel(r'C:/Users/mahdis/PycharmProjects/phase2/news.xlsx')
#         sheet = pd.read_excel(r'C:/Users/mahdis/PycharmProjects/phase2/nnews.xlsx')
#         return len(sheet)
#
#     def writepDocsVector(self, vectors):
#         # with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train-docpVectors.csv', 'a', newline='', encoding='utf-8') as f2:
#         with open('C:/Users/mahdis/PycharmProjects/phase2/docpVectors.csv', 'a', newline='', encoding='utf-8') as f2:
#             for i in range(0, len(vectors)):
#                 f2.write(str(vectors[i].docId) + "@" + str(vectors[i].vector))
#                 f2.write('\n')
#         f2.close()
#
#     def readpDocsVector(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/docpVectors.csv', 'r', newline='', encoding='utf-8') as f2:
#             vectorsList = []
#             docIds = []
#             for line in f2:
#                 idnVec = line.split("@")
#                 docIds.append(int(idnVec[0]))
#                 vec = ast.literal_eval(idnVec[1])
#                 vectorsList.append(vec)
#         return vectorsList, docIds
#
#     def writeDic(self, result):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/dictionary.csv', 'a', newline='', encoding='utf-8') as f2:
#             csvwriter = csv.writer(f2, delimiter=' ')
#             csvwriter.writerow(result)
#         f2.close()
#
#     def writeDocID(self, result):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/DocID.csv', 'a', newline='', encoding='utf-8') as f2:
#             csvwriter = csv.writer(f2, delimiter=' ')
#             csvwriter.writerow(result)
#         f2.close()
#
#     def writePostingList(self, result):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/postingList.csv', 'a', newline='', encoding='utf-8') as f2:
#             csvwriter = csv.writer(f2, delimiter=' ')
#             csvwriter.writerow(result)
#         f2.close()
#
#     def readDic(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/dictionary.csv', 'r', newline='', encoding='utf-8') as f2:
#         # with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train-dictionary.csv', 'r', newline='', encoding='utf-8') as f2:
#             lis = [line[:len(line) - 2] for line in f2]  # create a list of lists
#         return lis
#
#     def readDocID(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/DocID.csv', 'r', newline='', encoding='utf-8') as f2:
#         # with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train-DocID.csv', 'r', newline='', encoding='utf-8') as f2:
#             lis = []
#             for line in f2:
#                 sp = line.split(' ')
#                 sp[-1] = sp[-1][:len(sp[-1]) - 2]
#                 lis.append(sp)
#         return lis
#
#     def readPostingList(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/postingList.csv', 'r', newline='', encoding='utf-8') as f2:
#         # with open('C:/Users/mahdis/PycharmProjects/phase2/IR-project-data-phase-3-100k/train/train-postingList.csv', 'r', newline='', encoding='utf-8') as f2:
#             lis = []
#             for line in f2:
#                 sp = line.split('\"')
#                 sp[-1] = sp[-1][:len(sp[-1]) - 3]
#                 # print(sp)
#                 # for i in range(len(sp)):
#                 #     sp2 = sp[i].split(' ')
#                 #     print(sp2)
#                 sp2 = []
#                 for i in range(len(sp)):
#                     if i % 2 == 1:
#                         sp2.append(sp[i][:len(sp[i]) - 1])
#                 lis.append(sp2)
#                 # sp.remove('\n')
#         return lis
#
#
#
#
#
#     def writeCentroids(self, center):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/centers.csv', 'w', newline='', encoding='utf-8') as f2:
#             csvwriter = csv.writer(f2, delimiter=',')
#             for i in list(center.keys()):
#                 f2.write(i + '@')
#                 csvwriter.writerow(center[i])
#                 f2.write('\n')
#         f2.close()
#
#     def writeClusters(self, cluster):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/clusters.csv', 'w', newline='', encoding='utf-8') as f2:
#             for i in list(cluster.keys()):
#                 csvwriter = csv.writer(f2, delimiter=',')
#                 f2.write(i + '@')
#                 csvwriter.writerow(cluster[i])
#                 f2.write('\n')
#         f2.close()
#
#     def readCenters(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/centers.csv', 'r', newline='', encoding='utf-8') as f2:
#             centers = dict()
#             reader = csv.reader(f2, delimiter='\n')
#             reader = list(filter(None, reader))
#             for l in reader:
#                 idnVec = l[0].split("@")
#                 centers[idnVec[0]] = ast.literal_eval(idnVec[1])
#         return centers
#
#     def readClusters(self):
#         with open('C:/Users/mahdis/PycharmProjects/phase2/clusters.csv', 'r', newline='', encoding='utf-8') as f2:
#             centers = dict()
#             reader = csv.reader(f2, delimiter='\n')
#             reader = list(filter(None, reader))
#             for l in reader:
#                 idnVec = l[0].split("@")
#                 if idnVec[1]:
#                     centers[idnVec[0]] = ast.literal_eval(idnVec[1])
#                 else:
#                     centers[idnVec[0]] = ()
#         return centers
