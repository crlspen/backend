from flask import Flask, jsonify, request, redirect, session, url_for
import requests
from requests_oauthlib import OAuth2Session
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://accounts.google.com/o/oauth2/token'
redirect_uri = 'https://2699-2601-184-497f-6409-cc31-ff15-4264-d84b.ngrok-free.app'
scopes = ['openid', 'email', 'profile']
@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API!")

#@app.route('/api/session_id', methods=['GET'])
#def get_data():
    #session = requests.Session() 

    #response = session.get('http://aspen.cpsd.us/aspen/logon.do') 
    
    #return {'session_id': session.cookies.get_dict().get('JSESSIONID')}

@app.route('/api/OAuth2')
def get_data():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)
    authorization_url, state = oauth.authorization_url(authorization_base_url, access_type="offline", prompt="select_account")
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/oauth2/callback')
def callback():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['oauth_state'])
    token = oauth.fetch_token(token_url, authorization_response=request.url, client_secret=client_secret)
    session['oauth_token'] = token
    return jsonify(message="You have successfully logged in!")

@app.route('/fetch_data')
def fetch_data():
    oauth = OAuth2Session(client_id, token=session['oauth_token'])
    response = oauth.get('https://aspen.cpsd.us/app/rest/aasp/login?homepageUrl=https://aspen.cpsd.us/aspen-login/aaspLogin&organizationOid=*dst&idpName=Cambridge%20Google%20SAML')
    return response.json()
if __name__ == '__main__':
    app.run(debug=True)