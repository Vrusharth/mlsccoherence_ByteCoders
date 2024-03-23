from django.shortcuts import render, HttpResponse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import pprint
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from .serializer import *
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.
def home(request):
    login_user_instance = loginuser()
    login_user_instance.login_user()
    return HttpResponse('soham is great')


# login user for insta
logger = logging.getLogger()
cl = Client()
@csrf_exempt
def loginuser(request):    
    # data = json.loads(request.body.decode('utf-8'))
    username = "rm99877236"
    password = "Sharvesh@123"
    session = cl.load_settings("session.json")
    login_via_session = False
    login_via_pw = False


    if session:
        try:
            cl.set_settings(session)
            cl.login(username, password)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(username, password)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % username)
            if cl.login(username, password):
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
            print(acc_details)

            # Constructing the response dictionary
            acc_dict = {
                "status": acc_details.get("status"),
                "account_insights_unit": acc_details.get("account_insights_unit"),
                "followers_unit": acc_details.get("followers_unit"),
                "account_summary_unit": acc_details.get("account_summary_unit"),
                "top_posts_unit": acc_details.get("top_posts_unit"),
                "stories_unit": acc_details.get("stories_unit"),
                "promotions_unit": acc_details.get("promotions_unit"),
                "partner_top_posts_unit": acc_details.get("partner_top_posts_unit"),
                "partner_stories_unit": acc_details.get("partner_stories_unit")
                # Add more key-value pairs as needed
            }

            return JsonResponse({'accountinsights': acc_dict})
        except Exception as e:
            print("in except")
            loginuser(request)
            cl.insights_media_feed_all("ALL", "ONE_WEEK", "LIKE_COUNT")
            acc_details = cl.insights_account()
            print(acc_details)

            # Constructing the response dictionary
            acc_dict = {
                "status": acc_details.get("status"),
                "account_insights_unit": acc_details.get("account_insights_unit"),
                "followers_unit": acc_details.get("followers_unit"),
                "account_summary_unit": acc_details.get("account_summary_unit"),
                "top_posts_unit": acc_details.get("top_posts_unit"),
                "stories_unit": acc_details.get("stories_unit"),
                "promotions_unit": acc_details.get("promotions_unit"),
                "partner_top_posts_unit": acc_details.get("partner_top_posts_unit"),
                "partner_stories_unit": acc_details.get("partner_stories_unit")
                # Add more key-value pairs as needed
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
                    username =serializer.validated_data['username'],
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

def getuser(request, pk):
    if request.method == 'GET':
        try:
            thought_instance = Userprofile.objects.get(username=pk)
            serializer = UserprofileSerializer(thought_instance)
            return JsonResponse(serializer.data, safe=False)
        except Userprofile.DoesNotExist:
            return JsonResponse({'error': 'Thought not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



class postinfo(APIView):
    def get(self, request):
        loginuser(request)
        user_id = cl.user_id_from_username("rm99877236")
        posts = cl.user_medias(user_id)
        
        # Create a list to store post data
        posts_data = []
        
        # Iterate over posts and extract relevant data
        for post in posts:
            post_data = {
                "id": post.id,
                "caption": post.caption_text,
                "likes": post.like_count,
                "comments": post.comment_count,
                "type": post.media_type,
                "thumbnail_url": f"{post.thumbnail_url}",
                "share": f"{post.view_count}",
            }
            posts_data.append(post_data)

        # Return JSON response with posts data
        return JsonResponse({'posts': posts_data})

class suggestionbot(APIView):
    def get(self, request):
        genai.configure(api_key="AIzaSyAje4c-yOKwI8GcBgO0EdrnCx-uum0hW20")

        user_input = "what is full form of api"
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        print("\nResponse from Assistance Bot:")
        print(response.text)
        return HttpResponse(response.text)
