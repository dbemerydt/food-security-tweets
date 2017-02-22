# processTweets.py
# crawl the tweets, and look for keywords
# output with daily resolution
#
# NOTES
# uses the new 15-minute compressed format
# 
# USAGE 
# gzip -cd tweets.gz | python processTweet.py 2014-01-01 keywords
#  
# this will read keywords.txt and the tweets from stdin
# and save a frequency file, labMT vector in keywords/[keyword]
# for each keyword

# we'll use most of these
from json import loads,dumps
import codecs
import datetime
import re
import sys

from metadata import *
folders,keywords = keywords_re_compiled()

def tweetreader(tweet,outfile):
    # takes in the hashtag-stripped text
    # the keyword list
    # and the title of the file to append to
    for i,keyword_re in enumerate(keywords):
        if keyword_re.search(tweet["text"]) is not None:
            g = codecs.open("raw-tweets/{0}/{1}/{2}.json".format(outfile[0],folders[i],outfile[1]),"a","utf8")
            g.write(dumps(tweet))
            g.write("\n")
            g.close()

def gzipper(outfile):
    f = sys.stdin
    for line in f:
        try:
            tweet = loads(line)
        except:
            print("failed to load a tweet")
        if "text" in tweet:
            # print("found text")
            tweetreader(tweet,outfile)

if __name__ == "__main__":
    # load the things
    outfile = [sys.argv[2],sys.argv[1]]
    
    gzipper(outfile)
    
    print("complete")

    # makefolders()

  








