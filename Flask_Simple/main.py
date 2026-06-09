from flask import Flask

app= Flask(__name__)

@app.route("/hello")
def hello_world():
    return "<h1>Hello , Dieu Merci</h1>"
    