#from gtgs.users.models import User
import os
from PIL import Image
from datetime import datetime
import json


text = """
{'model': 'users.user',
'pk': {},
'fields': {'password': 'argon2$argon2i$v=19$m=512,t=2,p=2$anJjTXh3bUhwVFFX$8eDRlzJ2al/KYJdhYhR4Qg',
'last_login': '2017-11-27T15:43:03Z',
'is_superuser': false,
'username': '{}',
'first_name': ',
'last_name': ',
'email': '{}@scielo.org',
'is_staff': true,
'is_active': true,
'date_joined': '2017-11-22T17:50:32Z',
'name': ',
'birthdate': '{}',
'anniversary': '{}',
'photo': '{}',
'is_checked': false,
'is_checked_by_admin': false,
'groups': [],
'user_permissions': []}},
"""


def format_register(id, username, birthdate, anniversary, photo):
    model = {}
    model['model'] = 'users.user'
    model['pk'] = id
    fields = {}
    fields['password'] = 'argon2$argon2i$v=19$m=512,t=2,p=2$anJjTXh3bUhwVFFX$8eDRlzJ2al/KYJdhYhR4Qg'
    fields['last_login'] = '2017-11-27T15:43:03Z'
    fields['is_superuser'] = False
    fields['username'] = username
    fields['first_name'] = ''
    fields['last_name'] = ''
    fields['username'] = username
    fields['email'] = username+'@scielo.org'
    fields['is_staff'] = False
    fields['is_active'] = True
    fields['date_joined'] = '2017-11-22T17:50:32Z'
    fields['name'] = ''
    fields['birthdate'] = birthdate.isoformat()[:10]
    fields['anniversary'] = anniversary.isoformat()[:10]
    fields['birthdate_alert'] = True
    fields['anniversary_alert'] = True
    fields['photo'] = photo
    fields['is_checked'] = False
    fields['is_checked_by_admin'] = False
    fields['groups'] = []
    fields['user_permissions'] = []
    model['fields'] = fields
    return model


data = {}

for item in open('../temp/anniversary.csv').readlines():
    item = item.replace('_', '-').strip()
    image = item
    if '-' in item:
        parts = item[:item.rfind('.')].split('-')
        print(parts)
        month, day, username, year = parts
        data[username] = [(int(year), int(month), int(day))]


for item in open('../temp/faces.csv').readlines():
    image = item.strip()
    item = item.replace('_', '-').strip()
    if '-' in item:
        parts = item[:item.rfind('.')].split('-')
        print(parts)
        month, day, username = parts
        year = 1987
        if data.get(username) is not None:
            year = data.get(username)[0][0]
            year = int(year) - 25
        year = str(year)
        if username not in data.keys():
            data[username] = [(int(year), int(month), int(day))]

        data[username].append(image)
        data[username].append((int(year), int(month), int(day)))


def update_or_create(data, model):
    defaults = {
    }

    try:
        obj = model.objects.get(username=data.get('username'))
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
    except model.DoesNotExist:
        try:
            new_values = data
            new_values.update(defaults)
            obj = model(**new_values)
            obj.save()
        except:
            print('error', username)


def format_data(username, u_data):
    print(u_data)
    d = {
            'username': username,
            'anniversary': datetime(u_data[0][0], u_data[0][1], u_data[0][2]),
            'birthdate': datetime(u_data[2][0], u_data[2][1], u_data[2][2]),
        }
    f = '../media/'+u_data[1]
    if os.path.isfile(f):
        d['photo'] = f
    d['photo'] = u_data[1]
    d['photo'] = 'perfil.png'

    return d


i = 101
j = []
for username, u_data in data.items():
    
    d = format_data(username, u_data)
    print(username)
    print(u_data)
    j.append(format_register(i, username, d['birthdate'], d['anniversary'], d.get('photo')))
    i += 1
    #d = format_data(username, u_data)
    #update_or_create(d, User)

open('input.user.json', 'w').write(json.dumps(j))


# ./manage.py dumpdata 
# ./manage.py loaddata user.json 


# (./data/media) /Users/roberta.takenaka/github.com/robertatakenaka/scielo/gtgs/gtgs/media
# (/app/media) /Users/roberta.takenaka/github.com/robertatakenaka/scielo/gtgs/gtgs/media
