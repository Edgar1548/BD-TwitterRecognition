from generate_tokens import generateStopFile
from invertedindex import generateIndexInv, generateNorm
from app_sql import charge_data, create_index, create_update_tsvector
import params


def preapp_static():
    #cleaning static data
    #clean_data(params.static_path_folder, params.static_path_clean)

    #generate_data_tosql
    charge_data(params.static_path_clean)
    create_update_tsvector()
    create_index()

    #generate stopwords
    stop_words = generateStopFile(params.stoplist_file)

    #generate and save IndexInv
    N = generateIndexInv(params.static_path_clean, stop_words, 'spanish',
                         params.index_path)
    #generate and save Norm
    generateNorm(params.index_path, N, params.norm_path)


#preapp_static()