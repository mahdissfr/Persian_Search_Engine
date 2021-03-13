import math

from DataLayer.docIO import FileInOut


class HeapsLaw:

    def set_tokens(self):
        input = FileInOut()
        dictionary = input.readDic()
        M = len(dictionary)
        print("M :" + str(M))
        T = 755440
        return T, M

    def check(self, T, M):
        print("based on : M = kT^b")
        print("b = 0.5 so : k = M/(T^0.5)")
        print("30 < k < 100")
        k = M / pow(T, 0.5)
        print("k = " + str(k))


class ZipfsLaw:
    def __init__(self):
        self.cfDic = []

    def set_cf_dictionary(self):
        input = FileInOut()
        postings = input.readPostingList()
        cfis = {}
        for i in range(len(postings) - 1):
            cfis[i] = 0
            for j in range(len(postings[i]) - 1):
                cfis[i] += len(postings[i][j])
        self.cfDic = sorted(cfis.items(), key=lambda cfis: cfis[1], reverse=True)
        cfis.clear()

    def check(self):
        print("based on : logcfi = logc + klogi")
        print("k=-1 so : logc = logcfi + logi")
        for i in range(len(self.cfDic) - 1):
            logi = math.log10(i + 1)
            if self.cfDic[i][1] != 0:
                logcfi = math.log10(self.cfDic[i][1])
            else:
                logcfi = 0
            logc = logcfi + logi
            print("i :" + str(i + 1) + " term id :" + str(self.cfDic[i][0]) + " cf :" + str(
                self.cfDic[i][1]) + " logc :" + str(logc))


#
zipf = ZipfsLaw()
zipf.set_cf_dictionary()
zipf.check()

# heap = HeapsLaw()
# T, M = heap.set_tokens()
# heap.check(T, M)
