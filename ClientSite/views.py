'''
Author: Farmehr Farhour f.farhour@gmail.com
'''
# Django settings for Client project.
import os

#Define relevant paths
VIEWS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(VIEWS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
GTFSSTOPS_PATH = os.path.join(PROJECT_PATH, 'stops.txt')

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

#import for login functionality
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

#import for decorator access restriction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

##REQUEST DATA FROM AT API

#import requests
import requests
#import json
import json
from threading import Thread
import time

#query the api server for Shapesby TripID data
url = requests.get("http://api.at.govt.nz/v1/gtfs/shapes/tripId/0070ML577521154231898?api_key=0dd6fe7c-5b44-45db-a5c2-023558a490d3")
#convert to python 
data = url.json()
#store the response only
if data['status']=='OK':
    response = data['response']
else:
    print('ERROR')

#define lat/long lists
latlist1 = []
longlist1 = []

for a in response:
    latlist1.append(a['shape_pt_lat'])
    longlist1.append(a['shape_pt_lon'])




#randomizer
"""
#query the api server for stops data
urlStops = requests.get('http://api.at.govt.nz/v1/gtfs/stops?api_key=0dd6fe7c-5b44-45db-a5c2-023558a490d3')
#convert to python 
dataStops = urlStops.json()
'''
#store the response only
if data['status']=='OK':
    responseStops = dataStops['response']
else:
    print('ERROR')
'''
responseStops = dataStops['response']
#define lat/long lists
latlistStops = []
longlistStops = []

for a in responseStops:
    latlistStops.append(a['stop_lat'])
    longlistStops.append(a['stop_lon'])
"""
import decimal
latlistStops = []
longlistStops = []
f = open(GTFSSTOPS_PATH,'r')
next(f)
fileData = f.readlines()
for line in fileData:
        bits = line.split(',')
        longlistStops.append(float(bits[4]))
        latlistStops.append(float(bits[3]))

import random
latlist2= []
longlist2 = []
for i in range (5000):
    a = random.randint(0, len(latlistStops) - 1)
    latlist2.append(latlistStops[a])
    longlist2.append(longlistStops[a])

latlist3= []
longlist3 = []
for i in range (5000):
    a = random.randint(0, len(latlistStops) - 1)
    latlist3.append(latlistStops[a])
    longlist3.append(longlistStops[a])

#add a decorator to restrict access to index
@login_required
def map(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'point1': "176,-36",'lat':latlist1,'long':longlist1,'lat2':latlist2, 'long2':longlist2,'lat3':latlist3, 'long3':longlist3}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('ClientSite/map.html', context_dict, context)

@login_required
def heatmap(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('ClientSite/heatmap.html', context_dict, context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/ClientSite/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('ClientSite/login.html', {}, context)



#add a decorator to restrict access
@login_required
def user_logout(request):
    # logout
    logout(request)

    # Take the user back
    return HttpResponseRedirect('/')

def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('ClientSite/index.html', context_dict, context)

#add a decorator to restrict access
@login_required
def navigate(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('ClientSite/navigate.html', context_dict, context)
'''
def points(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    points = points.objects.get(points = request.GET['points'])
    print(points)

    # Construct a dictionary to pass to the template engine as its context.
    context_dict = {'point1': "176,-36",'lat':points[1,3],'long':points[0,2]}

    # Return a rendered response to send to the client..
    return render_to_response('ClientSite/map.html', context_dict, context)
'''