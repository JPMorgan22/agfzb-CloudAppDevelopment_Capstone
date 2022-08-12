from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import getDealershipByState, getAllDealerships, getReviewByDealership, addReviewToCloudant
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('/djangoapp/')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('/djangoapp/')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    if request.method == "POST":
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("/djangoapp/")
        else:
            return render(request, 'djangoapp/signup.html', context)

    elif request.method == "GET":
        return render(request, 'djangoapp/signup.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    dealerships = []
    if request.method == "GET" and 'state' in request.GET:
        context = getDealershipByState(request.GET['state'])
        for dealer in context['dealerships']:
            if 'short_name' in vars(dealer):
                dealerships.append(vars(dealer))
        context = {"dealerships":dealerships}
        return render(request, 'djangoapp/index.html', context)
    else:
        url = "https://jpmorganjere-8000.us-east.mybluemix.net/djangoapp/dealership"
        context = getAllDealerships()
        for dealer in context['dealerships']:
            if 'short_name' in vars(dealer):
                dealerships.append(vars(dealer))
        context = {"dealerships":dealerships}
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request):
    context = {}
    reviews = []
    if request.method == "GET" and 'dealerId' in request.GET:
        context = getReviewByDealership(request.GET['dealerId'])
        if 'reviews' in context:
            for review in context['reviews']:
                if 'review' in vars(review):
                    reviews.append(vars(review))
        context = {"reviews":reviews}
        return render(request, 'djangoapp/dealer_details.html', context)
    
    elif request.method == "POST":
        print("do something lol")

def add_review(request, dealer_id=10):
        context = {}
        if request.method == "GET":
            print("get review form")
            cars = CarModel.objects.filter(DealerID=dealer_id)
            print("CARS:")
            print(cars)
            context = {
                "dealer_id": dealer_id,
                "cars": cars
            }
            return render(request, 'djangoapp/add_review.html', context)

        elif request.method == "POST":
            review = request.POST['review']
            car = request.POST['car'].split()
            car_year = int(car[0])
            car_make = car[1]
            car_model = car[2]
            purchase_date = request.POST['purchasedate']
            if 'purchasecheck' in request.POST:
                reviewData = {
                    "name": "anon",
                    "dealership": int(dealer_id),
                    "review": review,
                    "purchase": True,
                    "purchase_date": purchase_date,
                    "car_make": car_make,
                    "car_model": car_model,
                    "car_year": car_year
                }
            else:
                reviewData = {
                    "name": "anon",
                    "dealership": int(dealer_id),
                    "review": review,
                    "purchase": False,
                }
            print("Posting review" + str(reviewData))
            addReviewToCloudant(reviewData)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        

