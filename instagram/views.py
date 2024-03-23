from django.shortcuts import render, HttpResponse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import pprint
from rest_framework.views import APIView
from django.http import JsonResponse

# Create your views here.
print("test")
def home(request):
    login_user_instance = loginuser()
    login_user_instance.login_user()
    return HttpResponse('soham is great')


# login user for insta
logger = logging.getLogger()
cl = Client()
class loginuser(APIView):
    def login_user():
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

class accountinsight(APIView):
    def accountinsights(request):
        try:
            print("in try")
            cl.insights_media_feed_all("ALL", "ONE_WEEK", "LIKE_COUNT")
            acc_details=cl.insights_account()
            pprint.pprint(acc_details)
        except:
            print("in except")
            login_user_instance = loginuser()
            login_user_instance.login_user()
            cl.insights_media_feed_all("ALL", "ONE_WEEK", "LIKE_COUNT")
            acc_details=cl.insights_account()
            pprint.pprint(acc_details)
        return JsonResponse({'accountinsights': acc_details})
    
class accountinfo(APIView):
    def accountinfo(request):
        try:
            account_info=cl.account_info()
        except:
            print("in except")
            login_user_instance = loginuser()
            login_user_instance.login_user()
            account_info=cl.account_info()
        return JsonResponse({'accountinfo': account_info})
    
class postinsight(APIView):
    def postinsight(request):
        try:
            account_info=cl.account_info()
        except:
            print("in except")
            login_user_instance = loginuser()
            login_user_instance.login_user()
            account_info=cl.account_info()
        return JsonResponse({'accountinfo': account_info})