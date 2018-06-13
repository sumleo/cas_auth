from flask import Flask, jsonify
import requests
import bs4
from flask import request
import json
app = Flask(__name__)

def cas_login(username,password):
    url="https://cas.sustc.edu.cn/cas/login"
    #init
    sess=requests.session()
    #pre login
    res=sess.get(url)
    formatedHTML=bs4.BeautifulSoup(res.text,"lxml")
    execution=formatedHTML.select('input[name$="execution"]')[0]["value"]
    data={
        "username":username,
        "password":password,
        "execution":execution,
        "_eventId":"submit",
        "geolocation":"",
    }
    #login part
    logined=sess.post(url,data=data)
    successed=len(logined.text.replace("Log In Successful",""))<len(logined.text) or len(logined.text)>len(logined.text.replace("登录成功",""))
    return successed
@app.route('/casAuth',methods=["POST"])
def cas_auth_post():
    data = request.get_json()
    result = cas_login(data["username"], data["password"])
    data = {}
    if (result):
        data['result'] = 'success'
    else:
        data['result'] = "failed"
    return jsonify(data)
@app.route('/casAuth/<username>/<password>')
def cas_auth(username,password):
    result=cas_login(username,password)
    data={}
    if(result):
        data['result']='success'
    else:
        data['result'] ="failed"
    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
