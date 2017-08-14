from facebook_requests import FacebookRequests
import sys

def control():
    access_token = sys.argv[1]
    print (access_token)
    facebook = FacebookRequests(access_token)
    birthday_boy = facebook.retrieve_name()
    feed = facebook.retrieve_feed()
    facebook.post_comments(feed=feed, name=birthday_boy)

if __name__ == '__main__':
    control()
