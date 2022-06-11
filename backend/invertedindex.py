from cmath import sqrt
from math import log10
import os

from ntpath import join
from generate_tokens import generateTokens
from memoriasec import writeJsonData, readJsonData
from collections import Counter


def generateIndexInv(data_path, stop_words, languaje, indexinv_path):
    data_files = os.listdir(data_path)
    index_inv = {}
    num_tweets = 0
    for file in data_files:
        tweets = readJsonData(join(data_path, file))
        num_tweets += len(tweets)
        i = 0
        for tweet in tweets:
            i += 1
            text = tweet['text']
            text_tokens = generateTokens(text, stop_words, languaje)
            if text_tokens == []:
                continue
            tokens_count = dict(Counter(text_tokens))
            for token in tokens_count:
                if token not in index_inv:
                    index_inv[token] = [0, {}]
                if tweet['id'] not in index_inv[token][1]:
                    index_inv[token][1][tweet['id']] = [
                        tokens_count[token], (i - 1, file)
                    ]
                    index_inv[token][0] += 1
    writeJsonData(indexinv_path, index_inv)
    with(open("N.txt", "w", encoding="utf-8") as file):
        file.write(str(num_tweets))
    return num_tweets


def generateNorm(index_path, N, norm_path):
    norms = {}
    indexdb = readJsonData(index_path)
    for term in indexdb:
        for doc in indexdb[term][1]:
            try:
                norms[doc] += (log10(1 + indexdb[term][1][doc][0]) *
                               log10(N / indexdb[term][0]))**2
            except:
                norms[doc] = (log10(1 + indexdb[term][1][doc][0]) *
                              log10(N / indexdb[term][0]))**2
    for doc in norms:
        norms[doc] = sqrt(norms[doc]).real
    writeJsonData(norm_path, norms)
    return norms
