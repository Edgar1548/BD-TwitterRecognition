from generate_tokens import clean, generateTokens
import app
import os
from memoriasec import readJsonData
from ntpath import join
import time


def charge_data(data_path):
    data_files = os.listdir(data_path)
    for file in data_files:
        tweets = readJsonData(join(data_path, file))
        for tweet in tweets:
            id = tweet['id']
            text = tweet['text']
            date = tweet['date']
            user = tweet['user']
            content_ts = clean(text.lower())
            tweet = app.Twiitts(id, text, date, user, content_ts)
            app.db.session.add(tweet)
    app.db.session.commit()


def create_update_tsvector():
    create = 'alter table twitts add column text_ts tsvector;'
    languaje = 'spanish'
    update = f"update twitts set text_ts = x.text_ts from (select id_tweet,to_tsvector('{languaje}', content_ts) as text_ts from twitts ) as x where x.id_tweet = twitts.id_tweet;"
    app.db.engine.execute(create)
    app.db.engine.execute(update)


def create_index():
    app.db.engine.execute(
        'create index idx_text on twitts using gin (text_ts);')


def staticConsultSql(query, topk):
    languaje = 'spanish'
    token_query_text = ' '.join([str(item) for item in query])
    token_query_text_clean = token_query_text.replace(' ', ' | ')
    consult = f"select id_tweet, text, date, twitts.user, ts_rank(text_ts, query_ts) as score from twitts, to_tsquery('{languaje}', '{token_query_text_clean}') query_ts where query_ts @@ text_ts order by score desc limit {topk};"
    data = app.db.engine.execute(consult)
    data_map = {}
    for i in data:
        data_map[i[0]] = [i[1], i[2], i[3], round(i[4], 5)]

    return data_map