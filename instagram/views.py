from django.shortcuts import render, HttpResponse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import pprint
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from .serializer import *
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
        print(request.body)
        try:
            media = cl.photo_upload(
           f"{request.FILES.get('file')}",
            f"{request.POST.get('caption')}",
            extra_data={
                "custom_accessibility_caption": "alt text example",
                # "like_and_view_counts_disabled": 1,
                # "disable_comments": 1,
            }
        )

        except:
            loginuser(request)
            media = cl.photo_upload(
           f"{request.FILES.get('file')}",
            f"{request.POST.get('caption')}",
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
        
        user_input = f""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        print("\nResponse from Assistance Bot:")
        print(response.text)
        return HttpResponse(response.text)


import nltk
from nltk.chat.util import Chat, reflections
# nltk.download('punkt')
pairs = [
    [
        r"hi|hey|hello",
        ["Hello", "Hi there", "Hello, how can I help you today?"]
    ],
    [
        r"what is your name ?",
        ["My name is Mental Health Bot, but you can call me MH Bot for short."]
    ],
    [
        r"how are you ?",
        ["I'm doing well, thank you for asking. How about you?", "I'm a machine learning model, so I don't have feelings as humans do. But I'm always here to help you."]
    ],
    [
        r"sorry (.*)",
        ["It's alright, no worries", "No problem at all."]
    ],
    [
        r"i'm (.*) doing good",
        ["That's great to hear! How can I help you today?"]
    ],
    [
        r"i am (.*)",
        ["That's interesting. Tell me more about yourself."]
    ],
    [
        r"can you help me (.*)",
        ["Of course! I'll do my best to assist you with whatever you need."]
    ],
    [
        r"(.*) thank you (.*)",
        ["You're welcome! I'm always here to help.", "No problem at all. It's what I'm here for."]
    ],
    [
        r"quit",
        ["Goodbye for now. Take care!"]
    ]
]
chatbot = Chat(pairs, reflections)

from textblob import TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score < -0.5:
        return "very negative"
    elif sentiment_score < 0:
        return "negative"
    elif sentiment_score == 0:
        return "neutral"
    elif sentiment_score <= 0.5:
        return "positive"
    else:
        return "very positive"
    
def get_response(input_text):
    sentiment = get_sentiment(input_text)
    if sentiment == "very negative":
        return "I'm sorry to hear that. but the comments on your channel is very negative so plz improve your content"
    elif sentiment == "negative":
        return "I'm sorry but the comments are negative"
    elif sentiment == "neutral":
        return "I'm here to listen.your chats are neutral?"
    elif sentiment == "positive":
        return "That's great to hear! Chats on your channels are postive ?"
    elif sentiment == "very positive":
        return "That's great to hear! Chats on your channels are very postive"


class PostQuery(APIView):
    
    def post(self, request):
        res=[]
        sent=[]
        data = request.data
        print("This is the data", data['query'])
        
        try:
            user_input = data['query']
            print('--->',user_input)
            for inp in user_input:
                if inp.lower() == 'quit':
                    print(chatbot.respond(inp))
                else:
                    response = get_response(inp)
                    sentiment = get_sentiment(response)
                    print(response)
                    res.append(response)
                    sent.append(sentiment)
                    print(f"Sentiment: {sentiment}")
                
            return JsonResponse({ 'sentiments':sent})
                
        except Exception as e:
            print("Error: ", str(e))
            return JsonResponse({"message": "Error occurred while processing the request."})
