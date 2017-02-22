# metadata.py
# hold the metadata for the search
# also, submit jobs, and process the results into counts and word vectors

def listify(raw_text,lang="en"):
    """Make a list of words from a string."""

    punctuation_to_replace = ["---","--","''"]
    for punctuation in punctuation_to_replace:
        raw_text = raw_text.replace(punctuation," ")
    # four groups here: numbers, links, emoticons, words
    # could be storing which of these things matched it...but don't need to
    words = [x.lower() for x in re.findall(r"(?:[0-9][0-9,\.]*[0-9])|(?:http://[\w\./\-\?\&\#]+)|(?:[\w\@\#\'\&\]\[]+)|(?:[b}/3D;p)|’\-@x#^_0\\P(o:O{X$[=<>\]*B]+)",raw_text,flags=re.UNICODE)]

    return words

food_keywords = ["food","foods","food security","food insecurity","groceries","water","drinks","prepare","preparing","grocery store","store","supermarket","food store","food market","farm","food bank","food assistance","shelter","food pantry","food shelf","SNAP","food stamps","unprepared","shock","help","supplies","fridge","generator","power","canned"]
event_keywords = ["rain","wind","emergency","snow","hurricane","tornado","flood*","watson","EF-*","sandy","irene"]
new=["bread","milk","eggs","hungry","starving","disaster","assistance","eat","mcdonalds","breakfast","dinner","lunch"]

from datetime import date,timedelta
events = [
    {"name": "Hurricane Sandy",
     "start": date(2012,10,30),
     "end": date(2012,10,31),
     "cost": 68.3,
     "states": ["MD","DE","NJ","NY","CT","MA","RI","NC","VA","WV","OH","PA","NH"]},
     {"name": "Hurricane Irene",
     "start": date(2011,8,26),
     "end": date(2011,8,28),
     "cost": 14.4,
     "states": ["NC","VA","MD","NJ","NY","CT","RI","MA","VT"]},
     {"name": "Tornadoes 1",
     "start": date(2011,4,25),
     "end": date(2011,4,28),
     "cost": 10.9,
     "states": ["AL","AR","LA","MS","GA","TN","VA","KY","IL","MO","OH","TX","OK"]},
     {"name": "Louisiana Flooding",
     "start": date(2016,8,12),
     "end": date(2016,8,15),
     "cost": 10.0,
     "states": ["LA"]},
     {"name": "Tornadoes 2",
     "start": date(2011,5,22),
     "end": date(2011,5,27),
     "cost": 9.7,
     "states": ["MO","TX","OK","KS","AR","GA","TN","VA","KY","IN","IL","OH","WI","MN","PA"]},
    ]

def makefolders():
    from os import mkdir
    for event in events:
        mkdir("raw-tweets/"+event["name"].lower().replace(" ","-"))
        for a in food_keywords+event_keywords:
            mkdir("raw-tweets/"+event["name"].lower().replace(" ","-")+"/"+a.replace(" ","-"))
    return 1

import re
def keywords_re_compiled():
    # all_keywords = food_keywords+event_keywords
    all_keywords = new_keywords
    return [x.replace(" ","-") for x in all_keywords],[re.compile(r"\b"+keyword.replace("*","[A-Za-z0-9]")+r"\b",flags=re.IGNORECASE) for keyword in all_keywords]

import time
import subprocess
def submit_all_jobs():
    for event in events:
        search_start = event["start"]-timedelta(days=7)
        search_len = (event["end"]-event["start"]).days+1+14
        for i in range(search_len):
            d = search_start+timedelta(days=i)
            job='''#PBS -l nodes=1:ppn=1
#PBS -l walltime=30:00:00
#PBS -N keywordScrape
#PBS -j oe

/gpfs2/scratch/areagan/realtime-parsing/RHEL7-python-3.5.1/bin/activate
which python
cd /users/a/r/areagan/scratch/2016-11-food-security
pwd

echo "processing {0}"
for HOUR in 0{{0..9}} {{10..23}};
do
    /usr/bin/time -v gzip -cd /users/c/d/cdanfort/scratch/twitter/tweet-troll/zipped-raw/{0}/{0}-$HOUR-{{00,15,30,45}}.gz | python processTweets.py {0}-$HOUR {1}
   echo $HOUR
done
echo "job script completed"'''.format(d.strftime('%Y-%m-%d'),event["name"].lower().replace(" ","-"))

            subprocess.call("echo '{0}' | qsub".format(job),shell=True)
            # print(job)
            # print("-"*80)
            time.sleep(0.1)

if __name__ == "__main__":
    # this submits jobs to grab the data
    # submit_all_jobs()

    # now let's grab some results
    # first let's just get the count of tweets.
    # `wc` will be faster than reading the file in python
    all_keywords = food_keywords+event_keywords
    all_keyword_folders = [x.replace(" ","-") for x in all_keywords]
    
    from os.path import join,isfile
    import numpy as np
    import pickle
    # from scipy.sparse import lil_matrix,issparse
    import sys
    import json
    sys.path.append("/users/a/r/areagan/work/2014/03-labMTsimple/")
    from labMTsimple.speedy import *
    from labMTsimple.storyLab import *
    my_LabMT = LabMT(stopVal=0.0)
    for event in events:
        event_folder = "raw-tweets/"+event["name"].lower().replace(" ","-")
        search_start = event["start"]-timedelta(days=7)
        search_len = (event["end"]-event["start"]).days+1+14
        tweet_counts = [np.zeros((search_len*24,)) for x in all_keywords]
        # sparse:
        # building scipy for python3 would be a days work
        # word_vectors = [lil_matrix((search_len*24,10222),dtype="i") for x in all_keywords]
        # dense:
        word_vectors = [np.zeros((search_len*24,10222),dtype="i") for x in all_keywords]
        for i in range(search_len):
            d = search_start+timedelta(days=i)
            print(d.strftime('%Y-%m-%d'))
            for hour in range(24):
                for j in range(len(all_keywords)):
                    full_file = join(event_folder,all_keyword_folders[j],d.strftime('%Y-%m-%d-{0:02d}.json'.format(hour)))
                    # print(full_file)
                    # this does just the lines...
                    # if isfile(full_file):
                    #     lines = int(subprocess.check_output("wc -l {0}".format(full_file),shell=True).decode("ascii").split(" ")[0])
                    # else:
                    #     lines = 0
                    # tweet_counts[j][i*24+hour] = lines
                    if isfile(full_file):
                        f = open(full_file,"r")
                        tweets = [json.loads(line) for line in f]
                        f.close()
                        tweet_counts[j][i*24+hour] = len(tweets)
                        word_dict = dict()
                        for tweet in tweets:
                            words = listify(tweet["text"])
                            for word in words:
                                if word in word_dict:
                                    word_dict[word] += 1
                                else:
                                    word_dict[word] = 1
                        word_vec = my_LabMT.wordVecify(word_dict)
                        word_vectors[j][i*24+hour,:] = word_vec
        # print(tweet_counts[0])
        f = open(join(event_folder,"tweet-counts.p"),"wb")
        f.write(pickle.dumps(tweet_counts,protocol=4))
        f.close()
        for j in range(len(all_keywords)):
            f = open(join(event_folder,all_key_word_folders[j]+"-word-vectors.p"),"wb")
            # f.write(pickle.dumps(word_vectors[j].tocsr(),protocol=4))
            f.write(pickle.dumps(word_vectors[j],protocol=4))
            f.close()
                


