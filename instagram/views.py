from django.shortcuts import render, HttpResponse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import pprint
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from .serializer import *

# Create your views here.
def home(request):
    login_user_instance = loginuser()
    login_user_instance.login_user()
    return HttpResponse('soham is great')


# login user for insta
logger = logging.getLogger()
cl = Client()
import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def loginuser(request):    
    data = json.loads(request.body.decode('utf-8'))
    USERNAME = data.get('username')
    PASSWORD = data.get('password')
    request.session['USERNAME'] = USERNAME
    request.session['PASSWORD'] = PASSWORD
    # USERNAME='rm99877236'
    # PASSWORD='Sharvesh@123'


    print(request.session.get('USERNAME'))
    print(request.session.get('PASSWORD'))

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
            data = {
                "pk": account_info.pk,
                "username": account_info.username,
                "full_name": account_info.full_name,
                "is_private": account_info.is_private,
                "profile_pic_url": str(account_info.profile_pic_url),
                "is_verified": account_info.is_verified,
                "biography": account_info.biography,
                "external_url": account_info.external_url,
                "is_business": account_info.is_business,
                "birthday": account_info.birthday,
                "phone_number": account_info.phone_number,
                "gender": account_info.gender,
                "email": account_info.email
            }
            return JsonResponse({'data':data})
        except:
            print("in except")
            loginuser(request)
            account_info=cl.account_info()
            data = {
                "pk": account_info.pk,
                "username": account_info.username,
                "full_name": account_info.full_name,
                "is_private": account_info.is_private,
                "profile_pic_url": str(account_info.profile_pic_url),
                "is_verified": account_info.is_verified,
                "biography": account_info.biography,
                "external_url": account_info.external_url,
                "is_business": account_info.is_business,
                "birthday": account_info.birthday,
                "phone_number": account_info.phone_number,
                "gender": account_info.gender,
                "email": account_info.email
            }
            return JsonResponse({'data':data})


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

from django.http import JsonResponse
from rest_framework.views import APIView
# from your_app_name.views import loginuser  # Import the loginuser view


class getcommentsonpost(APIView):
    def get(self, request):
        try:
            user_id = cl.user_id
            media_id = cl.user_medias(user_id)
            lis = []

            for i in media_id:
                media_pk = cl.media_id(i.pk)
                comments = cl.media_comments(media_pk)
                
                # Convert Comment objects to dictionaries
                comments_data = []
                for comment in comments:
                    comment_data = {
                        "pk": comment.pk,
                        "text": comment.text,
                        "user": {
                            "pk": comment.user.pk,
                            "username": comment.user.username,
                            "full_name": comment.user.full_name,
                            # Add more user attributes if needed
                        },
                        "created_at_utc": comment.created_at_utc.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string
                        "content_type": comment.content_type,
                        "status": comment.status,
                        "has_liked": comment.has_liked,
                        "like_count": comment.like_count
                    }
                    comments_data.append(comment_data)
                
                lis.append(comments_data)
            
            return JsonResponse({'comments_on_posts': lis})
        
        except Exception as e:
            print("Exception:", e)
            loginuser(request)
            user_id = cl.user_id
            media_id = cl.user_medias(user_id)
            lis = []

            for i in media_id:
                media_pk = cl.media_id(i.pk)
                comments = cl.media_comments(media_pk)
                
                # Convert Comment objects to dictionaries
                comments_data = []
                for comment in comments:
                    comment_data = {
                        "pk": comment.pk,
                        "text": comment.text,
                        "user": {
                            "pk": comment.user.pk,
                            "username": comment.user.username,
                            "full_name": comment.user.full_name,
                            # Add more user attributes if needed
                        },
                        "created_at_utc": comment.created_at_utc.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string
                        "content_type": comment.content_type,
                        "status": comment.status,
                        "has_liked": comment.has_liked,
                        "like_count": comment.like_count
                    }
                    comments_data.append(comment_data)
                
                lis.append(comments_data)
            
            return JsonResponse({'comments_on_posts': lis})

class createprofile(APIView):
    def post(self, request):
        sr_data = request.data
        user = request.user

        serializer = UserprofileSerializer(data=sr_data)

        if serializer.is_valid():
            try:
                thought = Userprofile.objects.create(
                    businessCartegory =serializer.validated_data['businessCartegory'],
                    businessBio =serializer.validated_data['businessBio'],
                    businessObjective =serializer.validated_data['businessObjective'],
                    businessGoal =serializer.validated_data['businessGoal'],
                    location =serializer.validated_data['location']
                )
                thought.save()

                new_response = UserprofileSerializer(thought)

                return Response({
                    "status": 200,
                    "message": "Thought created",
                    "thought": new_response.data
                })
            except Exception as e:
                return Response({
                    "status": 400,
                    "error": f"{e}"
                })
        else:
            return Response({
                "status": 400,
                "error": serializer.errors
            })
        