# This file provided by Facebook is for non-commercial testing and evaluation purposes only.
# Facebook reserves all rights not expressly granted.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# FACEBOOK BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import json
import requests
from flask import Flask, Response, request, send_from_directory

if not os.environ.get("dbo-userid"):
    import secrets

app = Flask(__name__, static_url_path='', static_folder='')
app.debug = True
app.add_url_rule('/', 'root', lambda: app.send_static_file('demo-on.html'))


@app.route('/inf')
def inf():
    return send_from_directory('', 'demo-on.html')


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


@app.route('/comments.json', methods=['GET', 'POST'])
def comments_handler():

    with open('comments.json', 'r') as file:
        comments = json.loads(file.read())

    if request.method == 'POST':
        comments.insert(0, request.form.to_dict())

        with open('comments.json', 'w') as file:
            file.write(json.dumps(comments, indent=4, separators=(',', ': ')))

    return Response(json.dumps(comments), mimetype='application/json', headers={'Cache-Control': 'no-cache'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))
