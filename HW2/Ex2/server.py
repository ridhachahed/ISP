from flask import Flask, request, make_response, abort
import os
import hmac
import hashlib
import time
import base64

app = Flask(__name__)

cookie_name = "LoginCookie"
secret_key = os.urandom(24)


@app.route("/login", methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']
    time_stamp = int(time.time())
    res = make_response("Setting a cookie")

    if username == 'admin' and password == '42':
        msg = '{},{},com402,hw2,ex2,admin'.format(username, time_stamp)
    else:
        msg = '{},{},com402,hw2,ex2,user'.format(username, time_stamp)
    mac = hmac.new(secret_key, msg=msg.encode('utf-8'))
    value = msg + ',{}'.format(mac.hexdigest())
    res.set_cookie(cookie_name, base64.b64encode(value.encode('utf-8')), max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/auth", methods=['GET'])
def auth():
    cookie = request.cookies.get('LoginCookie')
    if cookie:
        cookie = base64.b64decode(cookie).decode('utf-8').split(',')
        mac = cookie[-1]
        msg = ','.join(cookie[:-1])
        if mac != hmac.new(secret_key, msg=msg.encode('utf-8')).hexdigest():
            return abort(403, 'Cookie tampered')
        else:
            if cookie[-2] == 'admin':
                return make_response('User is admin', 200)
            else:
                return make_response('Simple user', 201)
    else:
        return abort(403, 'No cookie')


if __name__ == '__main__':
    app.run()
