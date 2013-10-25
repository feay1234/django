from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
from django.db.models import Count

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),

)
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=GENDER)
    datetime = models.DateTimeField(default=datetime.now, editable=False)
    friends = models.ManyToManyField("self", related_name="friends")
    def __unicode__(self):
            return self.user.username
class Message(models.Model):
	sender = models.ForeignKey(UserProfile,related_name='senderM')
	receiver = models.ForeignKey(UserProfile, related_name='receiverM')
	text = models.CharField(max_length=128)
	datetime = models.DateTimeField(default=datetime.now, editable=False)
	read = models.BooleanField(default=False)
	notify = models.BooleanField(default=False)
	def __unicode__(self):
            return self.sender.user.username

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':"Username"}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Password"}))
	class Meta:
		model = User
		fields = ["username","password"]

class UserProfileForm(forms.ModelForm):
	name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':"Name"}))
	gender = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=GENDER)
	class Meta:
		model = UserProfile
		fields = [ 'name','gender',]