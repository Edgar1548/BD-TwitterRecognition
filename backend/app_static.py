from ntpath import join
from memoriasec import readJsonData
import params
from generate_tokens import generateTokens
from collections import Counter
from retrievalscore import ScoreRetrieval

def consultStatic(query, topk, indexinv):
    n = 0
    with(open("N.txt", "r", encoding="utf-8") as file):
        for i in file:
            n = i
    norms = readJsonData(params.norm_path)

    query_tf = dict(Counter(query))

    score = ScoreRetrieval(query, query_tf, indexinv, int(n), norms)
    score = score[:topk]

    consult_response = {}
    path = score[0][1][1][1]
    tweets = readJsonData(join(params.static_path_clean, path))
    for i in score:
        temp = i[1][1][1]
        if path != temp:
            tweets = readJsonData(join(params.static_path_clean, temp))
            path = temp
        data = tweets[i[1][1][0]]
        consult_response[i[0]] = [data['text'], data['date'], data['user'], round(i[1][0], 5)]

    return consult_response
