1. To run
go to the corresponding folder
pipenv run pytest RESTTest.py

2. Test written
test_no_two_movie_should_have_same_name - Pass
test_no_two_movie_should_have_same_name_after_submitting_duplicate - Fail
test_all_poster_path_valid - Fail
test_sorting - Fail
test_no_more_than_7_400_genre_ids_movies - Pass
test_title_should_contain_palindrome - Pass
test_two_or_more_title_contain_other_another_title - Pass


3. Other tests I would like to try if I have enough time
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
