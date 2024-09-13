from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Please subscribe, jenkins(ci) and Argocd(cd) commit(7)!!'
