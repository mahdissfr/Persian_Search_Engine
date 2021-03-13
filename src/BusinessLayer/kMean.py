import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DataLayer.docIO import FileInOut


class Kmean:
    def __init__(self):
        self.inOut = FileInOut()
        self.df = dict()
        v, d = self.inOut.readDocsVector()
        for i in range(1, 38729):
            for j in v:
                if i in j.keys():
                    self.df.setdefault(str(i), []).append(j[i])
                else:
                    self.df.setdefault(str(i), []).append(0)
        self.df = pd.DataFrame(self.df)
        self.df.index=d
        print('phase 1 completed')
        # print(self.df.head())
        # self. df = pd.DataFrame({
        #     '1': [12, 20, 28, 18, 29, 33, 24, 45, 45, 52, 51, 52, 55, 53, 55, 61, 64, 69, 72],
        #     '2': [39, 36, 30, 52, 54, 46, 55, 59, 63, 70, 66, 63, 58, 23, 14, 8, 19, 7, 24]
        # })

    def similarity(self, centroids, k):
        for i in range(k):
            d = (self.df.sub(centroids.iloc[i, :]) ** 2).sum(axis=1)
            # d = d ** 2
            # powSum = d.sum(axis=1)
            self.df['distance_from_{}'.format(i)] = (
                np.sqrt(d)
            )
        centroid_distance_cols = ['distance_from_{}'.format(i) for i in range(k)]
        self.df['closest'] = self.df.loc[:, centroid_distance_cols].idxmin(axis=1)
        self.df['closest'] = self.df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
        return self.df

    def updateCentroids(self, centroids, k):
        for i in range(k):
            # if len(self.df.loc[self.df['closest'] == i]) > 0:
            centroids.iloc[i] = self.df.loc[self.df['closest'] == i, [str(l) for l in range(1,38729)]].mean()#no.features 38729
        return centroids

    def cluster(self, k):
        # centroids = {
        #     i + 1: self.df.loc[np.random.randint(0,18)] for i in range(k)
        # }
        # centroids = self.df.ix[np.random.sample(self.df.index, k)]
        centroids = self.df.sample(n = k)
        centroids.index = range(k)
        # np.random.seed(200)
        # centroids = pd.DataFrame({
        #     str(i): [np.random.randint(0, 80) for i in range(k)]
        #     for i in range(1,3) #no.feature38729
        # })
        self.similarity(centroids, k)
        print('sim1')
        a = 0
        while True:
            a += 1
            closest_centroids = self.df['closest'].copy(deep=True)
            centroids= self.updateCentroids(centroids,k)
            print('update')
            self.similarity(centroids, k)
            if closest_centroids.equals(self.df['closest']) or a == 10:
                break
        dist = self.RSSmeasure(centroids, self.df)

        finalcenters = {str(i):{j+1: list(centroids.loc[i, :])[j] for j in range(0, 38728)} for i in range(k)}#no feature-1
        # print(finalcenters)
        self.inOut.writeCentroids(finalcenters, k)
        finalCluster = {str(i): list(self.df.index[self.df['closest'] == i]) for i in range(k)}
        # print(finalCluster)
        self.inOut.writeClusters(finalCluster, k)
        # colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'y', 5:'black', 0:'brown'}
        # fig = plt.figure(figsize=(5, 5))
        # l = []
        # print(self.df)
        # for d in self.df['closest']:
        #     l.append(colmap[d])
        # plt.scatter(self.df['1'], self.df['2'], color=l, alpha=0.5, edgecolor='k')
        # for i in range(k):
        #     plt.scatter(*centroids[i], color=colmap[i])
        # plt.xlim(0, 80)
        # plt.ylim(0, 80)
        # plt.show()
        print(dist)
        return dist

    def RSSmeasure(self, centroids, df):
        dist = 0
        for i in range(len(self.df.index)):#no. doc
            dist += self.df.iloc[i]['distance_from_'+str(int(self.df.iloc[i]['closest']))] ** 2
        return dist

k = Kmean()
dists = []
for i in range(8,10):
    dists.append(k.cluster(i+1))
print(dists)
plt.plot([j for j in range(8,10)], dists, color='lightblue', linewidth=1,
         marker='o', markerfacecolor='lightblue', markersize=5)
plt.xlabel('K')
plt.ylabel('RSS')
plt.show()