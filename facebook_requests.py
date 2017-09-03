import requests
import pprint
import time
import logging
import datetime
from exceptions import EmptyFeedException, RequestException


class FacebookRequests(object):
    def __init__(self, access_token):
        logging.basicConfig(level=logging.INFO)
        self.access_token = access_token       
        self.host_url = "https://graph.facebook.com/v2.8"

    def retrieve_feed(self):
        """This method essentially finds out the current date and the time in seconds since epoch till that
        date. It then queries the user's facebook feed with this data, and also retrieves who each wallpost
        is from.
        
        Returns:
            feed_json (dict): A dictionary containing the feed
        """
        gm_date_parameters = time.strftime("%Y %m %d", time.gmtime())
        local_time_parameters = time.strftime("%Y %m %d", time.localtime())
        (local_year, local_month, local_date) = local_time_parameters.split(" ")
        current_date = datetime.datetime(int(local_year), int(local_month), int(local_date))
        seconds_since_epoch = time.mktime(current_date.timetuple())
        feed_url = "{}/me/feed".format(self.host_url)
        feed_response = requests.get(feed_url, params={"access_token": self.access_token, "fields": "from", "since": seconds_since_epoch})
        self.check_response(feed_response)
        feed_json = feed_response.json()
        return feed_json
    
    def check_response(self, response):
        """This method essentially checks if the response returned from a request to the FB graph api
        is a 200 or not. If it isnt an exception is raised

        Raises:
            RequestException (Exception): An exception that is raised when a request was not made to the FB graph api properly
        """
        if not response.ok:
            logging.info("Something went wrong while making a request to FB Graph API %s", response.json())
            raise RequestException("Request was not made to the facebook graph api")

    def post_comments(self, feed, birthday_boy_or_girl):
        """This method iterates through each post in the feed, checks if the creator of each post is the 
        currently logged in user (ignores this json if it is), and then posts a Thank you message to the 
        wall post with the users name
        
        Args:
            feed (list): A list of dictionaries, with each dictionary being a post on the user's wall
            birthday_boy_or_girl (dict): The name and the id of the current user

        Raises:
            EmptyFeedException(Exception): An exception that is raised when the feed recieved is empty
        """
        if feed['data'] == []:
            raise EmptyFeedException(message="Empty Feed")
        current_page = True
        while (current_page):
            if feed['data']:
                for post in feed['data']:
                    logging.info("POST IS ", post)
                    name = birthday_boy_or_girl['name']
                    id = birthday_boy_or_girl['id']
                    id_post = post['id']
                    creator_of_post = post['from']['id']
                    comments_url= "{}/{}/comments".format(self.host_url, id_post)
                    if creator_of_post != id:
                        comment = "Thanks " + post['from']['name'] + "!"
                        response =  requests.post(comments_url, params={"access_token": self.access_token, "message": comment})
                        self.check_response(response)
                if 'paging' in feed and 'next' in feed['paging']:
                    feed_request = requests.get(feed['paging']['next'])
                    self.check_response(feed_request)
                    feed = feed_request.json()
                    current_page = True
                else:
                    current_page = False
            else:
                current_page = False

    def retrieve_birthday_boy_or_girl(self):
        """Retrieve the id and the name of the user with the access_token. I guess you can say this could be 
        either a birthday boy or a birthday girl

        Returns:
            birthday_boy_or_girl (dict): The name and the id of the user with the access token
        """
        name_url = "{}/me".format(self.host_url)
        response = requests.get(name_url, params={"access_token": self.access_token})
        self.check_response(response)
        birthday_boy_or_girl = response.json()
        logging.info("USER INFO IS %s", birthday_boy_or_girl)
        return birthday_boy_or_girl

