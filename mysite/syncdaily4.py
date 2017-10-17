# import os
# os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings'

import requests
import json
from .shows.models import Show, YesterdayID
from django.core.mail import send_mail

yesterday_ids = []
for i in YesterdayID.objects.all():
    yesterday_ids.append(i.show_id)

schedule_req = requests.get('http://api.tvmaze.com/schedule/full')
schedule_json = json.loads(schedule_req.text)

ids = []
k = 0
while True:
    try:
        ids.append(schedule_json[k]['_embedded']['show']['id'])
        k += 1
    except IndexError:
        break

new_ids = []
indices = []
j = 0
for i in ids:
    if i not in yesterday_ids:
        new_ids.append(i)
        indices.append(j)
    j += 1

id_premiere = {}
for i in indices:
    # if it's the first episode of a series
    if schedule_json[i]['number'] == 1:
        id_premiere[schedule_json[i]['_embedded']['show']['id']] = schedule_json[i]['airdate']

for show in Show.objects.all():
    if id_premiere.has_key(show.show_id):
        # email out premiere date!
        subj = show.name + ' premieres on ' + id_premiere[show.show_id]
        msg = 'Thanks for using tvshowpremieredate!'
        for user in show.subscribers.all():
            worked = send_mail(
                subj,
                msg,
                'tvshowpremieredate@gmail.com',
                [user.email],
                fail_silently=False,
            )

# set yesterday_ids to ids for tomorrow
YesterdayID.objects.all().delete()
for i in ids:
    yesterday_id = YesterdayID(show_id=i)
    yesterday_id.save()
