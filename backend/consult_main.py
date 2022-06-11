import app_static
import app_sql
import params
from generate_tokens import generateStopFile, generateTokens
import time


def consult_topk(type, query, topk, indexinv):
    if (type == "static"):
        stop_words = generateStopFile(params.stoplist_file)
        query_tokens = generateTokens(query, stop_words, "spanish")

        start_time = time.time()
        result_static = app_static.consultStatic(query_tokens, topk, indexinv)
        time_static = round(time.time() - start_time, 5)

        start_time = time.time()
        result_sql = app_sql.staticConsultSql(query_tokens, topk)
        time_sql = round(time.time() - start_time, 5)

        return {
            'data': result_static,
            'data_sql': result_sql,
            'time': time_static,
            'times_sql': time_sql
        }

    return {'Error': "Something fail"}

