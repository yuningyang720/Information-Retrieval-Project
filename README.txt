The Project consisted of 4 main python files, 1 html file under templates and 1 css file under static.

1. sample_index.py
This file is to build inverted index of all tokens in DEV Data files. This process is done well before any query is issued.

2. boolean_retrieval.py
This file is a complete console-based search engine. Results are return as entering query.
We get the documents after the index creation, take the query and then rank the website based on the relevance.

3. boolean_API.py
This file has a function that takes query as an input and return the search results.

4. flaskPage.py
This file is a Web-based search engine.

Run on Local:
sample_index.py and boolean_retrieval.py are needed.
First is to run sample_index.py, we'll get three documents with index and one document with urls.
This four files would be used in next step.
Second is to run boolean_retrieval.py, we'll get a console-based search engine.
It'll return top 10 websites if we enter the query.
Enter "quit" to stop the program.

Run on Web GUI:
sample_index.py, boolean_API.py and flaskPage.py are needed.
First is to run sample_index.py, we'll get three documents with idnex and one document with urls.
This four files would be used in next step.
Second is to run flaskPage.py.
Flask give us a WEB GUI of search engine. We can enter the query in the placeholder and click on search.
As long as we click on the search button, the search function would call the queryURl function from boolean_API.
The queryURL will return a the Top URLs and search time to the flask page and show the results on the website.
