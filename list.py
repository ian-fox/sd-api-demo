from requests import get, post
from os import environ
from sys import argv, exit


if len(argv) != 2:
    exit('Usage: list.py <pipeline id>')

pipeline_id = int(argv[1])

print('Authenticating with token')
jwt_request = get('https://api.screwdriver.cd/v4/auth/token?api_token=%s' % environ['SD_TOKEN']).json()

try:
    jwt = jwt_request['token']
except:
    exit('Invalid token')

print('Got JWT')

headers = { 'Authorization': 'Bearer %s' % jwt }


print('Getting events for pipeline %s' % pipeline_id)
events = get('https://api.screwdriver.cd/v4/pipelines/%s/events' % pipeline_id, headers=headers).json()

results = {}
total = len(events)
last_event_status = None

print('%s events found' % total)

if len(events) > 20:
    print('Taking most recent 20')
    events = events[:20]
    total = 20

for event in events:
    build = get('https://api.screwdriver.cd/v4/events/%s/builds' % event['id'], headers=headers).json()[0]
    if not build['status'] in results:
        results[build['status']] = 0

    if last_event_status is None:
        last_event_status = build['status']

    results[build['status']] += 1

for status in results:
    print('%s: %s events' % (status, results[status]))

print('Status of last event: %s' % last_event_status)
