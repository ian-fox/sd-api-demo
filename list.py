from requests import get, post
from os import environ
from time import sleep
from sys import argv


if len(argv) != 2:
    raise Exception('Usage: list.py <pipeline id>')

pipeline_id = int(argv[1])

print('Authenticating with token')
jwt = get('https://api.screwdriver.cd/v4/auth/token?access_key=%s' % environ['SD_KEY']).json()['token']
print('Got JWT')

headers = { 'Authorization': 'Bearer %s' % jwt }


print('Getting events for pipeline %s' % pipeline_id)
events = get('https://api.screwdriver.cd/v4/pipelines/%s/events' % pipeline_id, headers=headers).json()

results = {}
total = len(events)
last_event_status = None

print('%s events found' % total)

for event in events:
    build = get('https://api.screwdriver.cd/v4/events/%s/builds' % event['id'], headers=headers).json()[0]
    if not build['status'] in results:
        results[build['status']] = 0

    if last_event_status is None:
        last_event_status = build['status']

    results[build['status']] += 1

for status in results:
    print('%s: %s builds (%s %%)' % (status, results[status], int(results[status]/total*100)))

print('Status of last event: %s' % last_event_status)
