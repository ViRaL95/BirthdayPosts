from flask import Flask, redirect, request, session, render_template
from oauth import OAuth
from facebook_requests import FacebookRequests
app = Flask(__name__)
app.secret_key = 'be00ce44e8a48addf582665368a2742f0f037313'
  
@app.route('/')
def start():
    return render_template("index.html", disabled=True)

@app.route("/login")
def login():
    url_root =  request.url_root
    oauth = OAuth(url_root=url_root)
    facebook_url = oauth.facebook_url
    return redirect(facebook_url)

@app.route('/authorized', methods=['GET'])
def authorized():
    url_root = request.url_root
    code = request.args.get('code', '')
    oauth = OAuth(url_root=url_root)
    oauth.retrieve_access_token(code=code)
    return render_template("index.html", disabled=False)

@app.route("/post_comments", methods=['POST'])
def post_comments():
    comment = request.get_json()['comment']
    facebook_request = FacebookRequests()
    facebook_request.retrieve_feed()
    facebook_request.post_comments(comment)

