from flask import Flask, render_template, request
import json

import sys
sys.path.append('..\\..\\')

from Microsservices.Linguistic import linguistic as Linguistic

ling = Linguistic.LinguisticAnalyses()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['newsLink']
    processed_text = text.upper()
    print (processed_text)
    return render_template("index.html")

@app.route('/get_linguist_prob', methods=['POST'])
def get_linguist_probability():
    data = request.json

    if (data['txt']):
        result = ling.make_linguistic_analyses(data['txt'])
    else:
        result = "Ops... there is no text to be analysed!"

    return result

    
if __name__ == "__main__":
    app.run(debug=True)