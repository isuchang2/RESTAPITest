import json
import requests
from pandas.io.json import json_normalize
import uuid
import math

geturl = 'https://splunk.mocklab.io/movies?q=batman'
headers_get = {'Accept': 'application/json'}
headers_post = {'Content-Type': 'application/json'}
posturl = 'https://splunk.mocklab.io/movies'


def setup_module(module):
    print("setup_module      module:%s" % module.__name__)


# Below are tests
def test_no_two_movie_should_have_same_name():
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    assert len(t.get('title')) == len(set(t.get('title')))


def test_no_two_movie_should_have_same_name_after_submitting_duplicate():
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    count1 = len(t.get('id'))
    newname = "batman 2" + str(uuid.uuid4())
    while newname in t.get('title'):
        newname = "batman 3" + uuid.uuid4()
    data = {"name": newname, "description": "the best movie ever made"}
    r = requests.post(posturl, data=json.dumps(data), headers=headers_post)
    assert r.status_code == 200
    r = requests.post(posturl, data=json.dumps(data), headers=headers_post)
    assert r.status_code == 400  # make sure duplicate submits are handled with proper error code
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    count2 = len(t.get('id')) - 1
    assert count1 == count2
    test_no_two_movie_should_have_same_name()


def test_all_poster_path_valid():
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    posterurl = t.get('poster_path')
    for s in posterurl:
        assert math.isnan(s) == False
        assert s.startswith('http') == True or s == 'None'


def test_sorting():
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    genre_ids = t.get('genre_ids')
    count = sum(len(x) == 0 for x in genre_ids)
    null_lst = t.get('id')[0:count]
    lst = t.get('id')[count:]
    for l in range(0, count):
        assert len(genre_ids[l]) == 0
    assert sorted(null_lst) == null_lst
    assert sorted(lst) == lst


def test_no_more_than_7_400_genre_ids_movies():
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    genre_ids = t.get('genre_ids')
    count = sum(1 for x in genre_ids if sum(x) > 400)
    assert count < 7


def test_title_should_contain_palindrome():  # assume word with lenth 1 is palindrome
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    title = t.get('title')
    lst = ''.join(title).replace(':', '').replace('.', '').split(' ')
    count = 0
    for s in lst:
        if str(s.lower()) == str(s.lower())[::-1]:
            count += 1
    assert count > 0


def test_two_or_more_title_contain_other_another_title():
    r = requests.get(geturl, headers=headers_get)
    t = json_normalize(json.loads(r.content), record_path='results')
    title = t.get('title')
    word_freq = {}
    count = 0
    for s in title:
        s = set(s.replace(':', '').replace('.', '').split(' '))
        for word in s:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
            if word_freq[word] == 2:
                count += 1
    assert count > 1

#
# # other API related testing
# different accept and content-type value used in GET and POST
# different REST call using UPDATE, PUT, DELETE
# different encoding
# uploading 1 or multiple movies in one request
# delete movie if supported
# different chunking, especially chunked upload
# query movie using get by specifying a specific valid num
# query movie using get by specifying an invalid num (negative, or larger than total count stored)
# paging (if response is too big, and will be split into pages), and corresponding counting update (e.g. no more than 7 movies with 400+ genre_ids_movies)
# HTTP supported or not
# HTTP/S 1.0, 1.1, 2 supported or not
# cert expired or not trusted by browser
# Oauth2 supported or not, if yes, refresh and invalid and revoked token should also be tested
# non json format upload
# other parameters in get other than q should be correctly handled if not supported
# support 2 or more concurrent transactions
# handle properly when 2 or more concurrent transactions are submitting the same movie - from same location
# handle properly when 2 or more concurrent transactions are submitting the same movie - from different locations/distributed way
#
#
# #content specific testing
# unicode or non-english movie supported or not (esp in title for checking palindrome or genre_ids)
# movies with mixed language
# url encoding in poster_path supported or not
# 2 or more movies with same content but different language in title (e.g. same Batman movie one in English title, one in Chinese title)
# movies with new fields in the json
# movies with BASE64 encoding fields in json
# single movie with super large content (e.g. in overview)
# handle specific wording case - e.g. language word start from right to left
#
#
# #perf or throttling or timeout handling or security related (OWASP top 10) testing not considered
#
#
