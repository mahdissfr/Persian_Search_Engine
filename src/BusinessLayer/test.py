# # import codecs
# # import re
# # from os import path
# #
# # data_path = path.join(path.dirname(__file__), 'data')
# # default_words = path.join(data_path, 'words.dat')
# # default_verbs = path.join(data_path, 'verbs.dat')
# #
# #
# # class Tokenizer:
# #     def __init__(self, words_file=default_words, verbs_file=default_verbs, join_verb_parts=True, separate_emoji=False,
# #                  replace_links=False, replace_IDs=False, replace_emails=False, replace_numbers=False,
# #                  replace_hashtags=False):
# #         self._join_verb_parts = join_verb_parts
# #         self.separate_emoji = separate_emoji
# #         self.replace_links = replace_links
# #         self.replace_IDs = replace_IDs
# #         self.replace_emails = replace_emails
# #         self.replace_numbers = replace_numbers
# #         self.replace_hashtags = replace_hashtags
# #
# #         self.pattern = re.compile(r'([؟!\?]+|\d[\d\.:/\\]+|[:\.،؛»\]\)\}"«\[\(\{])')  # TODO \d
# #         self.emoji_pattern = re.compile(u"["
# #                                         u"\U0001F600-\U0001F64F"  # emoticons
# #                                         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
# #                                         u"\U0001F4CC\U0001F4CD"  # pushpin & round pushpin
# #                                         "]", flags=re.UNICODE)
# #         self.emoji_repl = r'\g<0> '
# #         self.id_pattern = re.compile(r'([^\w\._]+)(@[\w_]+)')
# #         self.id_repl = r'\1ID'
# #         self.link_pattern = re.compile(
# #             r'((https?|ftp):\/\/)?(?<!@)([wW]{3}\.)?(([\w-]+)(\.(\w){2,})+([-\w@:%_\+\/~#?&]+)?)')
# #         self.link_repl = r'LINK'
# #         self.email_pattern = re.compile(r'[a-zA-Z0-9\._\+-]+@([a-zA-Z0-9-]+\.)+[A-Za-z]{2,}')
# #         self.email_repl = r'EMAIL'
# #         self.number_int_pattern = re.compile(r'([^\.,\w]+)([\d۰-۹]+)([^\.,\w]+)')
# #         self.number_int_repl = lambda m: m.group(1) + 'NUM' + str(len(m.group(2))) + m.group(3)
# #         self.number_float_pattern = re.compile(r'([^,\w]+)([\d۰-۹,]+[\.٫]{1}[\d۰-۹]+)([^,\w]+)')
# #         self.number_float_repl = r'\1NUMF\3'
# #         self.hashtag_pattern = re.compile(r'\#([\S]+)')
# #         # NOTE: python2.7 does not support unicodes with \w  Example: r'\#([\w\_]+)'
# #
# #         self.hashtag_repl = lambda m: 'TAG ' + m.group(1).replace('_', ' ')
# #
# #         self.words = {item[0]: (item[1], item[2]) for item in self.words_list(default_words)}
# #
# #         self.pattern2 = re.compile(r'([!\.\?⸮؟]+)[ \n]+')
# #
# #         if join_verb_parts:
# #             self.after_verbs = set([
# #                 'ام', 'ای', 'است', 'ایم', 'اید', 'اند', 'بودم', 'بودی', 'بود', 'بودیم', 'بودید', 'بودند', 'باشم',
# #                 'باشی', 'باشد', 'باشیم', 'باشید', 'باشند',
# #                 'شده_ام', 'شده_ای', 'شده_است', 'شده_ایم', 'شده_اید', 'شده_اند', 'شده_بودم', 'شده_بودی', 'شده_بود',
# #                 'شده_بودیم', 'شده_بودید', 'شده_بودند', 'شده_باشم', 'شده_باشی', 'شده_باشد', 'شده_باشیم', 'شده_باشید',
# #                 'شده_باشند',
# #                 'نشده_ام', 'نشده_ای', 'نشده_است', 'نشده_ایم', 'نشده_اید', 'نشده_اند', 'نشده_بودم', 'نشده_بودی',
# #                 'نشده_بود', 'نشده_بودیم', 'نشده_بودید', 'نشده_بودند', 'نشده_باشم', 'نشده_باشی', 'نشده_باشد',
# #                 'نشده_باشیم', 'نشده_باشید', 'نشده_باشند',
# #                 'شوم', 'شوی', 'شود', 'شویم', 'شوید', 'شوند', 'شدم', 'شدی', 'شد', 'شدیم', 'شدید', 'شدند',
# #                 'نشوم', 'نشوی', 'نشود', 'نشویم', 'نشوید', 'نشوند', 'نشدم', 'نشدی', 'نشد', 'نشدیم', 'نشدید', 'نشدند',
# #                 'می‌شوم', 'می‌شوی', 'می‌شود', 'می‌شویم', 'می‌شوید', 'می‌شوند', 'می‌شدم', 'می‌شدی', 'می‌شد', 'می‌شدیم',
# #                 'می‌شدید', 'می‌شدند',
# #                 'نمی‌شوم', 'نمی‌شوی', 'نمی‌شود', 'نمی‌شویم', 'نمی‌شوید', 'نمی‌شوند', 'نمی‌شدم', 'نمی‌شدی', 'نمی‌شد',
# #                 'نمی‌شدیم', 'نمی‌شدید', 'نمی‌شدند',
# #                 'خواهم_شد', 'خواهی_شد', 'خواهد_شد', 'خواهیم_شد', 'خواهید_شد', 'خواهند_شد',
# #                 'نخواهم_شد', 'نخواهی_شد', 'نخواهد_شد', 'نخواهیم_شد', 'نخواهید_شد', 'نخواهند_شد',
# #             ])
# #
# #             self.before_verbs = set([
# #                 'خواهم', 'خواهی', 'خواهد', 'خواهیم', 'خواهید', 'خواهند',
# #                 'نخواهم', 'نخواهی', 'نخواهد', 'نخواهیم', 'نخواهید', 'نخواهند'
# #             ])
# #
# #             with codecs.open(verbs_file, encoding='utf8') as verbs_file:
# #                 self.verbs = list(reversed([verb.strip() for verb in verbs_file if verb]))
# #                 self.bons = set([verb.split('#')[0] for verb in self.verbs])
# #                 self.verbe = set([bon + 'ه' for bon in self.bons] + ['ن' + bon + 'ه' for bon in self.bons])
# #
# #     def words_list(words_file=default_words):
# #         with codecs.open(words_file, encoding='utf-8') as words_file:
# #             items = [line.strip().split('\t') for line in words_file]
# #             return [(item[0], int(item[1]), tuple(item[2].split(','))) for item in items if len(item) == 3]
# #
# #     def sent_tokenize(self, text):
# #         return self.sentence_tokenize(text)
# #
# #     def word_tokenize(self, sentence):
# #         return self.tokenize(sentence)
# #
# #     def tokenize(self, text):
# #
# #         if self.separate_emoji:
# #             text = self.emoji_pattern.sub(self.emoji_repl, text)
# #         if self.replace_links:
# #             text = self.link_pattern.sub(self.link_repl, text)
# #         if self.replace_IDs:
# #             text = self.id_pattern.sub(self.id_repl, text)
# #         if self.replace_emails:
# #             text = self.email_pattern.sub(self.email_repl, text)
# #         if self.replace_hashtags:
# #             text = self.hashtag_pattern.sub(self.hashtag_repl, text)
# #         if self.replace_numbers:
# #             text = self.number_int_pattern.sub(self.number_int_repl, text)
# #             text = self.number_float_pattern.sub(self.number_float_repl, text)
# #
# #         text = self.pattern.sub(r' \1 ', text.replace('\n', ' ').replace('\t', ' '))
# #
# #         tokens = [word for word in text.split(' ') if word]
# #         if self._join_verb_parts:
# #             tokens = self.join_verb_parts(tokens)
# #         return tokens
# #
# #     def join_verb_parts(self, tokens):
# #         """
# #         >>> tokenizer.join_verb_parts(['خواهد', 'رفت'])
# #         ['خواهد_رفت']
# #         >>> tokenizer.join_verb_parts(['رفته', 'است'])
# #         ['رفته_است']
# #         >>> tokenizer.join_verb_parts(['گفته', 'شده', 'است'])
# #         ['گفته_شده_است']
# #         >>> tokenizer.join_verb_parts(['گفته', 'خواهد', 'شد'])
# #         ['گفته_خواهد_شد']
# #         >>> tokenizer.join_verb_parts(['خسته', 'شدید'])
# #         ['خسته', 'شدید']
# #         """
# #
# #         result = ['']
# #         for token in reversed(tokens):
# #             if token in self.before_verbs or (result[-1] in self.after_verbs and token in self.verbe):
# #                 result[-1] = token + '_' + result[-1]
# #             else:
# #                 result.append(token)
# #         return list(reversed(result[1:]))
# #
# #     def sentence_tokenize(self, text):
# #         text = self.pattern2.sub(r'\1\n\n', text)
# #         return [sentence.replace('\n', ' ').strip() for sentence in text.split('\n\n') if sentence.strip()]
# from hazm import *
# print(word_tokenize('2365'))
#
# from .stemmer import Stemmer
# from hazm import *
# from os import path
#
# data_path = path.join(path.dirname(__file__), 'data')
# default_words = path.join(data_path, 'words.dat')
# default_verbs = path.join(data_path, 'verbs.dat')
#
#
# class Lemmatizer():
#     def __init__(self, words_file=default_words, verbs_file=default_verbs, joined_verb_parts=True):
#         self.verbs = {}
#         self.stemmer = Stemmer()
#
#         tokenizer = WordTokenizer(words_file=default_words, verbs_file=verbs_file)
#         self.words = tokenizer.words
#
#         if verbs_file:
#             self.verbs['است'] = '#است'
#             for verb in tokenizer.verbs:
#                 for tense in self.conjugations(verb):
#                     self.verbs[tense] = verb
#             if joined_verb_parts:
#                 for verb in tokenizer.verbs:
#                     bon = verb.split('#')[0]
#                     for after_verb in tokenizer.after_verbs:
#                         self.verbs[bon + 'ه_' + after_verb] = verb
#                         self.verbs['ن' + bon + 'ه_' + after_verb] = verb
#                     for before_verb in tokenizer.before_verbs:
#                         self.verbs[before_verb + '_' + bon] = verb
#
#     def lemmatize(self, word, pos=''):
#         if not pos and word in self.words:
#             return word
#
#         if (not pos or pos == 'V') and word in self.verbs:
#             return self.verbs[word]
#
#         if pos.startswith('AJ') and word[-1] == 'ی':
#            + with_nots(present_simples) + with_nots(
#                 present_imperfects) + present_subjunctives + present_not_subjunctives + imperatives)
from DataLayer.constants import ConstantVars
from BusinessLayer.textOperations import FormWords
wordFormer = FormWords()
constants = ConstantVars()
query_tokens = wordFormer.tokenize("شفاف سازی")
print('query tokens')
print(query_tokens)
postaged_tokens = wordFormer.posTagging(query_tokens)
print(postaged_tokens)
stemmed_tokens = wordFormer.stemmWords(query_tokens, len(query_tokens))
print(stemmed_tokens)
lemmatized_tokens = wordFormer.lemmatizeWords(stemmed_tokens, postaged_tokens, len(query_tokens))
print(lemmatized_tokens)

for token in lemmatized_tokens:
    if token in constants.punctuations() or token in constants.StopWords():
        lemmatized_tokens.remove(token)
print(lemmatized_tokens)