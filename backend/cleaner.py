import json
from os import listdir
from os.path import isfile, join


def encodeText(tweet_text):
    tweet_text = tweet_text.replace('\n', ' ')
    tweet_text = tweet_text.encode("utf-8")
    return str(tweet_text)


def parse_file(file_in, file_out):
    ptrFile_in = open(file_in, "r", encoding="utf-8")
    ptrFile_out = open(file_out, "w", encoding="utf-8")
    cleanLines = []
    tweets = json.load(ptrFile_in)
    for tweet in tweets:
        cleantweet = {}
        cleantweet.update({"id": tweet['id']})
        if tweet.get('RT_text') is None:
            cleantweet.update({"text": tweet['text']})
        else:
            cleantweet.update({"text": tweet['RT_text']})
        cleantweet.update({"user": tweet['user_name']})
        cleantweet.update({"date": tweet['date']})
        cleantweet.update({"retweeted": tweet['retweeted']})
        cleanLines.append(cleantweet)

    ptrFile_out.write(json.dumps(cleanLines, ensure_ascii=False))
    ptrFile_out.close()


def clean_data(path_in, path_out):
    for f in listdir(path_in):
        file_in = join(path_in, f)
        file_out = join(path_out, f)
        if isfile(file_in):
            parse_file(file_in, file_out)