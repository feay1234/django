import os.path
ROOT_PATH = os.path.dirname(__file__)
from django.http import HttpResponse
from django.utils import simplejson
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
    print request.user
    userProfile = UserProfile.objects.get(user = user)
    context = RequestContext(request,{'userProfile':userProfile})
    return HttpResponse(template.render(context))

def chat_list(request):
    template = loader.get_template('linguo/chat_list.html')
    context = RequestContext(request,{})
    return HttpResponse(template.render(context))

def profile(request):
    template = loader.get_template('linguo/friend.html')
    context = RequestContext(request,{})
    return HttpResponse(template.render(context))

def chat(request):
    template = loader.get_template('linguo/chat.html')
    context = RequestContext(request,{})
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

