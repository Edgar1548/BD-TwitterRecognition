import json
from ntpath import join
import os
from nltk.stem import SnowballStemmer
import re
from nltk import word_tokenize


def generateStopFile(file):
    with(open(file, "r", encoding="utf-8") as file):
        stop_list = [line.lower().strip()  for line in file]
    return stop_list

def clean(text):
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub('[()!?]', ' ', text)
    text = re.sub('@#\[.*?\]', ' ', text)
    text = re.sub("[^áéíóú+a-z0-9]", " ", text)
    text = re.sub('\\b[^0-9]{1} \\b', ' ', text)
    return text


def generateTokens(text, stop_words, languaje):
    tokens, tokens_return = [], []
    clean_text = clean(text.strip().lower())
    clean_text = word_tokenize(clean_text)
    if clean_text == []:
        return []
    tokens = [w for w in clean_text if not w in stop_words]
    stemmer = SnowballStemmer(languaje)
    for token in tokens:
        tokens_return.append(stemmer.stem(token))
    return tokens_return


def generateTokensOfFiles(data_path, stop_words):
    data_files = os.listdir(data_path)
    tokens_tweets = []
    tokens_file = []
    for file in data_files:
        decode_file = open(join(data_path, file), "r", encoding="utf-8")
        tweets = json.load(decode_file)
        for tweet_text in tweets:
            text = tweet_text['text']
            tokens_tweet = generateTokens(text, stop_words)
            tokens_tweets.extend(list(dict.fromkeys(tokens_tweet)))
        tokens_tweets = list(dict.fromkeys(tokens_tweets))
        tokens_file.append(tokens_tweets)
        tokens_tweets = []
        print("end" + file)
    return tokens_file

