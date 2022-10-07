from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Event
from . import db
import json
import requests
import pymsgbox
from flask_paginate import Pagination, get_page_args, get_page_parameter

# defines that this is a blueprint of our app
# this has a bunch of urls in here for navigation
# blueprint lets us break up files for readability
views = Blueprint('views', __name__)

# store the url and api_key for reuse
url = "https://app.ticketmaster.com/discovery/v2/"
api_key = "Bp0o0LwAEIR2zOwa7h1eoT7BnylC1kst"
# creating an empty global list to store all events found by search
events = []


# defines url to get to this page and what methods are allowed
# whenever you hit this route it calls this function
# cannot get to home page unless you're logged in
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # using index to get all the data from the search
    index = 0

    # getting the data from the two input fields
    if request.method == 'POST':
        place = request.form.get('city')
        keyword = request.form.get("keyword")
        if keyword and place:
            # looping through until the page number hits the totalPages
            # this gets all the data from the search criteria so I can paginate through it
            while True:
                url_string = f"{url}events.json?apikey={api_key}&keyword={keyword}&locale=*&size=18&page={index}&city={place}"
                resp = requests.get(url_string)
                if resp.ok and resp.json()['page']['totalElements'] != 0:
                    events.extend(resp.json()['_embedded']['events'])
                    index = index + 1
                    if index == resp.json()['page']['totalPages']:
                        break
                else:
                    pymsgbox.alert(
                        f'Bummer, no upcoming {keyword} events in {place}', 'FAIL!')
                    break
    # this is for pagination
    # gets the args I need, sets them to the values I want and passes it to home.html
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    per_page = 18
    offset = (page - 1) * per_page
    total = len(events)
    pagination_events = events[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template("home.html", user=current_user, items=pagination_events, pagination=pagination)
# render_template is what loads the data on the html pages
    # this is also how we pass in variables to be used in html templating language


@views.route('/watch-list', methods=['GET', 'POST'])
@login_required
def watch_list():
    return render_template("watch_list.html", user=current_user)


@views.route('/add-to-list', methods=['POST'])
@login_required
def add_to_list():
    # querying the 'evtId' from the route 'delete-event'
    # now i can make another api call with that id
    # then commit the event to my db
    event = json.loads(request.data)
    event_id = event['eventId']

    if event_id:
        resp = requests.get(
            f"{url}events?apikey={api_key}&id={event_id}&locale=*")
        if resp.ok:
            data = resp.json()['_embedded']['events'][0]

            img = data['images'][0]['url']
            name_taken = data['name']
            locations = data['_embedded']['venues']
            time = data['dates']['start']['localDate']

            site = data['url']
            for locale in locations:
                location = locale['city']['name']
            if name_taken and img and time and location and site:
                new_event = Event(title=name_taken, image=img, date=time,
                                  city=location, website=site, user_id=current_user.id)
                db.session.add(new_event)
                db.session.commit()
                pymsgbox.alert(f'{name_taken} has been added to your watch list!',
                               'SUCCESS!')
        else:
            pymsgbox.alert(f'Request error: {resp}', 'ERROR')

    return jsonify({})


@views.route('/delete-event', methods=['POST'])
def remove_evt():
    evt = json.loads(request.data)
    # querying the 'evtId' from the route 'delete-event'
    # then querying the event from my db with the id
    # now I can use that to remove it from my db below
    evtId = evt['evtId']
    evt = Event.query.get(evtId)
    if evt:
        if evt.user_id == current_user.id:
            db.session.delete(evt)
            db.session.commit()
            pymsgbox.alert(f'{evt.title} has been removed from your watch list!',
                           'SUCCESS!')

    return jsonify({})
