import pandas as pd
from django import template
import re
# from hazm import *
from BusinessLayer.textOperations import FormWords

# nor = Normalizer()

register = template.Library()
# sheet = pd.read_excel(r'C:/Users/mahdis/PycharmProjects/phase2/news.xlsx')
sheet = pd.read_csv(r'C:/Users/mahdis/PycharmProjects/phase2/nnews.csv')


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, ' ', raw_html)
    return cleantext


@register.simple_tag
def get_publish_date(docID):
    return sheet.loc[docID-1][0]


@register.simple_tag
def get_title(docID):
    return sheet.loc[docID-1][1]


@register.simple_tag
def get_url(docID):
    return sheet.loc[docID-1][2]


@register.simple_tag
def get_summary(docID):
    return sheet.loc[docID-1][3]


@register.simple_tag
def get_meta_source_url(self, docID):
    return self.sheet.loc[docID-1][4]

@register.simple_tag
def get_meta_tags(self, docID):
    # return self.sheet.loc[docID-1][4]
    return self.sheet.loc[docID-1][5]


@register.simple_tag
def get_content(docID):
    # return sheet.loc[docID-1][5]
    return sheet.loc[docID-1][6]


@register.simple_tag
def get_related_content(docID, indexList, n):
    # content = cleanhtml(sheet.loc[docID-1][5])

    content = cleanhtml(sheet.loc[docID-1][6])
    # wordFormer = FormWords()
    # content = wordFormer.normalize(content)
    # splitted = wordFormer.tokenize(content)
    # splitted = list(filter(lambda a: a != '\n', splitted))
    # for x in indexList[n-1]:
    #     splitted[x-1] = "<b>"+splitted[x-1]+"</b>"
    # modified_content = ' '.join(splitted[(indexList[n-1][0]-4):])
    # return modified_content
    return content


@register.simple_tag
def get_thumbnail(docID):
    # print("docid")
    # print(docID)
    # return sheet.loc[docID-1][6]
    return sheet.loc[docID-1][9]

@register.simple_tag
def get_category(docID):
    return sheet.loc[docID-1][7]

@register.simple_tag
def get_subcategory(docID):
    return sheet.loc[docID-1][8]
