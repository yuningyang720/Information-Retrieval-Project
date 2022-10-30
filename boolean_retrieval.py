import os
import time
import json
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from urllib.parse import urldefrag
import time


if __name__ == "__main__":
    with open("document_info1.txt") as documentsFile1, open("document_info2.txt") as documentsFile2, open(
            "document_info3.txt") as documentsFile3, open("url.txt") as urlFile:
        documents1 = json.load(documentsFile1)
        documents2 = json.load(documentsFile2)
        documents3 = json.load(documentsFile3)
        documents = []
        documents.append(documents1)
        documents.append(documents2)
        documents.append(documents3)

        urls = json.load(urlFile)

    print("Welcome to the search engine!\n")
    while True:

        query = input("Please enter your query, type 'quit' to stop:\n")
        if query == "quit":
            break

        start = time.time()

        use_stemmer = PorterStemmer()
        tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
        tokens = [use_stemmer.stem(word) for word in tokenizer.tokenize(query.lower())]

        print("\nResults:\n")
        webs = set()

        dic = {}

        result = {}

        combined_dict = {}

        # record all different webs based on each token
        for i in tokens:

            for document in documents:
                if i in document:
                    if i in combined_dict:
                        combined_dict[i].extend(document[i])
                    else:
                        combined_dict[i] = document[i]

        no_match = 0
        num_list = []  # [[#,#,#,#], [#,#,#,#]    ...  ]
        for token in tokens:
            cur = set()

            if token not in combined_dict:
                print("no matched website")
                no_match = 1
            if no_match == 1:
                break
            for posting in combined_dict[token]:
                cur.add(posting['docid'])
            num_list.append(cur)

        if no_match == 1:
            continue

        intersect_set = num_list[0]
        for each in num_list:
            intersect_set = intersect_set.intersection(each)

        for token in tokens:
            for posting in combined_dict[token]:
                if posting['docid'] in intersect_set:
                    if posting['docid'] not in result:
                        result[posting['docid']] = posting['tfidf'] + posting['fields']
                    else:
                        result[posting['docid']] += posting['tfidf'] + posting['fields']

        result = dict(sorted(result.items(), key=lambda x: -x[1]))

        count = 0

        unique = []

        for k, v in result.items():
            count += 1
            if count == 11:  # return top 10 url
                break
            u = urldefrag(urls[str(k)])[0]
            if u in unique:
                count -= 1
                continue
            else:
                unique.append(u)
                print(u)


        end = time.time()  # calculate the search time
        print("total search time: ", 1000 * (end - start), "ms.")

        print()




