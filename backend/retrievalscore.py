import heapq
from math import log10, sqrt


def generateTfIdfSquareQuery(dic_tf, index_inv_df, N):
    tf_idf = {}
    square = 0
    for i in dic_tf:
        try:
            idf = log10(N / index_inv_df[i][0])
            tf = log10(1 + dic_tf[i])
            tf_idf[i] = tf * idf
            square += tf_idf[i]**2
        except:
            continue
    return [tf_idf, sqrt(square)]


def generateTfIdfQueryDocs(query_tokens, index_inv_filter, N):
    doc_tf_idf = {}
    for term_dic in query_tokens:
        try:
            tweets = index_inv_filter[term_dic][1]
            for doc in tweets:
                tf_tweet_term = log10(1 + tweets[doc][0])
                idf_tweet_term = log10(N / index_inv_filter[term_dic][0])
                tf_idf = tf_tweet_term * idf_tweet_term
                if doc not in doc_tf_idf:
                    doc_tf_idf[doc] = [{},
                                       (tweets[doc][1][0], tweets[doc][1][1])]
                doc_tf_idf[doc][0][term_dic] = tf_idf
        except:
            continue
    return doc_tf_idf


def ScoreRetrieval(query_tokens, query_tf, invertedindex_tokens, N, norm):
    score = {}
    [query_tfidf,
     query_norm] = generateTfIdfSquareQuery(query_tf, invertedindex_tokens, N)

    if len(query_tfidf) == 0:
        return score
    docs_tfidf = generateTfIdfQueryDocs(query_tokens, invertedindex_tokens, N)
    norms = norm

    for doc in docs_tfidf:
        score[doc] = [0, (docs_tfidf[doc][1][0], docs_tfidf[doc][1][1])]
        for token in query_tokens:
            try:
                score[doc][0] += query_tfidf[token] * docs_tfidf[doc][0][token]

            except:
                continue
    for doc in docs_tfidf:
        length = (norms[doc] * query_norm)
        if length.real > 0.0:
            score[doc][0] = score[doc][0] / length
    sort_orders = sorted(score.items(), key=lambda x: x[1][0], reverse=True)
    return sort_orders
