# After a few requests, comments_data.content is the generic New York Times error page, but
# comments_data does not have a 404 response or anything. It's a valid request, but NY Times
# can't process it for whatever reason. The rate limit is 30 calls/second and 5000/day, so
# that's not the issue. See if you can get it to work, I guess.
#
# I used simplejson, which you can install with pip, because it gives better error messages,
# but you can just replace simplejson with json and it should work the same.

import requests, time, simplejson, sys
from datetime import date, datetime, timedelta
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

# Scrape 300 comments per day from Nov. 1, 2014 to Oct. 31, 2015
comments = []
for da in perdelta(date(2014, 11, 1), date(2015, 11, 1), timedelta(days=1)):
    print da
    for i in range(12):
        url = ('http://api.nytimes.com/svc/community/v3/user-content/' +
               'by-date.json?api-key=PUTYOURAPIKEYHERE&date=' + str(da) + # put your API key in here
               '&offset=' + str(25*i))
        comments_data = requests.get(url)
        try:
            data = simplejson.loads(comments_data.content) # error happens here
        except:
            print url, comments_data, comments_data.content
            sys.exit()
        for d in data['results']['comments']:
            comments.append(d)
        time.sleep(2)

# Save the data
with open("comments.json", 'w') as f:
    simplejson.dump(comments, f)

# Uncomment for error-tolerant version
#
# for da in perdelta(date(2014, 11, 5), date(2015, 11, 1), timedelta(days=1)):
#     comments = []
#     print da
#     for i in range(12):
#         success = False
#         url = ('http://api.nytimes.com/svc/community/v3/user-content/' +
#                'by-date.json?api-key=KEY&date=' + str(da) +
#                '&offset=' + str(25*i))
#         while not success:
#             comments_data = requests.get(url)
#             try:
#                 data = simplejson.loads(comments_data.content)
#                 success = True
#                 for d in data['results']['comments']:
#                     comments.append(d)
#                 time.sleep(2)
#             except:
#                 print 'error on {}'.format(str(da))
#                 print url
#                 time.sleep(2)
                
#     filestr = 'comments {}.json'.format(str(da))
#     with open(filestr, 'w') as f:
#         simplejson.dump(comments, f)