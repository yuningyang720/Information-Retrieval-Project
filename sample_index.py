import os
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import json
from bs4 import BeautifulSoup
import math

import sys


class posting:
    def __init__(self, docid, tfidf, fields):
        self.docid = docid
        self.tfidf = tfidf  # use freq counts for now
        self.fields = fields  # the importance


def fetch(file, num_file, dic):
    f = open(file, encoding='utf-8').read()
    json_file = json.loads(f)
    url = json_file["url"]  # get the url
    soup = BeautifulSoup(json_file["content"].encode(json_file["encoding"], "strict"), "html.parser")

    use_stemmer = PorterStemmer()
    # Use previous Assignment tokenizer style
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
    text = soup.get_text().lower()  # get content using the beautiful soup
    tokens = [use_stemmer.stem(word) for word in tokenizer.tokenize(text)]

    num_tokens = len(tokens)

    # distribute words based on their fields.
    h1, h2, h3, b = [], [], [], []


    for word in soup.find_all('h1'):
        h1 += tokenizer.tokenize(word.get_text().lower())
    for word in soup.find_all('h2'):
        h2 += tokenizer.tokenize(word.get_text().lower())
    for word in soup.find_all('h3'):
        h3 += tokenizer.tokenize(word.get_text().lower())
    for word in soup.find_all('b'):
        b += tokenizer.tokenize(word.get_text().lower())

    stemmer = PorterStemmer()
    h1 = set(stemmer.stem(word) for word in h1)
    h2 = set(stemmer.stem(word) for word in h2)
    h3 = set(stemmer.stem(word) for word in h3)
    b = set(stemmer.stem(word) for word in b)

    frequency_dict = {}
    for word in tokens:
        if word in frequency_dict:
            frequency_dict[word] += 1
        else:
            frequency_dict[word] = 1
    for word, freq in frequency_dict.items():
        freq_tf = freq / num_tokens  # get the term frequency

        #give weight to different fields
        importance = int(word in h1) * 0.5 + int(word in h2) * 0.25 + int(word in h3) * 0.15 + int(word in b) * 0.1

        if word not in dic:
            dic[word] = [posting(num_file, freq_tf, importance).__dict__]
        else:
            dic[word].append(posting(num_file, freq_tf, importance).__dict__)

    return dic, url, frequency_dict  # f_dict


if __name__ == "__main__":
    num_file = 0
    table = ""
    token_set = set()
    dic = {}
    urlDict = {}
    urlD = {}
    with open("index_table.txt", "a", encoding='windows-1252') as ez_index, open("token_posting.txt", "a",
                                                                                 encoding='windows-1252') as token_posting, open(
            "document_info1.txt", "a", encoding='windows-1252') as document_info1, open("document_info2.txt", "a",
                                                                                        encoding='windows-1252') as document_info2, open(
            "document_info3.txt", "a", encoding='windows-1252') as document_info3, open("url.txt", "a",
                                                                                        encoding='windows-1252') as urlFile:
        for root0, dirs0, files0 in os.walk("ANALYST"):
            for dir in dirs0:
                for root1, dirs1, files1 in os.walk(root0 + os.path.sep + dir):
                    for file in files1:
                        num_file += 1

                        dic, url, freq = fetch(root0 + os.path.sep + dir + os.path.sep + file, num_file, dic)
                        urlD[num_file] = url

                        urlDict[num_file] = (url, freq)

                        # off load the inverted index to a partial index on disk 3 times
                        if num_file == 20000:
                            json.dump(dic, document_info1)
                            dic = {}
                        elif num_file == 40000:
                            json.dump(dic, document_info2)
                            dic = {}
                        elif num_file == 55393:
                            json.dump(dic, document_info3)
                            dic = {}

        table += "Documents num: " + str(num_file) + "\n" + "Token num:" + str(len(dic.keys())) + "\n"

        ez_index.write(table)

        for word, postings in dic.items():
            df = len(postings)
            for post in postings:
                post['tfidf'] = post['tfidf'] * math.log(num_file / df, 10) # calculate the TFIDF score


        json.dump(urlD, urlFile)


        print(sys.getsizeof(dic))
        print(num_file)

        ez_index.close()
