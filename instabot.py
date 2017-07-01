#Import requests library to make network requests.
import requests,urllib,colorama
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
#We have imported color file to make our project look attractive.
from termcolor import *
#form file named keys we have to import access token
from keys import app_access_token
#Here base URL is the URL of instagram on which we have to work for.
BASE_URL = 'https://api.instagram.com/v1/'
colorama.init()

#Access token for accessing perticular instagram account.
#This is my access token(Gaurav Garkoti)
app_access_token = '1776073792.0b7f1ea.2813a38481e84867be41ae4247bbd455'




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
        cprint('NO INFO','yellow')

  else:
    cprint('ERROR','red')
  choice()




#This function will get the user id which will help us in future.
def get_user_id(insta_username):

    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username,app_access_token)
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





#Now we are suppoose to fetch users information.
def user_info(insta_username):

#Here we are fectching information through users id.
    user_id = get_user_id(insta_username)

    if user_id == None:
#if user id does not match it will show user does not exixt.
        print 'User does not exist!'
        exit()

#this will will serch for user id from my access token.
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, app_access_token)
    user_info = requests.get(request_url).json()

#here if condition becomes equal to 200 will print details of the user.
    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
            cprint('User ID : %s ' % (user_id),'green')
            cprint('Username: %s' % (user_info['data']['username']),'green')
            cprint('No. of followers: %s' % (user_info['data']['counts']['followed_by']),'green')
            cprint('No. of people you are following: %s' % (user_info['data']['counts']['follows']),'green')
            cprint('No. of posts: %s' % (user_info['data']['counts']['media']),'green')

#otherwise proper message will be shown in screen.
        else:
            cprint('There is no data for this user!','yellow')

    else:
        cprint('ERROR','red')
    choice()




#function to save own posts.
def get_own_post():

#this will take or access token to fetch details.
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (app_access_token)
    own_post = requests.get(request_url).json()

    if own_post['meta']['code'] == 200:

        if len(own_post['data']):
#if condition will satesfied this will compare and save the respective post in jpeg formate.
            image_name = own_post['data'][0]['id'] + '.jpeg'
            image_url = own_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            cprint('Image has been successufully downloaded','green')

        else:
            cprint('Post not exist','yellow')

    else:
        cprint('ERROR','red')
        exit()
    choice()



#this will help in saving users post.
def get_user_post(insta_username):

    #firstly we have to take the users id so that we can fatch the data.
    media_id = get_user_id(insta_username)
#if media id does not match it will show respective message.

    if media_id ==  None:
        print 'media does not exist'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (media_id,app_access_token)
    user_post = requests.get(request_url).json()

    if user_post['meta']['code'] == 200:

        if len(user_post['data']):
            image_name = user_post['data'][0]['id'] + '.jpeg'
            image_url = user_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            cprint('Image has been successufully downloaded','yellow')

        else:
            cprint('Post not exist','yellow')

    else:
        cprint('Exit','red')
        exit()

    choice()




#post id for liking and to comment in others post.
def get_post_id(insta_username):

    #we are suppose to take user id first to fetch data.
    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id,app_access_token)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code']== 200:

        if len(own_media['data']):
            return own_media['data'][0]['id']

        else:
            cprint('No Posts','yellow')

    else:
        cprint('ERROR','red')
    return None





#function for liking others post.
def post_liked(insta_username):

    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": app_access_token}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'

    else:
        print 'Your like was unsuccessful. Try again!'

    choice()



def recently_liked_post():

    request_url = (BASE_URL + 'users/self/media/liked?access_token==%s') % (app_access_token)
    payload = {'access_token': app_access_token}
    recently_liked = requests.get(request_url, payload).json()

    if recently_liked ['meta']['code'] == 200:

        if len(recently_liked['data']):
#if condition will satesfied this will compare and save the respective post in jpeg formate.
            image_name = recently_liked['data'][0]['id'] + '.jpeg'
            image_url = recently_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Image has been successufully downloaded'

        else:
            print 'Post not exist'

    else:
        print 'Exit'
        exit()

    choice()




#function for commenting in a post.
def comment_a_post(insta_username):

#this will again take post id from user id.
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")

#payload for storing data.
    payload = {"access_token": app_access_token, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        cprint('Successfully commented!','yellow')

    else:
        cprint('ERROR','red')

    choice()



def dlt_negative_comment(insta_username):

    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, app_access_token)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:

        if len(comment_info['data']):
#Here's a naive implementation of how to delete the negative comments :)

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    cprint('Negative comment : %s' % (comment_text),'red')
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, app_access_token)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        cprint('Comment successfully deleted!\n','green')

                    else:
                        cprint('Unable to delete comment!','blue')

                else:
                    cprint('Positive comment : %s' % (comment_text),'yellow')

        else:
            cprint('There are no existing comments on the post!','yellow')

    else:
        cprint('ERROR!','red')

    choice()


def list_of_comment(insta_username):
    media_id = get_post_id(insta_username)
    if media_id == None:
        print 'user does not exist'
        exit()
    #payload = {"access_token": app_access_token}
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,app_access_token)

    comments_on_post = requests.get(request_url).json()

    if comments_on_post['meta']['code'] == 200:

        if len(comments_on_post['data']):
            for x in range(0, len(comments_on_post['data'])):
                #comment_id = liked_media['data'][x]['id']
                comment_text = comments_on_post['data'][x]['text']
                cprint('%s' % (comment_text),'green')

        else:
            cprint("No Comment",'yellow')

    else:
        cprint('ERROR','red')

    choice()




def list_of_likes(insta_username):
    media_id = get_post_id(insta_username)
    if media_id == None:
        print 'user does not exist'
        exit()

    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id,app_access_token)

    liked_media = requests.get(request_url).json()

    if liked_media['meta']['code'] == 200:

        if len(liked_media['data']):
            for x in range(0, len(liked_media['data'])):
                liked_post = liked_media['data'][x]['username']
                print '%s\n' % (liked_post)

        else:
            cprint("No likes", 'yellow')

    else:
        cprint('ERROR', 'red')

    choice()



#this is for showing list to user what he/she wants to do.
def start_bot():

    while True:

        cprint('\nHey! Welcome to instaBot!','blue')
        cprint('Here are your menu options:','blue')
        cprint("a.Get your own details",'yellow')
        cprint("b.Get details of a user by username",'yellow')
        cprint("c.Get your own recent post",'yellow')
        cprint("d.Get the recent post of a user",'yellow')
        cprint("e.Post liked",'yellow')
        cprint("f.Recently liked post by the user", 'yellow')
        cprint("g.List of likes on users post", 'yellow')
        cprint("h.Comment on users post",'yellow')
        cprint("i.List of comments on users post", 'yellow')
        cprint("j.Delete bad comments",'yellow')

        cprint("q.Exit",'yellow')

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()

        elif choice == "b":
            insta_username = raw_input("Enter username : ")
            user_info(insta_username)

        elif choice == "c":
            get_own_post()

        elif choice == "d":
            insta_username = raw_input("Enter username : ")
            get_user_post(insta_username)

        elif choice == "e":
            insta_username = raw_input("Enter username : ")
            post_liked(insta_username)

        elif choice == "f":
            recently_liked_post()

        elif choice == "g":
            insta_username = raw_input("Enter username : ")
            list_of_likes(insta_username)

        elif choice == "h":
            insta_username = raw_input("Enter username : ")
            comment_a_post(insta_username)

        elif choice == "i":
            insta_username = raw_input("Enter username : ")
            list_of_comment(insta_username)

        elif choice == "j":
            insta_username = raw_input("Enter username : ")
            dlt_negative_comment(insta_username)

        elif choice == "q":
            exit()

        else:
            cprint("wrong choice",'red')


start_bot()


