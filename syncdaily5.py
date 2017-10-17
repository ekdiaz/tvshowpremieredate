'''This file is run daily to check if any new premiere dates
are known, or if any premiere date is coming up in 7 days.'''
# setup
import os
import django
os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings'
django.setup()

import requests
import json
from shows.models import Show, YesterdayID

import dateutil.parser
from datetime import timedelta
from django.utils import timezone


# Get all new episode show ids known yesterday
yesterday_ids = []
for i in YesterdayID.objects.all():
    yesterday_ids.append(i.show_id)

# get today's full schedule
schedule_req = requests.get('http://api.tvmaze.com/schedule/full')
schedule_json = json.loads(schedule_req.text)

# Get all new episode show ids from today
ids = []
k = 0
while True:
    try:
        ids.append(schedule_json[k]['_embedded']['show']['id'])
        k += 1
    # IndexError when no more shows remaining
    except IndexError:
        break

# Compare yesterday's ids to today's ids.
# If there's a new id from today, then add it and its
# index to new_ids and indices respectively.
# If there's a season premiere whose airstamp is
# different than the one listed, then change it
# and add it to new_ids so that an email will be
# sent out that the airstamp changed.
new_ids = []
indices = []
for i in range(len(ids)):
    if ids[i] not in yesterday_ids:
        new_ids.append(ids[i])
        indices.append(i)
    # check if the airstamp changed
    elif schedule_json[i]['number'] == 1:
        airstamp = schedule_json[i]['airstamp']
        date = dateutil.parser.parse(airstamp)
        for show in Show.objects.all():
            if ids[i] == show.show_id and date != show.date:
                new_ids.append(ids[i])
                indices.append(i)

# Check all new ids to see if they are a season premiere
id_premiere = {}
for i in indices:
    # if it's the first episode of a series
    if schedule_json[i]['number'] == 1:
        id_premiere[schedule_json[i]['_embedded']['show']['id']] = \
            schedule_json[i]['airdate']

# Email out to all subscribers of new season premieres the premiere date.
for show in Show.objects.all():
    if id_premiere.has_key(show.show_id):
        # email out premiere date!
        subj = show.name + ' premieres on ' + id_premiere[show.show_id]
        msg = 'Thanks for using tvshowpremieredate!'
        for user in show.subscribers.all():
            user.email_user(subj, msg)

# set yesterday_ids to ids for tomorrow
YesterdayID.objects.all().delete()
for i in ids:
    yesterday_id = YesterdayID(show_id=i)
    yesterday_id.save()


# Send out email notification for a week ahead
i = 0
number_ids = []
while True:
    try:
        if schedule_json[i]['number'] == 1:
            # format is (for example) 2017-07-10T01:00:00+00:00 ISO 8601
            airstamp = schedule_json[i]['airstamp']
            date = dateutil.parser.parse(airstamp)
            for show in Show.objects.all():
                if show.show_id == schedule_json[i]['_embedded']['show']['id']:
                    show.date = date
                    show.save()
                    if timezone.now() + timedelta(days=7) > date \
                        and timezone.now() + timedelta(days=6) < date:
                        # email out premiere date!
                        channel = schedule_json[i]['_embedded']['show']['network']['name']
                        subj = 'Reminder: ' + show.name + ' premieres in one week on ' + airstamp + ' on ' + channel + '!'
                        msg = 'Thanks for using tvshowpremieredate!'
                        for user in show.subscribers.all():
                            user.email_user(subj, msg)
        i += 1
    except IndexError:
        break