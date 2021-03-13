from inforet.templatetags.readInputFile import get_publish_date
import re

months = {"January": 0, "February": 1, "March": 2, "April": 3, "May": 4, "June": 5, "July": 6, "August": 7,
          "September": 8, "October": 9,
          "November": 10, "December": 11}


def partition(arr, low, high):
    i = (low - 1)
    pivot = arr[high]
    for j in range(low, high):
        if not (arr[j].time.year < pivot.time.year or arr[j].time.month < pivot.time.month or arr[j].time.day < pivot.time.day or arr[j].time.hour < pivot.time.hour or arr[j].time.minute < pivot.time.minute):
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quickSort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


class Time:
    def __init__(self, doc_id):
        string = get_publish_date(doc_id)
        date, time = string.split(', ')
        date = date.split(" ")
        self.year = date[2]
        self.month = months[date[0]]
        self.day = int(re.split('[a-z|,]+', date[1])[0])
        self.hour, self.minute = list(map(int, time.split(":")[0:2]))


class TimeSorting:
    def __init__(self, doc_ids, index_lists):
        self.docs = []
        for i in range(len(doc_ids) - 1):
            self.docs.append(Doc(doc_ids[i], index_lists[i], Time(doc_ids[i])))

    def sort(self):
        n = len(self.docs)
        quickSort(self.docs, 0, n - 1)
        docs = []
        indexList = []
        for i in range(n-1):
            docs.append(self.docs[i].docId)
            indexList.append(self.docs[i].indexList)
        return docs, indexList

class Doc:
    def __init__(self, doc_id, index_list, time):
        self.docId = doc_id
        self.indexList = index_list
        self.time = time
