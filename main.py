from flask import Flask, jsonify, request, redirect, session, url_for, make_response
from flask_session import Session
import requests
from requests_oauthlib import OAuth2Session
import os
import redis
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379, db=0)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

Session(app)

client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'REDIRECT_URI'
scopes = ['openid', 'email', 'profile']

@app.route('/')
def home():
    return jsonify(message="Welcome to the aspine")

@app.route('/OAuth2/login')
def get_data():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
    authorization_url, state = oauth.authorization_url(authorization_base_url, access_type="offline", prompt="select_account")
    session['oauth_state'] = state
    #res = make_response()
    #res.set_cookie('state', state)
    print(f"Session at login: {session}")
    return redirect(authorization_url)

@app.route('/OAuth2/callback')
def callback():
    #session['oauth_state'] = request.cookies.get('state')
    print(f"Session in callback: {session}")
    if 'oauth_state' in session:
        print(f"State in session at callback: {session['oauth_state']}")
    else:
        print("No state in session")
        return jsonify(message="No state in session")
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['oauth_state'])
    token = oauth.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)
    session['oauth_token'] = token
    print(f"Session in callback: {session}")
    return redirect(url_for('fetch_data'))

@app.route('/OAuth2/fetch_data')
def fetch_data():
    oauth = OAuth2Session(client_id, token=session['oauth_token'])
    response = oauth.get('https://aspen.cpsd.us/app/rest/aasp/login?homepageUrl=https://aspen.cpsd.us/aspen-login/aaspLogin&organizationOid=*dst&idpName=Cambridge%20Google%20SAML')
    return response.json()

def get_sessionid():
    url = "https://aspen.cpsd.us/aspen/logon.do"

    session = requests.Session()
    response = session.get(url)
    
    sessionid = session.cookies.get_dict().get('JSESSIONID')

    return sessionid

@app.route('/api/getsaml', methods=['GET'])
def get_data():
    session = requests.Session()
    session.get("https://aspen.cpsd.us/aspen/logon.do")
    response = session.get("https://aspen.cpsd.us/app/rest/aasp/login?homepageUrl=https://aspen.cpsd.us/aspen-login/aaspLogin&organizationOid=*dst&idpName=Cambridge%20Google%20SAML")

    decodedurl = unquote(response.url)\
    
    samlurl = decodedurl.split("SAMLRequest=")[1]
    samlurl = samlurl.split("&Relay")[0]

    html = response.text

    return jsonify({"status": "success"}, {"responseurl": samlurl})

if __name__ == '__main__':
    app.run(debug=True)