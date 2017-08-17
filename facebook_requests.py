import requests
import pprint
import time
import datetime

class FacebookRequests(object):
    def __init__(self, access_token):
        self.access_token = access_token       
        self.host_url = "https://graph.facebook.com/v2.8"

    def retrieve_feed(self):
        """This method essentially finds out the current date and the time in seconds since epoch till that
        date. It then queries the user's facebook feed with this data, and also retrieves who each wallpost
        is from.
        
        Returns:
            feed_json ['data'] (list): A list of dictionaries, with each dictionary being a post on the user's wall
        """
        current_date_parameters = time.strftime("%Y %m %d", time.localtime())
        (year, month, date) = current_date_parameters.split(" ")
        current_date = datetime.datetime(int(year), int(month), int(date))
        seconds_since_epoch = time.mktime(current_date.timetuple())
        feed_url = "{}/me/feed".format(self.host_url)
        feed_response = requests.get(feed_url, params={"access_token": self.access_token, "fields": "from", "since": seconds_since_epoch})
        feed_json = feed_response.json()
        return feed_json['data']
    
    def post_comments(self, feed, birthday_boy_or_girl):
        """This method iterates through each post in the feed, checks if the creator of each post is the 
        currently logged in user (ignores this json if it is), and then posts a Thank you message to the 
        wall post with the users name
        
        Args:
            feed (list): A list of dictionaries, with each dictionary being a post on the user's wall
            birthday_boy_or_girl (dict): The name and the id of the current user
        """
        for post in feed:
            name = birthday_boy_or_girl['name']
            id = birthday_boy_or_girl['id']
            pprint.pprint(post)
            id_post = post['id']
            creator_of_post = post['from']['id']
            comments_url= "{}/{}/comments".format(self.host_url, id_post)
            if creator_of_post != id:
                comment = "Thanks " + post['from']['name'] + "!"
                response =  requests.post(comments_url, params={"access_token": self.access_token, "message": comment})
                pprint.pprint(response.json())
        
    def retrieve_birthday_boy_or_girl(self):
        """Retrieve the id and the name of the user with the access_token. I guess you can say this could be 
        either a birthday boy or a birthday girl
       
        Return:
            birthday_boy_or_girl (dict): The name and the id of the user with the access token
        """
        name_url = "{}/me".format(self.host_url)
        response = requests.get(name_url, params={"access_token": self.access_token})
        birthday_boy_or_girl = response.json()
        return birthday_boy_or_girl

