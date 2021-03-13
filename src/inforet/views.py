from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, render
from BusinessLayer.indexing import Index
from BusinessLayer.query import QueryProc
from BusinessLayer.queryProcessing import Query
from django.views import generic
from BusinessLayer.similarity import Similiarity
from BusinessLayer.sort import TimeSorting
from BusinessLayer.sameNews import SimilarNews

sn = SimilarNews()
s = Similiarity()
indexList = None
docList = None
data = None
relatedNews = None
paginator = None


def similarityHome(request):
    return render(request, 'inforet/similarityHomepage.html')


def simpleHome(request):
    return render(request, 'inforet/homepage.html')


def dq_editor(data):
    if "“" in data:
        data = data.replace("“", "\"")
    if "”" in data:
        data = data.replace("”", "\"")
    return data


def get_queryset_similarity(request):
    global data, indexList, paginator, docList
    data = dq_editor(request.GET.get('query'))
    docList, indexList = s.process_query(data, 100)

    page = request.GET.get('page', 1)

    paginator = Paginator(docList, 8)
    try:
        docIds = paginator.page(page)
    except PageNotAnInteger:
        docIds = paginator.page(1)
    except EmptyPage:
        docIds = paginator.page(paginator.num_pages)

    return render(request, 'inforet/similarityIndex.html',
                  {'form': docIds, 'indexList': indexList[0:len(docIds)], 'query': data, })


def get_queryset(request):
    global data, indexList, paginator, docList
    data = dq_editor(request.GET.get('query'))
    q1 = QueryProc()
    docList, indexList = q1.processQuery(data)

    page = request.GET.get('page', 1)

    paginator = Paginator(docList, 8)
    try:
        docIds = paginator.page(page)
    except PageNotAnInteger:
        docIds = paginator.page(1)
    except EmptyPage:
        docIds = paginator.page(paginator.num_pages)

    return render(request, 'inforet/index.html',
                  {'form': docIds, 'indexList': indexList[0:len(docIds)], 'query': data})


def get_news_url(request, doc_id):
    return render(request, 'inforet/news.html', {'doc_id': int(doc_id)})


def get_other_page(request, other_page):
    page_num = int(other_page)
    print("other page : " + str(other_page))
    docIds = paginator.get_page(page_num)
    print(docIds)
    for x in docIds:
        print(x)
    print("ey baba")
    print(indexList)
    return render(request, 'inforet/index.html',
                  {'form': docIds, 'indexList': indexList[(page_num - 1) * 8:(page_num - 1) * 8 + len(docIds)],
                   'query': data})


def get_other_page_cluster(request, other_page):
    page_num = int(other_page)
    print("other page : " + str(other_page))
    docIds = paginator.get_page(page_num)
    print(docIds)
    for x in docIds:
        print(x)
    print("ey baba")
    print(indexList)
    return render(request, 'inforet/clusterIndex.html',
                  {'form': docIds, 'indexList': indexList[(page_num - 1) * 8:(page_num - 1) * 8 + len(docIds)],
                   'query': data, 'related': relatedNews})

def time_sort(request):
    print(docList)
    print(indexList)
    print("timeeeeee")
    s = TimeSorting(docList, indexList)
    doc_ids, index_lists = s.sort()
    page = request.GET.get('page', 1)

    paginator = Paginator(doc_ids, 8)
    try:
        docIds = paginator.page(page)
    except PageNotAnInteger:
        docIds = paginator.page(1)
    except EmptyPage:
        docIds = paginator.page(paginator.num_pages)

    return render(request, 'inforet/index.html',
                  {'form': docIds, 'indexList': index_lists[0:len(docIds)], 'query': data})


def clusterHome(request):
    return render(request, 'inforet/clusterHomepage.html')


def get_queryset_clustering(request):
    global data, indexList, paginator, docList, relatedNews
    data = dq_editor(request.GET.get('query'))

    dcl, indxl, relatedNews = sn.findSimilarNews(data, 100)
    docList, indexList = dcl[0], indxl[0]
    print("len doclist:")
    print(len(docList))
    print("len indexList:")
    print(len(indexList))
    print("relatedNews:")
    print(relatedNews)
    page = request.GET.get('page', 1)

    paginator = Paginator(docList, 8)
    try:
        docIds = paginator.page(page)
    except PageNotAnInteger:
        docIds = paginator.page(1)
    except EmptyPage:
        docIds = paginator.page(paginator.num_pages)

    return render(request, 'inforet/clusterIndex.html',
                  {'form': docIds, 'indexList': indexList[0:len(docIds)], 'query': data, 'related': relatedNews})