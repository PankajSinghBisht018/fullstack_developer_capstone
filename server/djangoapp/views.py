import json
import logging
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Login view to handle sign-in requests
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    # Try to authenticate the user
    user = authenticate(username=username, password=password)
    if user is not None:
        # If valid, log in the user
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username})

# Logout view to handle sign-out requests
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})

# Registration view to handle user sign-up
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})
    
    # Create a new user and log them in
    user = User.objects.create_user(
        username=username, first_name=first_name, last_name=last_name, password=password, email=email
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})

# View to get dealerships
def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# View to get dealer reviews
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment_response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = sentiment_response.get('sentiment', 'Unknown')
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})

# View to get dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})

# View to add a review
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(f"Error posting review: {e}")
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    return JsonResponse({"status": 403, "message": "Unauthorized"})

# View to get car models
def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()
    
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name} for car_model in car_models]
    
    return JsonResponse({"CarModels": cars})
