import os
import json
import requests
from flask import Flask, Response, request, send_from_directory

if not os.environ.get("dbo-userid"):
    import secrets

app = Flask(__name__, static_url_path='', static_folder='')
app.debug = True
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


class SessionAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['SessionKey'] = self.token
        return r

    def __repr__(self):
        return json.dumps({'SessionKey': self.token})


@app.route('/posts')
def get_posts():
    start = request.args.get('start', 0)
    end = request.args.get('end', 50)

    userid = os.environ.get("dbo-userid")
    sessionKey = os.environ.get("dbo-sessionKey")
    url = "http://discoverboard.com/api/users/%s/latest?start=%s&end=%s" % (userid, start, end)
    auth = SessionAuth(sessionKey)
    r = requests.get(url, auth=auth, headers={"User-Agent": "DBoT"})
    response = Response(json.dumps(r.json()), mimetype='application/json', headers={'Cache-Control': 'no-cache'})
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))
