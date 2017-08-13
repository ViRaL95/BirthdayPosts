from flask import session
import requests

class FacebookRequests(object):
    def __init__(self):
        self.access_token = session['access_token']
        self.host_url = "https://graph.facebook.com/v2.8"

    def retrieve_feed(self):
        feed_id = "{}/me".format(self.host_url)
        feed_id_response = requests.get(feed_id, params={"access_token": self.access_token}).json()
        print(feed_id_response)
        feed_url = "{}/me/feed".format(self.host_url)
        feed_response = requests.get(feed_url, params={"access_token": self.access_token})
        feed_json = feed_response.json()
        return feed_json['data']
    
    def post_comments(feed, comment):
        for post in feed:
            post_id = post['id']
            comments_url= "{}/{}/comments".format(self.host_url, post_id)
            requests.post(comments_url, params={"access_token": self.access_token, "message": comment})
        


