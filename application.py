import numpy as np
from flask import Flask, redirect, url_for, render_template, request, Response, abort
from flask_login import LoginManager, login_required, login_user, logout_user
from sklearn.metrics.pairwise import cosine_similarity
from utils import *
import time
from flask import stream_with_context


application = Flask(__name__)

application.url_map.converters['list'] = ListConverter


@application.route('/')
def home():
    return render_template('index.html')


@application.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        capa1 = request.form['capability1']
        capa2 = request.form['capability2']
        capa3 = request.form['capability3']
        capa4 = request.form['capability4']
        capa5 = request.form['capability5']
        cap1 = request.form['cap1']
        cap2 = request.form['cap2']
        cap3 = request.form['cap3']
        cap4 = request.form['cap4']
        cap5 = request.form['cap5']

        return redirect(url_for('cap_search', argus=[cap1, capa1,
                                                     cap2, capa2,
                                                     cap3, capa3,
                                                     cap4, capa4,
                                                     cap5, capa5]))


@application.route('/cresult/<list:argus>')
def cap_search(argus):
    print('key and PG=', argus)
    cap1, capa1, \
    cap2, capa2,\
    cap3, capa3,\
    cap4, capa4,\
    cap5, capa5 = argus

    cap1 = int(cap1)
    cap2 = int(cap2)
    cap3 = int(cap3)
    cap4 = int(cap4)
    cap5 = int(cap5)

    all_docs = pd.read_pickle("./fake_data_scientists.pkl")

    df = all_docs[(all_docs[capa1] >= cap1) &
                  (all_docs[capa2] >= cap2) &
                  (all_docs[capa3] >= cap3) &
                  (all_docs[capa4] >= cap4) &
                  (all_docs[capa5] >= cap5)]

    print(df.shape[0])

    if df.shape[0] == 0:
        return "<html><body><h1>Keyword not found!</h1><h1><button onclick='goBack()'>Go Back</button><script>function \
        goBack() {window.history.back();}</script></h1></body></html>"
    else:
        string = write_table(df)
        # return render_template('key_results.html')
        return string


@application.route('/result/<int:name>')
def result(name):
    all_docs = pd.read_pickle("./fake_data_scientists.pkl")
    df = all_docs[all_docs['WWID']==name]
    if df.shape[0] == 0:
        return "<a href='{{ url_for('home') }}'>Home</a> <html><body><h1>No WWID found!</h1><h1><button onclick='goBack()'>Go Back</button><script>function \
        goBack() {window.history.back();}</script></h1></body></html>"
    else:
        #df2 = df.drop(["Cleaned Responsibilities"], axis=1)
        #df2 = df2.drop(["tfidf_vectors"], axis=1)
        dic = df.to_dict('list')
        return render_template('result.html', result=dic)


if __name__ == '__main__':
    # application.debug = True
    application.run()
