import os
import time
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from urllib.parse import urldefrag
import time


def queryURL(query):
    """ This function takes a query and return a list of Top 10 Websites and Search time. """
    with open("document_info1.txt") as documentsFile1, open("document_info2.txt") as documentsFile2, open(
            "document_info3.txt") as documentsFile3, open("url.txt") as urlFile:
        # loads the files and returns json object
        documents1 = json.load(documentsFile1)
        documents2 = json.load(documentsFile2)
        documents3 = json.load(documentsFile3)
        documents = []
        documents.append(documents1)
        documents.append(documents2)
        documents.append(documents3)

        urls = json.load(urlFile)

        # start to record the time
        start = time.time()


        use_stemmer = PorterStemmer()  # set up the stemmer for tokenizing
        tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
        tokens = [use_stemmer.stem(word) for word in tokenizer.tokenize(query.lower())]


        result = {}

        combined_dict = {}

        # record all different webs based on each token
        # merging all partial indexes to a same dict
        for i in tokens:
            for document in documents:
                if i in document:
                    if i in combined_dict:
                        combined_dict[i].extend(document[i])
                    else:
                        combined_dict[i] = document[i]


        num_list = []  # [[#,#,#,#], [#,#,#,#]    ...  ]
        no_match = 0
        for token in tokens:
            cur = set()
            if token not in combined_dict:  # no websites found
                print("no matched website")
                no_match = 1
            if no_match == 1:
                break
            for posting in combined_dict[token]:
                cur.add(posting['docid'])
            num_list.append(cur) # add the documents into the list

        end = time.time()  # stop to record the search time

        if no_match == 1:
            return ["no matched website found"], 1000*(end-start)

        intersect_set = num_list[0]  # get the set of document
        for each in num_list:
            intersect_set = intersect_set.intersection(each)  # keep the documents that both have

        for token in tokens:
            for posting in combined_dict[token]:
                if posting['docid'] in intersect_set:
                    if posting['docid'] not in result:
                        result[posting['docid']] = posting['tfidf'] + posting['fields']  # assign score to each document
                    else:
                        result[posting['docid']] += posting['tfidf'] + posting['fields']

        result = dict(sorted(result.items(), key=lambda x: -x[1]))  # ranking the document based on the scores

        count = 0
        urlList = []

        unique = []

        for k, v in result.items():
            count += 1
            if count == 11:  # return only top 10 websites, stop at 11.
                break
            u = urldefrag(urls[str(k)])[0]  # get the url
            if u in unique:
                count -= 1
                continue
            else:
                unique.append(u)
                urlList.append(u)
        end = time.time()  # stop to record the search time


    return urlList, 1000*(end-start)

