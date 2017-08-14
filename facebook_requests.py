from flask import session
import requests
import pprint
import time
import datetime

class FacebookRequests(object):
    def __init__(self):
        self.access_token = session['access_token']
        self.host_url = "https://graph.facebook.com/v2.8"

    def retrieve_feed(self):
        current_date_parameters = time.strftime("%Y %m %d", time.localtime())
        (year, month, date) = current_date_parameters.split(" ")
        current_date = datetime.datetime(int(year), int(month), int(date))
        seconds_since_epoch = time.mktime(current_date.timetuple())
        feed_url = "{}/me/feed".format(self.host_url)
        feed_response = requests.get(feed_url, params={"access_token": self.access_token, "fields": "from", "since": seconds_since_epoch})
        print(feed_response.url)
        feed_json = feed_response.json()
        return feed_json['data']
    
    def post_comments(feed, comment):
        for post in feed:
            post_id = post['id']
            comments_url= "{}/{}/comments".format(self.host_url, post_id)
            requests.post(comments_url, params={"access_token": self.access_token, "message": comment})
        


