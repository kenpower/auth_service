import flask
import logging
import os
import sys
import time
import werkzeug

sys.path.insert(1, os.path.sep.join(sys.path[0].split(os.path.sep)[:-1]) + os.path.sep)

# import config data
import config_data

# from... import
from flask import Flask, jsonify, render_template, request, send_from_directory, session
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth



logging.basicConfig(level=logging.DEBUG)

#Set up Flask:
app = Flask(__name__, 
           
            template_folder="web")

app.secret_key = "secret key" # Replace with your own secret key in production

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' 

CORS(app, supports_credentials=True)

#set up OAuth with MICROSOFT_IDENTITY_PLATFORM (previously known as Azure AD)
MICROSOFT_IDENTITY_PLATFORM_TENANT_ID = '05f8c239-cb17-4755-a345-048752063c3b'
MICROSOFT_IDENTITY_PLATFORM_CLIENT_ID = '77ef1428-2bc3-4956-bfbf-25b628ef572f'
MICROSOFT_IDENTITY_PLATFORM_CLIENT_SECRET = os.getenv('MICROSOFT_IDENTITY_PLATFORM_CLIENT_SECRET')
# Initialize OAuth
oauth = OAuth(app)
oauth.register(
    name='MICROSOFT_IDENTITY_PLATFORM',  # Give a name to the OAuth provider
    client_id=MICROSOFT_IDENTITY_PLATFORM_CLIENT_ID,
    client_secret=MICROSOFT_IDENTITY_PLATFORM_CLIENT_SECRET,
    access_token_url='https://login.microsoftonline.com/'+MICROSOFT_IDENTITY_PLATFORM_TENANT_ID+'/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/'+MICROSOFT_IDENTITY_PLATFORM_TENANT_ID+'/oauth2/v2.0/authorize',
    api_base_url='https://graph.microsoft.com/v1.0/',
    client_kwargs={
        'scope': 'User.Read',  # Adjust scopes as needed
    },
)

# config_data
configuration = os.getenv('CONFIGURATION')
config_data.configuration = configuration

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/ms_sign_in', methods=['GET', 'POST'])
def initiate_microsoft_sign_in():
    logging.info("Starting MS login")
    session['redirect'] = "www.google.com"
    return oauth.MICROSOFT_IDENTITY_PLATFORM.authorize_redirect('http://localhost:5000/auth')

@app.route('/auth')
def authorize():
    logging.info(f"session test {session['redirect']}")
    token = oauth.MICROSOFT_IDENTITY_PLATFORM.authorize_access_token()
    user = oauth.MICROSOFT_IDENTITY_PLATFORM.get('me').json()
    session['user'] = user
    return f"Logged in as: {user} - {request.args.get('state')} {session['redirect']}"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)