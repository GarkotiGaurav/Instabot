#Import requests library to make network requests.
import requests,urllib,colorama
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
#We have imported color file to make our project look attractive.
from termcolor import *
#form file named keys we have to import access token
from keys import app_access_token
#library for making word cloud.
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
#Here base URL is the URL of instagram on which we have to work for.
BASE_URL = 'https://api.instagram.com/v1/'
colorama.init()

#Access token for accessing perticular instagram account.
#This is my access token(Gaurav Garkoti)
app_access_token = '1776073792.0b7f1ea.2813a38481e84867be41ae4247bbd455'
#username for this token = g_garkoti , apoorav613.




#Here we have made a function which will ask each time wether to continue or to quit.
def choice():

#we have used while condition for makin or condition true.
    while True:

        cprint('\nDo you want to continue or want to quit : ','blue')
        cprint('\nx.Continue : ', 'blue')
        cprint('\ny.Quite : ', 'blue')
#here user have to give input for further process.
        choice = raw_input("Enter your choice ")
        if choice == 'x':
#if user presses x then it will took us to start_bot function.
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
#if condition does not satesfied then it will have to show some meaningfull message.
    else:
        cprint('NO INFO','yellow')

  else:
    cprint('ERROR','red')
#this will call us choice function.
  choice()





#This function will get the user id which will help us in future.
def get_user_id(insta_username):

#redirect to given url and will take provided username and provided access token.
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username,app_access_token)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if len(user_info['data']):
#if condition becomes true then it will take id for respective user.
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
#if given condition become true then it will return post id.
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
#payload is used for storing data.
    payload = {"access_token": app_access_token}
#here we have to use post request for storing like which we have liked.
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()

    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'

    else:
        print 'Your like was unsuccessful. Try again!'

    choice()




#function for downloading recently liked post by the user.
def recently_liked_post():
#this url will took url for liked media.
    request_url = (BASE_URL + 'users/self/media/liked?access_token==%s') % (app_access_token)
    payload = {'access_token': app_access_token}
    recently_liked = requests.get(request_url,payload).json()

    if recently_liked ['meta']['code'] == 200:

        if len(recently_liked['data']):
#if condition will satesfied this will compare and save the respective post in jpeg formate.
            image_name = recently_liked['data'][0]['id'] + '.jpeg'
            image_url = recently_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            cprint('Image has been successufully downloaded','green')

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





#now we are supposed to delete bad comments from users post.
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

#this is used for analyzing the text.
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
#this will compare wether the text is positive or negative.
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    cprint('Negative comment : %s' % (comment_text),'red')
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, app_access_token)
#delete request for deleting bad comments.
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





#function for getting list of comments on a post
def list_of_comment(insta_username):
    media_id = get_post_id(insta_username)
    if media_id == None:
        print 'user does not exist'
        exit()

    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id,app_access_token)

    comments_on_post = requests.get(request_url).json()

    if comments_on_post['meta']['code'] == 200:

        if len(comments_on_post['data']):
            for x in range(0, len(comments_on_post['data'])):

                comment_text = comments_on_post['data'][x]['text']
                cprint('%s' % (comment_text),'green')

        else:
            cprint("No Comment",'yellow')

    else:
        cprint('ERROR','red')

    choice()





#function for getting list of like on any post
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





#function for downloading media of your own choice.
def media_of_own_choice(insta_username):
#this will take user id for fetching information.
    media_id = get_user_id(insta_username)

    if media_id == None:
        print 'user does not exist'

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (media_id, app_access_token)
    user_post = requests.get(request_url).json()

    if user_post['meta']['code'] == 200:

        if len(user_post['data']):

#now we are suppose to ask which post u wants to download
            number = raw_input("Which post do you want to download : ")


            number = int(number)

            post = number - 1

            image_name = user_post['data'][post]['id'] + '.jpeg'
            image_url = user_post['data'][post]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)

            cprint('Image has been successfully downloaded!','green')

        else:
            cprint('Post does not exist','yellow')

    else:
        cprint('ERROR','red')

    choice()





#function for finding sub trends.
def sub_trend():

#dictionary for storing hastags.
    hash_dict = {}

#taking input for whic u wants to find subtrends
    tag = raw_input("enter trend for which you wants to find subtrend : ")
    request_url = (BASE_URL + 'tags/%s/media/recent?access_token=%s') % (tag, app_access_token)
    media_tag = requests.get(request_url).json()

    if media_tag['meta']['code'] == 200:

        if media_tag['data']:

            for x in range(0, len(media_tag['data'])):
                tags = media_tag['data'][x]['tags']
                # print tags


                for y in range(0, len(tags)):

#if tag is present this condition will add on.
                    if media_tag['data'][x]['tags'][y] in hash_dict:
                        hash_dict[media_tag['data'][x]['tags'][y]] += 1

                    else:
                        hash_dict[media_tag['data'][x]['tags'][y]] = 1



        else:
            print'post not exist'

    else:
        print 'ERROR'

#pop is used for deleting trends as we only wants subtrends.
    hash_dict.pop(tag.lower(), None)
    print hash_dict
#for making word cloud for our subtrends.
    wordcloud = WordCloud().generate_from_frequencies(hash_dict)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()

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
        cprint("e.Get post of your own choice", 'yellow')
        cprint("f.Post liked",'yellow')
        cprint("g.Recently liked post by the user", 'yellow')
        cprint("h.List of likes on users post", 'yellow')
        cprint("i.Comment on users post",'yellow')
        cprint("j.List of comments on users post", 'yellow')
        cprint("k.Delete bad comments",'yellow')
        cprint("l.Finding sub trends for any event", 'yellow')
        cprint("q.Exit",'yellow')


        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()


        elif choice == "b":
            insta_username = raw_input("Enter username : ")
            if not re.match("[a-z0-9_]*$", insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                user_info(insta_username)


        elif choice == "c":
            get_own_post()

        elif choice == "d":
            insta_username = raw_input("Enter username : ")
            if not re.match('[a-z0-9_]*$', insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                get_user_post(insta_username)


        elif choice == "e":
            insta_username = raw_input("Enter username : ")
            if not re.match("[a-z0-9_]*$", insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                media_of_own_choice(insta_username)


        elif choice == "f":
            insta_username = raw_input("Enter username : ")
            if not re.match("[a-z0-9_]*$", insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                post_liked(insta_username)


        elif choice == "g":
            recently_liked_post()


        elif choice == "h":
            insta_username = raw_input("Enter username : ")
            if not re.match("[a-z0-9_]*$", insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                list_of_likes(insta_username)


        elif choice == "i":
            insta_username = raw_input("Enter username : ")
            if not re.match('[a-z0-9_]*$', insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters!", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                comment_a_post(insta_username)


        elif choice == "j":
            insta_username = raw_input("Enter username : ")
            if not re.match("[a-z0-9_]*$", insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                list_of_comment(insta_username)


        elif choice == "k":
            insta_username = raw_input("Enter username : ")
            if not re.match("[a-z0-9_]*$", insta_username):
                cprint("ERROR!Please enter a valid name less then 15 characters", 'red')

            elif len(insta_username) > 15:
                cprint('ERROR!Please enter a valid name less then 15 characters''red')

            else:
                dlt_negative_comment(insta_username)


        elif choice == "l":
            sub_trend()


        elif choice == "q":
            exit()


        else:
            cprint("wrong choice",'red')

#called function which will aks what you want to do.
start_bot()


