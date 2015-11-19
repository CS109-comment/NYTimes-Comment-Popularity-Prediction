# After a few requests, comments_data.content is the generic New York Times error page, but
# comments_data does not have a 404 response or anything. It's a valid request, but NY Times
# can't process it for whatever reason. The rate limit is 30 calls/second and 5000/day, so
# that's not the issue. See if you can get it to work, I guess.
#
# I used simplejson, which you can install with pip, because it gives better error messages,
# but you can just replace simplejson with json and it should work the same.
#
# This version is very error-tolerant. It can deal with invalid JSON and stores the results
# for each day separately to guard against crashes. We then have to combine ~600 text files,
# but this shouldn't be too hard, and is in my opinion worth it since the NY Times is so much
# trouble.

import requests, time, simplejson, sys
from datetime import date, datetime, timedelta

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

# Scrape 300 comments per day from Nov. 1, 2014 to Oct. 31, 2015
for da in perdelta(date(2015, 2, 21), date(2015, 11, 1), timedelta(days=1)):
    comments = []
    print da
    skip = False
    gotany = True
    for i in range(12): # collect 25*12=300 comments
        if not skip:
            success = False
            count = 0
            url = ('http://api.nytimes.com/svc/community/v3/user-content/' +
                   'by-date.json?api-key=KEY&date=' + str(da) +
                   '&offset=' + str(25*i))
            while not success:
                comments_data = requests.get(url)
                try:
                    data = simplejson.loads(comments_data.content)
                    success = True # go to the next offset
                    for d in data['results']['comments']:
                        comments.append(d)
                    time.sleep(2)
                except:
                    print 'error on {}'.format(str(da))
                    print url
                    count += 1
                    if count > 3:
                        success = True # not really
                        skip = True # just skip to the next day
                        if i == 0:
                            gotany = False # if we didn't get any comments from that day
                    time.sleep(2)
    if gotany:      
        filestr = 'comments {}.json'.format(str(da))
        with open(filestr, 'w') as f:
            simplejson.dump(comments, f)

# Short script to combine all the JSON lists into one
allcomments = []
for d in perdelta(date(2014, 1, 1), date(2015, 12, 31), timedelta(days=1)):
    try:
        with open('comments {}.json'.format(str(d))) as f:
            c = simplejson.load(f)
            allcomments.extend(c)
    except:
        pass