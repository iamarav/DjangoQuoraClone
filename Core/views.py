from django.shortcuts import render, HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone

from .models import *

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  

from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

from Questions.models import *
import json

from django.template.defaulttags import register


# Define Global variables here
media_url = settings.MEDIA_URL
static = settings.STATIC_URL
site_info = settings.SITE_INFO
LOGIN_URL = settings.LOGIN_URL
LOGOUT_URL = settings.LOGOUT_URL


# Create your views here.
def HomePage(request):
    passing_dictionary = {
        'media_url': media_url,
        'home_page_title': 'DjQuora - A Quora Clone for Django Practice',
        'nav_title': 'DjQuora'
    }
    return render( request, 'core/home-page.html', passing_dictionary)

def LoginPage(request):
    passing_dictionary = {
        'media_url': media_url,
        'site_info': site_info,
    } 
    if request.user.id :
        # send user to dashboard if already logged in 
        return HttpResponseRedirect ('/dashboard')
    if 'successLogout' in request.session:
        # display message of successful logout if exists.
        passing_dictionary ['successLogout'] = 'You are logged out successfully!'
        del request.session['successLogout']
        request.session.modified = True
    if request.method == 'POST':
        # if form is submitted
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not "" and password is not "":
            # check credentials
            if '@' in username:
                # user is logging with email
                try:
                    user = User.objects.get(email = username)
                    if user.check_password(password):
                        # Password is correct and user is authenticated
                        print('Password is OK')
                    else:
                        user = None
                        # Password is wrong
                except User.DoesNotExist :
                    #User does not exist with the corresponding email
                    user = None
            else:
                # User is logging with username
                user = authenticate(username= username, password= password)
            if user is not None:
                # Login is success
                auth.login(request, user)
                passing_dictionary ['success'] = 'Woohoo! You are logged in to awesomeness.'
                return HttpResponseRedirect('/dashboard') 
                # return render( request, 'core/template-dashboard.html', passing_dictionary )
            else:
                # There is some error while logging in 
                passing_dictionary ['errors'] = 'Invalid Credentials buddy! Try again.' 
                return render( request, 'accounts/template-login.html', passing_dictionary )
        else:
            # Throw error of empty password
            passing_dictionary ['errors'] = 'Enter valid values.' 
            return render( request, 'accounts/template-login.html', passing_dictionary )
    else:
        return render( request, 'accounts/template-login.html', passing_dictionary )
        # to show the login page if there is no Form POSTED

def SignupPage(request):
    passing_dictionary = {
        'media_url': media_url,
        'site_info': site_info,
    }
    if request.user.id :
        # send user to dashboard if already logged in 
        return HttpResponseRedirect ('/dashboard')
    if request.method == 'POST':
        # if signup form is submitted
        email = request.POST.get('username')
        if '@' not in email:
            # User has entered invalid email. We can also use regex here.
            passing_dictionary ['errors'] = 'Enter a valid email.' 
            return render( request, 'accounts/template-signup.html', passing_dictionary)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        if password1 == password2:
            try:
                # Checking if the email entered is already existing in our DB.
                user = User.objects.get(email = email)
                passing_dictionary ['errors'] = 'Email already exists.' 
                return render( request, 'accounts/template-signup.html', passing_dictionary)
            except User.DoesNotExist :
                # The user does not exist.
                username = email.split('@', 1)[0] # just to remove the rest of the part after email
                try:
                    usernameExists = User.objects.get(username = username) # just to check if the username exists
                    username += str(1) # appending some additional text at the end
                except User.DoesNotExist :
                    username = username # No Change
                user = User.objects.create_user(email=email, username = username, first_name = fname, last_name = lname, password=password1)
#                auth.login(request,user) # This can be used to automatically login after successful signup.
                # Sign Up Success
                passing_dictionary ['success'] = 'Signup Success. Login to continue.' # Sending Signup Success Message.
                return render( request, 'accounts/template-login.html', passing_dictionary )
        else:
            # The Passwords entered are not identical.
            passing_dictionary ['errors'] = 'Passwords must match.' 
            return render( request, 'accounts/template-signup.html', passing_dictionary )
    else:
        # No POST request received.
        return render( request, 'accounts/template-signup.html', passing_dictionary )
        #to make a signup page

def ForgotPassword(request, action=None):
    passing_dictionary = {
        'media_url': media_url,
        'site_info': site_info,
    }
    if action == 'checkemail':
        return render( request, 'accounts/template-forgot-password-check-mail.html', passing_dictionary )
    if action == 'success':
        return render( request, 'accounts/template-forgot-password-reset-success.html', passing_dictionary )
    if action == 'new-password':
        user = None
        if request.method == 'POST':
            username = request.POST.get('username')
            token = request.POST.get('token')
            password1 = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password1 != password2:
                print (password1)
                print (password2)
                # the passwords entered are not same
                passing_dictionary ['errors'] = 'Passwords are not identical.'
            else:
                try:
                    if '@' in username:
                        # Email
                        user = User.objects.get(email = username)
                    else:
                        # username
                        user = User.objects.get(username = username)
                except User.DoesNotExist:
                    user = None
                    passing_dictionary ['errors'] = 'Invalid User'
                if user is not None:
                    # User exists.
                    try:
                        if '@' in username:
                            # Email
                            log = ForgotLog.objects.filter(username = user.email).order_by('-id')[:1][0]
                        else:
                            log = ForgotLog.objects.filter(username = user.username).order_by('-id')[:1][0]
                        # passing_dictionary['errors'] = log.date
                        if log.token != request.POST['token']:
                            passing_dictionary ['errors'] = 'Invalid Token!'
                        else:
                            log_date = log.date 
                            now = timezone.now()

                            if now-timedelta(hours=24) <= log_date <= now+timedelta(hours=24):
                                # the token generation date is in last 24 hours
                                print ('OK!')
                                user.set_password(password1)
                                user.save()
                                log.delete()
                                return HttpResponseRedirect ('/user/login')
                            else:
                                passing_dictionary ['errors'] = 'Invalid Token!'
                                print ('Entering a token which is generated before 24 hours!')
                    except ForgotLog.DoesNotExist:
                        # No token found
                        passing_dictionary['errors'] = 'Invalid Combination! Try again.'
        return render( request, 'accounts/template-forgot-password-create-new.html', passing_dictionary )
    
    if request.method == 'POST':
        username = request.POST.get('username')
        if username == '' or username is None:
            return HttpResponseRedirect ( '/user/forgot_password/' )
        token = get_random_string(length=32)
        the_data = ForgotLog (username=username, token=token)
        the_data.save()
        print ("username: "+str(username)+", token: "+str(token))
        return HttpResponseRedirect ( '/user/forgot_password/checkemail' )
    else:
        return render( request, 'accounts/template-forgot-password.html', passing_dictionary )


@login_required( login_url= LOGIN_URL)
def Logout(request):
    auth.logout(request) #logout the current user
    request.session['successLogout'] = 'You are now logged out successfully!' #logout message
    return HttpResponseRedirect( LOGIN_URL )

@login_required( login_url= LOGIN_URL )
def DashboardPage(request):
    passing_dictionary = {
        'media_url': media_url,
        'site_info': site_info,
    }
    if 'dashMessage' in request.session:
        # display message of successful logout if exists.
        passing_dictionary ['dashMessage'] = request.session['dashMessage']
        del request.session['dashMessage']
        request.session.modified = True

    questions_asked = Questions.objects.all().filter(author = request.user)

    question_answers_number = {}
    for question in questions_asked:

        answer_obj = Answers.objects.filter( question = question )
        ques_id = question.id
        question_answers_number[ ques_id ] = len(answer_obj)
    passing_dictionary ['question_answers_number'] = question_answers_number

    passing_dictionary['questions_asked'] = questions_asked
    return render( request, 'core/template-dashboard.html', passing_dictionary )


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def UserProfilePage(request, username):
    passing_dictionary = {
        'media_url': media_url,
    }
    user = User.objects.all().get(username = username)
    passing_dictionary ['user'] = user
    questions = Questions.objects.all().filter(author = user.id).exclude(anonymous = True)
    passing_dictionary ['questions_asked'] = questions
    passing_dictionary ['questions_asked_number'] = questions.count()
    passing_dictionary ['answers_answered'] = Answers.objects.all().filter(author = user.id).exclude(anonymous = True).count()

    return render( request, 'core/template-user-profile.html', passing_dictionary )
