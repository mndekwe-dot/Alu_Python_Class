from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello , Dieu Merci</h1>"

@app.route("/hello")
def hello_world():
    return "<h1>Hello , Dieu Merci</h1>"

if __name__ == "__main__":
    app.run()
