import json


def writeJsonData(path, data_json):
    File_out = open(path, "w", encoding="utf-8")
    File_out.write(json.dumps(data_json, ensure_ascii=False))
    File_out.close()


def readJsonData(path):
    decode_file = open(path, "r", encoding="utf-8")
    tweets = json.load(decode_file)
    decode_file.close()
    return tweets