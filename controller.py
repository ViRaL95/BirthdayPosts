from facebook_requests import FacebookRequests
import sys

def control():
    access_token = sys.argv[1]
    print (access_token)
    facebook = FacebookRequests(access_token)
    birthday_boy_or_girl = facebook.retrieve_birthday_boy_or_girl()
    feed = facebook.retrieve_feed()
    facebook.post_comments(feed=feed, birthday_boy_or_girl=birthday_boy_or_girl)

if __name__ == '__main__':
    control()
