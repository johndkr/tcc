from flask import Flask, render_template, request

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

    
if __name__ == "__main__":
    app.run(debug=True)