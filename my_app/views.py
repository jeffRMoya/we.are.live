from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Event
from . import db
import json
import requests

views = Blueprint('views', __name__)

url = "https://app.ticketmaster.com/discovery/v2/"
api_key = "Bp0o0LwAEIR2zOwa7h1eoT7BnylC1kst"


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    locales = {}
    events = {}

    if request.method == 'POST':
        place = request.form.get('city')
        keyword = request.form.get("keyword")

        if keyword and place:
            resp = requests.get(
                f"{url}events.json?apikey={api_key}&keyword={keyword}&locale=*&size=20&city={place}")
            if resp.ok:
                events = resp.json()['_embedded']['events']
                for event in events:
                    locales = event['_embedded']['venues']
            else:
                flash(
                    f"Error occurred. Response code: {resp}", category='error')

    return render_template("home.html", user=current_user, items=events, locations=locales)


@views.route('/watch-list', methods=['GET', 'POST'])
@login_required
def watch_list():
    return render_template("watch_list.html", user=current_user)


@views.route('/add-to-list', methods=['POST'])
@login_required
def add_to_list():
    event = json.loads(request.data)
    event_id = event['eventId']

    if event_id:
        resp = requests.get(
            f"{url}events?apikey={api_key}&id={event_id}&locale=*")
        if resp.ok:
            data = resp.json()['_embedded']['events'][0]
            print(data.keys())
            img = data['images'][0]['url']
            name_taken = data['name']
            locations = data['_embedded']['venues']
            time = data['dates']['start']['localDate']
            print(type(time))
            site = data['url']
            for locale in locations:
                location = locale['city']['name']
                print(img, name_taken, time, site, location)
            if name_taken and img and time and location and site:
                new_event = Event(title=name_taken, image=img, date=time,
                                  city=location, website=site, user_id=current_user.id)
                db.session.add(new_event)
                db.session.commit()
                flash(f'{name_taken} added to your watch list!',
                      category='success')
        else:
            flash(f'Request error: {resp}', category='error')

    return jsonify({})


@views.route('/delete-event', methods=['POST'])
def remove_evt():
    evt = json.loads(request.data)
    evtId = evt['evtId']
    evt = Event.query.get(evtId)
    if evt:
        if evt.user_id == current_user.id:
            db.session.delete(evt)
            db.session.commit()

    return jsonify({})
