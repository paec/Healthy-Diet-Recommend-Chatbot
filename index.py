from flask import Flask, session
from flask import request
import flask
from flask_session import Session
import requests
from bs4 import BeautifulSoup
from flask import jsonify
from flask import render_template
from flask_bootstrap import Bootstrap
import json
import testmongo
import sys
import MER
from time import sleep

app = Flask(__name__)




@app.route('/')

def hello():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])

def MER_predict():

    result = MER.predict(request.form.get('inputtext')) #回傳後為字串
    # resp = flask.make_response(jsonify(result))
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # resp.headers['Access-Control-Allow-Methods'] = 'POST'
    # resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type' 

    return jsonify(result)


@app.route('/getfood',methods=['POST'])

def getfood():

    dislist = json.loads(request.form.get('inputtext'))
    result2 = dict()

    for dis in dislist:
        result2[dis] = json.loads(testmongo.getfood(dis))

    result2 = json.dumps(result2,ensure_ascii=False)
    # resp = flask.make_response(jsonify(result2))
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # resp.headers['Access-Control-Allow-Methods'] = 'POST'
    # resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type' 

    return jsonify(result2) 


@app.route('/getaudio',methods=['POST'])
def listentoDB():
    requests.post('https://www.ilovetogether.com/Karaoke_Battle/tmp_delete.php')
    while True: 
        print("request")
        r = requests.post('https://www.ilovetogether.com/Karaoke_Battle/tmp_listening.php')
        if r.text!="none":
            return r.text
        elif r.text=="_stop_":
            return r.text
        sleep(1.5)
    # return r.text

@app.route('/stopaudio',methods=['POST'])
def sendStop():
    print("snedstop")
    r = requests.post('https://www.ilovetogether.com/Karaoke_Battle/tmp.php',{"text":"_stop_"})
    return ""
    




# -----------------------------------------------------------------------------------------------

app.run(host='0.0.0.0' , port=5000, debug=True)


