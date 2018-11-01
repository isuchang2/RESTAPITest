import json
import requests
from pandas.io.json import json_normalize
import uuid
import math

geturl = 'https://splunk.mocklab.io/movies?q=batman'
headers_get = {'Accept': 'application/json'}
headers_post = {'Content-Type': 'application/json'}
posturl = 'https://splunk.mocklab.io/movies'


# Below are tests
def test_no_two_movie_should_have_same_name():
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    assert len(t.get('title')) == len(set(t.get('title')))

def test_sample():
    assert 3+5 == 8