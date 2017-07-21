from requests import get, post
from os import environ
from sys import argv, exit

if len(argv) != 2:
    exit('Usage: start.py <pipeline id>')

pipeline_id = int(argv[1])

print('Authenticating with token...')
jwt = get('https://api.screwdriver.cd/v4/auth/token?api_token=%s' % environ['SD_KEY']).json()['token']
print('Got JWT')

headers = { 'Authorization': 'Bearer %s' % jwt }

print('Getting jobs for pipeline %s...' % pipeline_id)
jobs = get('https://api.screwdriver.cd/v4/pipelines/%s/jobs' % pipeline_id, headers=headers).json()


print('Starting pipeline...')
start_request = post('https://api.screwdriver.cd/v4/builds', headers=headers, data=dict(jobId=jobs[0]['id']))


if start_request.status_code != 201:
    exit('Failed to start pipeline: %s' % start_request.json()['message'])

event_id = start_request.json()['eventId']
print('Started event %s' % event_id)
