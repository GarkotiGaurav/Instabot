#Import requests library to make network requests.
import requests,urllib,colorama
#We have imported color file to make our project look attractive.
from termcolor import *
#form file named keys we have to import access token
from keys import app_access_token
#Here base URL is the URL of instagram on which we have to work for.
BASE_URL = 'https://api.instagram.com/v1/'
colorama.init()

#Here we have made a function which will ask each time wether to continue or to quit.
def choice():
#we have used while condition for makin or condition true.
    while True:
        cprint('\nDo you want to continue or want to quit : ','blue')
        cprint('\nx.Continue : ', 'blue')
        cprint('\ny.Quite : ', 'blue')

        choice = raw_input("Enter your choice ")
        if choice == 'x':
            start_bot()
        elif choice == 'y':
            exit()
        else:
            cprint('wrong choice','red')


#Now our task is to declare a function for getting users information.
def self_info():
#Now here we are redirecting to instagarm account through access token.
  request_url = (BASE_URL + 'users/self/?access_token=%s') % (app_access_token)

  cprint ('GET request url : %s' % (request_url),'red')

  self_info = requests.get(request_url).json()


#Now we have used if else condition for checking wether the provided information is correct or not.
  if self_info['meta']['code'] == 200:
#here len keyword will check the length of provided data if correct will allow to proceed.
    if len(self_info['data']):

#Through this information about user will be provided.
      cprint('Username: %s' % (self_info['data']['username']),'green')
      cprint('No. of followers: %s' % (self_info['data']['counts']['followed_by']),'green')
      cprint('No. of people you are following: %s' % (self_info['data']['counts']['follows']),'green')
      cprint('No. of posts: %s' % (self_info['data']['counts']['media']),'green')
    else:
      print 'NO INFO'

  else:
    cprint('ERROR','red')
  choice()


#This function will get the user id which will help us in future.
def get_user_id(insta_user):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_user,app_access_token)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        cprint('ERROR','red')
        exit()
    choice()

def user_info(insta_user):
    user_id = get_user_id(insta_user)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, app_access_token)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        cprint('ERROR','red')
    choice()


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (app_access_token)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code']== 200:
        if len(own_media['data']):
            return own_media['data'][0]['id']
        else:
            print 'No Posts'
    else:
        cprint('ERROR','red')
    return None
    choice()


def get_user_post(insta_user):
    user_id = get_user_id(insta_user)
    if user_id == None:
        print 'User does not exist'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id,app_access_token)
    user_post = requests.get(request_url).json()
    if user_post['meta']['code'] == 200:
        if len(user_post['data']):
            return user_post['data'][0]['id']
        else:
            print 'No post'
    else:
        print 'Exit'
        exit()
    choice()


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (app_access_token)
    own_post = requests.get(request_url).json()
    if own_post['meta']['code'] == 200:
        if len(own_post['data']):
            image_name = own_post['data'][0]['id'] + '.jpeg'
            image_url = own_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Image has been successufully downloaded'
        else:
            print 'Post not exist'
    else:
        print 'Exit'
        exit()
    choice()

def get_user_post(insta_user):
    user_id = get_user_id(insta_user)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, app_access_token)

    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            print user_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'exit'
    choice()



def start_bot():
    while True:

        cprint('\nHey! Welcome to instaBot!','red')
        cprint('Here are your menu options:','red')
        cprint("a.Get your own details\n",'yellow')
        cprint("b.Get details of a user by username\n",'yellow')
        cprint("c.Get your own recent post\n",'yellow')
        cprint("d.Get the recent post of a user by username\n",'yellow')
        cprint("q.Exit",'yellow')

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username : ")
            user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username : ")
            get_user_post(insta_username)


        elif choice == "q":
            exit()
        else:
            print "wrong choice"
        choice()

start_bot()


