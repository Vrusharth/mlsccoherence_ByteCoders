from django.shortcuts import render, HttpResponse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import pprint
from rest_framework.views import APIView
from django.http import JsonResponse

# Create your views here.
def home(request):
    login_user_instance = loginuser()
    login_user_instance.login_user()
    return HttpResponse('soham is great')


# login user for insta
logger = logging.getLogger()
cl = Client()
def loginuser(request):    
    USERNAME='rm99877236'
    PASSWORD='Sharvesh@123'
    session = cl.load_settings("session.json")
    login_via_session = False
    login_via_pw = False


    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    # return JsonResponse({'loggedin successfully!!!'})
    return HttpResponse("loggedin successfully")

    
class accountinsight(APIView):
    def get(self, request):
        try:
            print("in try")
            cl.insights_media_feed_all("ALL", "ONE_WEEK", "LIKE_COUNT")
            acc_details = cl.insights_account()

            # Convert Account object to dictionary
            acc_dict = {
                "attribute1": acc_details.attribute1,
                "attribute2": acc_details.attribute2,
                # Add more attributes as needed
            }

            return JsonResponse({'accountinsights': acc_dict})
        except Exception as e:
            print("in except")
            loginuser(request)
            cl.insights_media_feed_all("ALL", "ONE_WEEK", "LIKE_COUNT")
            acc_details = cl.insights_account()

            # Convert Account object to dictionary
            acc_dict = {
                "attribute1": acc_details.attribute1,
                "attribute2": acc_details.attribute2,
                # Add more attributes as needed
            }

            return JsonResponse({'accountinsights': acc_dict})

    
class accountinfo(APIView):
    def get(self, request):
        try:
            account_info=cl.account_info()
        except:
            print("in except")
            loginuser(request)
            account_info=cl.account_info()
        print(account_info)
        return JsonResponse({'accountinfo': account_info})
    
class postinsight(APIView):
    def get(self, request):
        lis = []
        try:
            user_id =cl.user_id
            media_id=cl.user_medias(user_id)
            for i in media_id:
                media_id = cl.media_id(i.pk)
                lis.append(cl.insights_media(media_id))
        except:
            print("in except")
            loginuser(request)
            user_id =cl.user_id
            media_id=cl.user_medias(user_id)
            for i in media_id:
                media_id = cl.media_id(i.pk)
                lis.append(cl.insights_media(media_id))
        return JsonResponse({'postinsight': lis})
    

class addpost(APIView):
    def post(self, request):
        try:
            media = cl.photo_upload(
            "lizard.jpeg",
            "How does Lizard Lives #csk #hashtags #animals #life#insect and mention users such @Ddas_2707",
            extra_data={
                "custom_accessibility_caption": "alt text example",
                # "like_and_view_counts_disabled": 1,
                # "disable_comments": 1,
            }
        )

        except:
            loginuser(request)
            media = cl.photo_upload(
            "lizard.jpeg",
            "How does Lizard Lives #csk #hashtags #animals #life#insect and mention users such @Ddas_2707",
            extra_data={
                "custom_accessibility_caption": "alt text example",
                # "like_and_view_counts_disabled": 1,
                # "disable_comments": 1,
            }
        )


        return JsonResponse({'response':media})


class getcommentsonpost(APIView):
    def get(self, request):
        lis = []
        try:
            user_id =cl.user_id
            media_id=cl.user_medias(user_id)
            for i in media_id:
                media_pk = cl.media_id(i.pk)
                comments = cl.media_comments(media_pk)
                print('----->',comments)
                lis.append(comments)
        except:
            loginuser(request)
            user_id =cl.user_id
            media_id=cl.user_medias(user_id)
            for i in media_id:
                media_pk = cl.media_id(i.pk)
                comments = cl.media_comments(media_pk)
                print('----->',comments)
                lis.append(comments)
        return JsonResponse({'comments on posts': lis})