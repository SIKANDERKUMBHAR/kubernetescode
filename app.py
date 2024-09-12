from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Please subscribe, This is me Sikander Ali deployed with Argocd(cd) and jenkins(ci)!!'
