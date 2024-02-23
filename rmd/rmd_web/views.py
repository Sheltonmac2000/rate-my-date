from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
# Authentication models and functions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from fire.fireconfig import Firebase
from .models import Person,Post, Comment
from .forms import PostForm, CreateUserForm, LoginForm, PersonForm

# time
from datetime import datetime
from django.utils import timezone
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)
# Create your views here.

def home(request):
    context = {
        'user': request.user  # Pass the user object to the context
    }
    return render(request, 'home.html', context=context)

def comment(request):
    # Your logic here
    pass

def createNewPerson(request):
    context = {
        'user': request.user  # Pass the user object to the context
    }
    return render(request, 'createnewperson.html', context=context)

def view_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    posts = person.post_set.all()  # Retrieve posts associated with the person
    print('post: ', posts)  # Print posts to verify they are retrieved correctly
    
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.person = person
            post.user = request.user
            post.save()
            messages.success(request, 'Post submitted successfully.')
            return redirect('view_person', person_id=person_id)
        else:
            messages.error(request, 'Failed to submit post. Please check the form.')
    else:
        post_form = PostForm()
        
    context = {
        'user': request.user,
        'person': person,
        'post_form': post_form,
        
    }
    return render(request, 'view_person.html', context=context)
# def view_person(request, person_id):
#     person = get_object_or_404(Person, pk=person_id)
    
#     if request.method == 'POST':
#         post_form = PostForm(request.POST)
#         if post_form.is_valid():
#             post = post_form.save(commit=False)
#             post.person = person
#             post.user = request.user
#             post.save()
#             return redirect('view_person', person_id=person_id)
#     else:
#         post_form = PostForm()
        
#     context = {
#         'user': request.user,
#         'person': person,
#         'post_form': post_form,
#     }
#     return render(request, 'view_person.html', context=context)
  
def searchPerson(request):
    context = {
        'user': request.user  # Pass the user object to the context
    }
    return render(request, 'searchpage.html', context=context)

def explore(request):
    persons = Person.objects.all().values()
    context = {
        'user': request.user,  # Pass the user object to the context
        'persons': persons,
    }
    return render(request, 'explore.html', context=context)

# CREATE A PERSON
@login_required
def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.user = request.user
            
            # Set joined_date to the current date
            current_date = timezone.now().strftime('%Y-%m-%d')
            print("Current Date:", current_date)  # Debugging information
            person.joined_date = current_date
            
            person.save()
            print("Person created successfully")  # Success debug message
            return redirect('viewperson', person_id=person.id)
        else:
            print("Form is invalid")  # Invalid form debug message
            print(form.errors)  # Print form errors for debugging
    else:
        form = PersonForm()
    
    return render(request, 'create_person.html', {'form': form, 'current_date': timezone.now().strftime('%Y-%m-%d')})
  
# CREATE A REVIEW
@login_required
def create_post(request, person_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Create a new post instance but don't save it yet
            post = form.save(commit=False)
            # Assign the user and person IDs to the post instance
            post.user_id = request.user.id
            post.person_id = person_id
            # Now save the post instance
            post.save()
            return redirect('view_person', person_id=person_id)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def agree_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.agree += 1
    comment.save()
    return redirect('post_detail', post_id=comment.post_id)

# AUTHENTICATION

def register(request):
    
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            print("Register was Successful")
            return redirect("my-login")
    
    context ={ 'registerform': form}
    
    return render(request, 'signup.html', context = context)

def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                print("User logged in successfully:", user)  # Add this line for debugging
                return redirect("/")
            else:
                print("Failed to authenticate user")

    context = {'loginform': form, 'user': request.user}
    return render(request, 'login.html', context=context)


# def my_login(request):
#     form = LoginForm()
#     if request.method == "POST":
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
            
#             user = authenticate(request, username=username,password=password)
            
#             if user is not None:
#                 # auth.login(request,user)
#                 auth_login(request,user)
#                 return redirect('/')

#     context ={ 'loginform': form}
    
#     return render(request, 'login.html', context=context)

def user_logout(request) :
    #  auth.logout(request)
    auth_logout(request)  
    return redirect('/')
    

@login_required(login_url="my-login")
def dashboard(request):
    return render(request, 'createnewperson.html')
