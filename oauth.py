from flask import session
import requests

class OAuth(object):
    def __init__(self, url_root):
        self.host = "https://www.facebook.com/v2.8"
        self.app_id = 1869692979931723
        self.redirect_uri = "{}authorized".format(url_root)
        self.facebook_url = "{}/dialog/oauth?client_id={}&redirect_uri={}".format(self.host, self.app_id, self.redirect_uri)
        self.client_secret = "353656cc7b5bfb1891b1921487a1bdc8"
        self.host_access_token = "https://graph.facebook.com/v2.8/oauth/access_token?client_id={}&redirect_uri={}&client_secret={}".format(self.app_id, self.redirect_uri, self.client_secret)        

    def retrieve_access_token(self, code):
        access_token_url = "{}&code={}".format(self.host_access_token, code)
        print(access_token_url)
        response = requests.get(access_token_url)
        response_json = response.json()
        print(response_json)
        if 'access_token' in response_json:
	    session['access_token'] = response_json['access_token']
        else:
            return "You must give the Birthday App permission in order to use it"

    
    
