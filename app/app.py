
import random
import time

from flask import Flask, request, Response, jsonify, session
from flask_cors import CORS, cross_origin
from flask_session import Session
from flaskext.mysql import MySQL

import json

app = Flask(__name__)
CORS(app)

app.secret_key = "netbackup"

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Gyp.s8m'
app.config['MYSQL_DATABASE_DB'] = 'netbackup'
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
mysql.init_app(app)


def saveUser(user, result):
    conn = mysql.connect()
    cur = conn.cursor()
    sql = "INSERT INTO user_result (uname, result) VALUES (%s, %s)"
    print(user,result)
    val = (user, int(result))
    cur.execute(sql, val)
    conn.commit()
    cur.close()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/insert', methods=['POST'])
@cross_origin(supports_credentials=True)
def insert():
    print("in insert")
    content = request.get_json()
    qid = int(content['Qno'])
    question = content['Question']
    option1 = content['Option1']
    option2 = content['Option2']
    option3 = content['Option3']
    option4 = content['Option4']
    answer = int(content['Answer'])
    conn = mysql.connect()
    cur = conn.cursor()
    print(type(qid), type(answer))
    # print("INSERT INTO qna_tbl VALUES(?,?,?,?,?,?,?)" %(qid,question,option1,option2,option3,option4,answer))
    sql = "INSERT INTO qna_tbl (qno, question, op1, op2, op3,op4, answer) VALUES (%s, %s, %s,%s,%s,%s,%s)"
    val = (qid, question, option1, option2, option3, option4, answer)
    cur.execute(sql, val)
    conn.commit()
    cur.close()
    json_data = {
        'status': 0
    }
    print(json_data)
    js = json.dumps(json_data)
    resp = jsonify(js)
    resp.status_code = 200
    return resp


@app.route('/login', methods=['POST'])
@cross_origin(supports_credentials=True)
def login():
    user = request.args.get('user')
    print(user)
    session['username'] = user
    session['noOfQ'] = 1
    session['result'] = 0
    session['setofQ'] = {0: True}
    json_data = {
        'status': 0
    }
    # print(json_data)
    js = json.dumps(json_data)
    resp = jsonify(js)
    resp.status_code = 200
    print(resp)
    return resp


@app.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=False)
def logout():
    session.clear()


@app.route('/getnext', methods=['POST', 'GET'])
@cross_origin(supports_credentials=True)
def get_nextqa():
    content = request.get_json()
    actual = content['Actual']
    selected = content['Selected']
    res = session['result']
    user = session['username']
    setofQ = session['setofQ']
    noq = session['noOfQ']
    print("ss1", actual, selected)
    print(setofQ.keys())
    if actual == selected:
        res = res + 1
        session['result'] = res

    time.sleep(1.2)

    json_data = {}
    if noq == 6:
        session.clear()
        saveUser(user, res)
        json_data = {
            'status': 1,
            'result': res,
            'user': user
        }
        js = json.dumps(json_data)
        resp = jsonify(js)
        resp.status_code = 200
    else:
        rno = 0  # random.randrange(1, 32)
        while True:
            rno = random.randrange(1, 71)
            if str(rno) in setofQ.keys():
                print(str(rno) + " already exists")
                continue
            break
        setofQ[str(rno)] = True
        session['setofQ'] = setofQ
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("select * from qna_tbl where qno=" + str(rno))
        myresult = cur.fetchall()
        #row_headers = [x[0] for x in cur.description]
        #print(row_headers)

        for x in myresult:
            json_data = {
                'qid': str(x[0]),
                'question': x[1],
                'option1': x[2],
                'option2': x[3],
                'option3': x[4],
                'option4': x[5],
                'ans': str(x[6]),
                'status': 0
            }

        cur.close()
        js = json.dumps(json_data)
        print(js)
        resp = jsonify(js)
        resp.status_code = 200
        session['noOfQ'] = noq + 1
        print('sss3', session)
    print(resp)
    return resp


if __name__ == "__main__":
#    app.run(debug=True)
    app.run(host='0.0.0.0')
