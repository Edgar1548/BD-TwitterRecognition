import json
import psycopg2
import consult_main
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
#from app_static import consult_static

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Residente1548@localhost/bdproyect2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

type_query = "static"


@app.route('/api', methods=['GET'])
def index():
    return {'name': 'Hello World'}


@app.route('/api/change_data')
def change():
    global type_query
    type_query = ("twitter", "static")[type_query == "twitter"]


@app.route('/api/consult', methods=['POST'])
def consult():
    global type_query
    request_data = json.loads(request.data)
    consult = request_data['consult']
    topk = int(request_data['topk'])
    if (type_query == "static"):
        data = consult_main.consult_topk(type_query, consult, topk)
        return data
    return {'201': "isOk"}


if __name__ == '__main__':
    app.run(debug=True)


class Twiitts(db.Model):
    __tablename__ = 'twitts'
    id = db.Column(db.Integer, primary_key=True)
    id_tweet = db.Column(db.String(35))
    text = db.Column(db.Text)
    date = db.Column(db.String(50))
    user = db.Column(db.String(50))
    content_ts = db.Column(db.Text)

    def __init__(self, id_tweet, text, date, user, content_ts):
        self.id_tweet = id_tweet
        self.text = text
        self.date = date
        self.user = user
        self.content_ts = content_ts
