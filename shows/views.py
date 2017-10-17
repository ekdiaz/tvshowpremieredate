'''views.py - Contains the views for the site.'''
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Show
from .forms import SearchForm, UserCreationForm
import requests
import json

from django.contrib.auth import login, authenticate
from django.contrib import messages

def index(request):
    '''Shows the homepage if the user is authenticated with all the shows that
    the user is subscribed to and their images. If the user is not authenticated,
    then they are redirected to the login or signup page.'''
    if request.user.is_authenticated:
        results = []
        for show in Show.objects.all():
            if request.user in show.subscribers.all():
                url = 'http://api.tvmaze.com/shows/'
                url += str(show.show_id)
                r = requests.get(url)
                j = json.loads(r.text)
                # sentinel value (since a url will never be just "-1") if no image exists
                image_url = '-1'
                if j['image'] is not None:
                    # convert from http to https
                    image_url = j['image']['medium'][:4] + 's' + j['image']['medium'][4:]

                results.append({'show': show.name, 'image': image_url, 'date': show.date})
                # results.append({show.name: image_url})
        return render(request, 'shows/index.html', {'results':results})
    return render(request, 'shows/login_signup.html', {})

def unsubscribe(request, **kwargs):
    '''Shows the shows that the user is subscribed to (which are in kwargs)
    and enables them to unsubscribe.'''
    if request.user.is_authenticated:
        return render(request, 'shows/unsubscribe_results.html', kwargs)
    messages.add_message(request, messages.INFO, 'You are not logged in.')
    return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')

def search(request, **kwargs):
    '''Shows the shows (in kwargs) that match the searched term in searchShows.'''
    if request.user.is_authenticated:
        return render(request, 'shows/search_results.html', kwargs)
    messages.add_message(request, messages.INFO, 'You are not logged in.')
    return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')

def searchShows(request):
    '''Searches for the shows that match the search term using TVMaze API, and
    gets their show ids and images so they can be displayed in search(request,
    **kwargs).'''
    if request.user.is_authenticated:
        if request.method == 'GET':
            # Search the search term using the API.
            search = request.GET.get('search')
            u =  'http://api.tvmaze.com/search/shows?q='
            u += search

            # Get search results.
            req = requests.get(u)
            json_req = json.loads(req.text)
            i = 0

            # Parse search results for name, show id, and image.
            results = []
            ids = []
            images_1 = []
            images_2 = []
            while True:
                try:
                    show_name = json_req[i]['show']['name']
                    show_id = json_req[i]['show']['id']
                    results.append(show_name)
                    ids.append(show_id)

                    # If there exists an image for the show
                    if json_req[i]['show']['image'] is not None:
                        # Image URLs are in format
                        # http://static.tvmaze.com/uploads/images/medium_portrait/num1/num2.jpg
                        # so we get the two numbers num1 and num2 by using slicing.
                        # First we slice it so that it's num1/num2
                        # Then we slice that so that it's num1 and num2
                        # by finding the index of the slash, and convert them to ints.
                        images_1.append(int(json_req[i]['show']['image']['medium'][56:-4][:json_req[i]['show']['image']['medium'][56:-4].index('/')]))
                        images_2.append(int(json_req[i]['show']['image']['medium'][56:-4][json_req[i]['show']['image']['medium'][56:-4].index('/')+1:]))
                    else:
                        images_1.append(None)
                        images_2.append(None)
                    i += 1
                # There is an index error when there are no more results.
                except IndexError:
                    break
            # If no results, then let user know and redirect to home page.
            if len(results) == 0:
                messages.add_message(request, messages.INFO, 'No shows were found with that name.')
                return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')
            kw = {'results': results,
                'ids': ids,
                'images_1':images_1,
                'images_2':images_2}
            # Redirect to search results.
            url = reverse('shows:search_results', kwargs=kw)
            return HttpResponseRedirect(url)
        else:
            form = SearchForm()
        return render(request, 'shows/index.html', {'form': form})
    messages.add_message(request, messages.INFO, 'You are not logged in.')
    return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')

def sub_to_shows(request, **kwargs):
    '''Covers the backend for subscribing to shows.'''
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Gets list of show ids that are checked when form is submitted.
            ids = request.POST.getlist('show')
            if len(ids) == 0:
                messages.add_message(request, messages.INFO, 'At least one show must be chosen to subscribe.')
                url = reverse('shows:search_results', kwargs=kwargs)
                return HttpResponseRedirect(url)
            # Gets names of shows that the user wants to subscribe to
            for i in ids:
                u = 'http://api.tvmaze.com/shows/'
                u += i
                req = requests.get(u)
                json_req = json.loads(req.text)
                # If the show isn't already in the database, then add the show
                # and subscribe the user to it.
                if Show.objects.filter(show_id=i).count() == 0:
                    show = Show(name=json_req['name'], show_id=json_req['id'])
                    show.save()
                    show.subscribers.add(request.user)
                    messages.add_message(request, messages.INFO, 'You have been subscribed to ' + show.name + '.')
                # If the show is already in the database, then if the user isn't
                # already subscribed to the show, then subscribe the user. Else
                # give them a message that they are already subscribed.
                else:
                    show = Show.objects.filter(show_id=json_req['id'])[0]
                    if request.user not in show.subscribers.all():
                        show.subscribers.add(request.user)
                        messages.add_message(request, messages.INFO, 'You have been subscribed to ' + show.name + '.')
                    else:
                        messages.add_message(request, messages.INFO, 'You are already subscribed to ' + show.name + '.')
    else:
        messages.add_message(request, messages.INFO, 'You are not logged in.')
    return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')

def unsubscribe_results(request):
    '''Gets the results for unsubscribing (aka the shows that the user is
    already subscribed to) and their names, ids, and images.'''
    if request.user.is_authenticated:
        if request.method == 'GET':
            shows = Show.objects.all()
            results = []
            ids = []
            images_1 = []
            images_2 = []
            for show in shows:
                if request.user in show.subscribers.all():
                    url = 'http://api.tvmaze.com/shows/'
                    url += str(show.show_id)
                    r = requests.get(url)
                    j = json.loads(r.text)
                    results.append(show.name)
                    ids.append(show.show_id)

                    if j['image'] is not None:
                        # Image URLs are in format
                        # http://static.tvmaze.com/uploads/images/medium_portrait/num1/num2.jpg
                        # so we get the two numbers num1 and num2 by using slicing.
                        # First we slice it so that it's num1/num2
                        # Then we slice that so that it's num1 and num2
                        # by finding the index of the slash, and convert them to ints.
                        images_1.append(int(j['image']['medium'][56:-4][:j['image']['medium'][56:-4].index('/')]))
                        images_2.append(int(j['image']['medium'][56:-4][j['image']['medium'][56:-4].index('/')+1:]))
                    else:
                        images_1.append(None)
                        images_2.append(None)
            kw = {'results': results,
                'ids': ids,
                'images_1':images_1,
                'images_2':images_2}
            url = reverse('shows:unsubscribe_results', kwargs=kw)
            return HttpResponseRedirect(url)
        else:
            form = SearchForm()
        return render(request, 'shows/index.html', {'form': form})
    else:
        messages.add_message(request, messages.INFO, 'You are not logged in.')
    return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')

def unsub_to_shows(request, **kwargs):
    '''Covers the backend for unsubscribing to shows.'''
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Gets the list of shows that the user wants to unsubscribe to
            ids = request.POST.getlist('show')
            messages.add_message(request, messages.INFO, ids)
            if len(ids) == 0:
                messages.add_message(request, messages.INFO, 'At least one show must be chosen to unsubscribe.')
                url = reverse('shows:unsubscribe_results', kwargs=kwargs)
                return HttpResponseRedirect(url)
            for i in ids:
                # ids are in form u'###L' in the list, so get rid of the L
                # and convert to int.
                i2 = int(i[:len(i) - 1])
                # remove the user from the show's subscribers
                show = Show.objects.filter(show_id=i2)[0]
                show.subscribers.remove(request.user)
        messages.add_message(request, messages.INFO, 'You have been unsubscribed from ' + show.name + '.')
    else:
        messages.add_message(request, messages.INFO, 'You are not logged in.')
    return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')

def signup(request):
    '''This handles the backend of the UserCreationForm.'''
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                e = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password, email=e)
                login(request, user)
                return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')
        else:
            form = UserCreationForm()
        return render(request, 'shows/signup.html', {'form': form})
    messages.add_message(request, messages.INFO, 'You are already logged in. You must log out to create a new user.')
    return HttpResponseRedirect('http://tvshowpremieredate.pythonanywhere.com/home')