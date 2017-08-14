from flask import session
import requests
import pprint
import time
import datetime

class FacebookRequests(object):
    def __init__(self, access_token):
        self.access_token = access_token       
        self.host_url = "https://graph.facebook.com/v2.8"

    def retrieve_feed(self):
        current_date_parameters = time.strftime("%Y %m %d", time.localtime())
        (year, month, date) = current_date_parameters.split(" ")
        current_date = datetime.datetime(int(year), int(month), int(date))
        seconds_since_epoch = time.mktime(current_date.timetuple())
        feed_url = "{}/me/feed".format(self.host_url)
        feed_response = requests.get(feed_url, params={"access_token": self.access_token, "fields": "from", "since": seconds_since_epoch})
        feed_json = feed_response.json()
        pprint.pprint(feed_json)
        return feed_json['data']
    
    def post_comments(self, feed, name):
        for post in feed:
            pprint.pprint(post)
            id_post = post['id']
            creator_of_post = post['from']['name']
            comments_url= "{}/{}/comments".format(self.host_url, id_post)
            if creator_of_post != name:
                comment = "Thanks " + creator_of_post + "!"
                response =  requests.post(comments_url, params={"access_token": self.access_token, "message": comment})
                pprint.pprint(response.json())
        
    def retrieve_name(self):
        name_url = "{}/me".format(self.host_url)
        response = requests.get(name_url, params={"access_token": self.access_token})
        name = response.json()["name"]
        return name


