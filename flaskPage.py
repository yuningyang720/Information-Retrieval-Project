from flask import Flask, render_template, request
from boolean_API import queryURL



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=["POST", "GET"])
def search():

    query = request.args.get('q')  # get the query from placeholder
    urlList, search_time = queryURL(query)

    string = ''
    string += f'<p>Results:\n</p>'
    for web in urlList:
        string += f'<p>{web}</p>'
    string += f'<p>total search time: {search_time} ms.'

    return f'{string}' \
                f'<form action="/" method="get"> \
                    <input type="submit" value="Back"> \
                </form>'



if __name__ == '__main__':
    app.run()
