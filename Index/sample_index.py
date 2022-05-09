import os
from nltk.tokenize import RegexpTokenizer
import json
from bs4 import BeautifulSoup
from nltk.stem.porter import *
import sys

class posting:
    def __init__(self, docid, tfidf):
        self.docid = docid
        self.tfidf = tfidf # use freq counts for now
        # self.fields = fields

def fetch(file,num_file, dic):
    f = open(file, encoding = 'utf-8').read()
    json_file = json.loads(f)
    soup = BeautifulSoup(json_file["content"].encode(json_file["encoding"], "strict"), "html.parser")
    f_dict = {}
    use_stemmer = PorterStemmer()
    #Use previous Assignment tokenizer style
    tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]+')
    text = soup.get_text().lower()
    tokens = [use_stemmer.stem(word) for word in tokenizer.tokenize(text)]
    #By adding those constraint but only decrease very few words like 104 token words but I do not know why
    # for word in tokenizer.tokenize(text):
    #     tokenized = re.sub('_', ' ', str(word))
    #     tokenized = tokenized.strip()
    #     if len(tokenized.split()) > 1:
    #         for token in tokenized.split():
    #             stemmed_word = use_stemmer.stem(token)
    #             if len(stemmed_word) >= 2:
    #                 tokens.append(stemmed_word)
    #     else:
    #         # determine if alphanumeric sequences
    #         if len(use_stemmer.stem(tokenized)) >= 2:
    #             tokens.append(use_stemmer.stem(tokenized))
    num_tokens = len(tokens)
    frequency_dict = {}
    for word in tokens:
        if word in frequency_dict:
            frequency_dict[word]+=1
        else:
            frequency_dict[word] = 1
    for word,freq in frequency_dict.items():
            freq_tf = freq/num_tokens
            f_dict[word] = posting(num_file, freq_tf)
            if word not in dic:
                dic[word] = [posting(num_file, freq_tf)]
            else:
                dic[word].append(posting(num_file, freq_tf))
            
    # print(dic)     

    return dic#f_dict


if __name__ == "__main__":
    num_file = 0
    table =""
    token_set = set()
    dic = {}

    with open("index_table.txt", "a", encoding = 'windows-1252') as ez_index:
        for root0, dirs0, files0 in os.walk("DEV"):
            for dir in dirs0:
                for root1, dirs1, files1 in os.walk(root0+os.path.sep+dir):
                    for file in files1:
                        num_file += 1
                        #file_dict = fetch(root0+os.path.sep+dir+os.path.sep+file, num_file, dic)
                        dic = fetch(root0+os.path.sep+dir+os.path.sep+file, num_file, dic)
                        #for word in file_dict:
                            #token_set.add(word)
        table += "Documents num: " + str(num_file) + "\n" +"Token num:"+ str(len(dic.keys())) + "\n"
        
        ez_index.write(table)
        # for word in dic.keys():
        #     token_set.add(word)
        # for i in token_set:
        #     ez_index.write(i)
        # get dictionary size
        print(sys.getsizeof(dic))
        
        ez_index.close()



