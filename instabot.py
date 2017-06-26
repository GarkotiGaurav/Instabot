#Import requests library to make network requests.
import requests
#form file named keys we have to import access token
from keys import app_access_token
#Here base URL is the URL of instagram on which we have to work for.
BASE_URL = 'https://api.instagram.com/v1/'

#Now our task is to declare a function for getting users information.
def self_info():
#Now here we are redirecting to instagarm account through access token.
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (app_access_token)

  print 'GET request url : %s' % (request_url)

  user_info = requests.get(request_url).json()


#Now we have used if else condition for checking wether the provided information is correct or not.
  if user_info['meta']['code'] == 200:
#here len keyword will check the length of provided data if correct will allow to proceed.
    if len(user_info['data']):

#Through this information about user will be provided.
      print 'Username: %s' % (user_info['data']['username'])
      print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
      print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
      print 'No. of posts: %s' % (user_info['data']['counts']['media'])
    else:
      print 'User does not exist!'

  else:
    print 'Exit'

#Here we have called the function.
self_info()