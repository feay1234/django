import os.path
ROOT_PATH = os.path.dirname(__file__)
from django.http import HttpResponse
from django.core import serializers
from django.template import RequestContext, loader
from Lingo.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from mysite.settings import MEDIA_ROOT
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime
import time
import json
from django.db.models.fields.files import ImageFieldFile
from django.utils import simplejson
from django import shortcuts
from django.db.models import Q
from django.db.models import F
from django.db.models import Count

@login_required
def index(request):
    template = loader.get_template('linguo/index.html')
    user = User.objects.get(username = request.user)
    userProfile = UserProfile.objects.get(user = user)
    another_user = UserProfile.objects.exclude(user = user)
    invitation = FriendInvitation.objects.filter(receiver = userProfile)

    context = RequestContext(request,{'userProfile':userProfile, 'another_user':another_user, 'invitation':invitation})

    return HttpResponse(template.render(context))

def chat(request):
    template = loader.get_template('linguo/chat.html')
    user = User.objects.get(username = request.user)
    userProfile = UserProfile.objects.get(user = user)

    if request.method == 'GET' and 'talker' in request.GET:
      talker = request.GET['talker']
      talkerProfile = UserProfile.objects.get(name = talker)
      message = Message.objects.filter(Q(sender=userProfile, receiver=talkerProfile) | Q(receiver=userProfile, sender=talkerProfile)).order_by('datetime')
      message.update(notify = True) 
      context = RequestContext(request,{'userProfile':userProfile,'message':message,'talker':talker})
    else:
      context = RequestContext(request,{'userProfile':userProfile})
    return HttpResponse(template.render(context))

def add_profile(request):
    user = User.objects.get(username = request.user)
    userProfile = UserProfile.objects.get(user = user)
    mode = request.GET['mode']
    if mode == "add_language":
      try:
          language = Language.objects.get(name = request.GET['name'])
      except (Language.DoesNotExist):
          language = Language(name = request.GET['name'])
          language.save()
      userProfile.languages.add(language)

    elif mode == "add_interest":
      try:
          interest = Interest.objects.get(name = request.GET['name'])
      except (Interest.DoesNotExist):
          interest = Interest(name = request.GET['name'])
          interest.save()
      userProfile.interests.add(interest)

    elif mode == "remove_language":
      language = Language.objects.get(name = request.GET['name'])
      userProfile.languages.remove(language)

    elif mode == "remove_interest":
      interest = Interest.objects.get(name = request.GET['name'])
      userProfile.interests.remove(interest)
    

    return HttpResponse("yes")
    
def get_message(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver = UserProfile.objects.get(name = request.GET['receiver'])
    message = Message.objects.filter(Q(sender = sender, receiver = receiver) | Q(sender = receiver, receiver = sender)).order_by('datetime')
    if len(message) == 0:
        return HttpResponse("No")
    else:
        message.update(notify = True) 
        data = serializers.serialize('json', message, use_natural_keys=True)
        return HttpResponse(data, mimetype="application/json")    

def get_new_message(request):
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.user))
    patient = 0;
    while True:
        # check new message
        message = Message.objects.filter(receiver = receiver, notify = False)
        # patient <3 and sleep 5
        if( len(message)==0 and patient<3):
            time.sleep(5)
            patient+=1
        else:
            break 
    if len(message) > 0:
        data = serializers.serialize('json', message,use_natural_keys=True)
        message.update(notify = True) 
        return HttpResponse(data, mimetype="application/json")
    else:
      return HttpResponse("")

def chat_list(request):
    template = loader.get_template('linguo/chat_list.html')
    context = RequestContext(request,{})
    return HttpResponse(template.render(context))

def add_friend(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.GET['receiver']))
    FriendInvitation(sender = sender, receiver = receiver).save()
    return HttpResponse("yes")

def accept_request(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.GET['sender']))
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver.friends.add(sender)
    FriendInvitation.objects.filter(sender = sender, receiver = receiver).delete()
    return HttpResponse("accept_friend")

def delete_friendInvitation(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.GET['receiver']))
    FriendInvitation.objects.filter(sender = sender, receiver = receiver).delete()
    return HttpResponse("delete already")

def delete_friend(request):
    friend = request.GET['receiver']

    return HttpResponse("yes")



def send_message(request):
    sender = UserProfile.objects.get(user = User.objects.get(username = request.user))
    receiver = UserProfile.objects.get(user = User.objects.get(username = request.GET['receiver']))
    message = Message(sender = sender, receiver = receiver, text = request.GET['text'])
    message.save()
    messages = [message]
    data = serializers.serialize('json', messages,use_natural_keys=True)
    return HttpResponse(data, mimetype="application/json")

@login_required
def search(request):
    template = loader.get_template('linguo/search.html')

    user = User.objects.get(username = request.user)
    userProfile = UserProfile.objects.get(user = user)
    friends = userProfile.friends.values_list('id', flat=True)
    filter_language = []
    filter_interest = []

    if "language" in request.GET:
      filter_language = request.GET["language"].split(",")

    if "interest" in request.GET:
      filter_interest = request.GET["interest"].split(",")

    languages = userProfile.languages.exclude(name__in = filter_language).values_list('id', flat=True)  
    interests = userProfile.interests.exclude(name__in = filter_interest).values_list('id', flat=True)

    another_user = UserProfile.objects.exclude(id__in = friends).exclude(user = user).filter(Q(languages__in = languages) | Q(interests__in = interests)).distinct()

    invitation = FriendInvitation.objects.filter(Q(sender=userProfile) | Q(receiver=userProfile))
    
    context = RequestContext(request,{'userProfile':userProfile,'another_user':another_user, 'invitation':invitation})
    return HttpResponse(template.render(context))

@login_required
def edit_profile(request):
    template = loader.get_template('linguo/edit_profile.html')

    user = User.objects.get(username = request.user)
    userProfile = UserProfile.objects.get(user = user)
    
    friends = userProfile.friends.values_list('id', flat=True)
    another_user = UserProfile.objects.exclude(id__in = friends).exclude(user = user)
    invitation = FriendInvitation.objects.filter(Q(sender=userProfile) | Q(receiver=userProfile))
    
    context = RequestContext(request,{'another_user':another_user, 'invitation':invitation})
    return HttpResponse(template.render(context))



def get_chat(request):
  response_data = {}
  response_data['result'] = 'failed'
  response_data['message'] = 'You messed up'
  return HttpResponse(json.dumps(response_data), content_type="application/json")

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          print "dfd"
          if user is not None:
              if user.is_active:
                  login(request, user)

                  # Redirect to index page.
                  return HttpResponseRedirect("/linguo/")
                  # return render_to_response('restaurant/feed.html', {}, context)

		 # return render_to_response('restaurant/index.html', {}, context)
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print  "invalid login details " + username + " " + password
              return render_to_response('linguo/login.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('linguo/login.html', {}, context)

@login_required
def user_logout(request):
    context = RequestContext(request)
    logout(request)
    return HttpResponseRedirect('/linguo/')

def register(request):
    context = RequestContext(request)
    if request.method == 'POST':      
        uform = UserForm(data = request.POST)
        pform = UserProfileForm(request.POST,request.FILES)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            pw = user.password
            user.set_password(pw)
            user.save()
            profile = pform.save(commit = False)
            profile.user = user
            profile.save()

            
            return HttpResponseRedirect('/linguo/')
        else:
            return render_to_response('linguo/register.html', {'uform': uform,'pform':pform}, context)          
    else:
        uform = UserForm()
        pform = UserProfileForm()
        return render_to_response('linguo/register.html', {'uform': uform,'pform':pform}, context)

