# BDproyect

## Integrantes:
| Edgar Chacon| Paulo Cuaresma|
| ----- | ---- |
| Backend + Functional Front End| Template Frontend + video + funcion de clean data inicial |

## Introducción:
Utec search

Nuestro proyecto es capaz de realizar consultas a una cantidad de 479945 twitts que han sido recompilados anteriormente.

## Fronted:
Vista del FrontEnd:![a](https://user-images.githubusercontent.com/66433825/173174346-12602b55-e706-4c97-aa06-25a072d2bcf7.jpg)


El FrontEnd se implemento con React, y debido a que el programa se basa en hacer una consulta dado 2 parametro no hay mucho que resaltar excepto por la función que se encarga de eso:


``` javascript 
const handleSubmit = (event) => {
    event.preventDefault()
    fetch("/api/consult", {
      method: "POST",
      body: JSON.stringify({
        consult: listofInputs.consult,
        topk: listofInputs.topk,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        onInputsSubmit(data);
      });
  };

```


## Backend:
El Backend de deasrrollo en python, usando Flask, SQLAlchemy.
Dentro del Backend las funciones principales que se deben tener en cuenta son consultStatic y staticConsultSql, que se encargar de realizar las consultas:
``` python 
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
```
``` python 
def staticConsultSql(query, topk):
    languaje = 'spanish'
    token_query_text = ' '.join([str(item) for item in query])
    token_query_text_clean = token_query_text.replace(' ', ' | ')
    consult = f"select id_tweet, text, date, twitts.user, ts_rank_cd(text_ts, query_ts) as score from twitts, to_tsquery('{languaje}', '{token_query_text_clean}') query_ts where query_ts @@ text_ts order by score desc limit {topk};"
    data = app.db.engine.execute(consult)
    data_map = {}
    for i in data:
        data_map[i[0]] = [i[1], i[2], i[3], round(i[4], 5)]

    return data_map
```


## Ejecucion del programa
Primero debera crear la base de datos, para ello es puede ejecutar los siguientes comandos en orden dentro de una terminal de python:
```python 
from app import db
db.create_all()
```

Luego se debe ejecutar la función pre_app, que se encargara de llenar la data en nuestra base de datos, asi como tambien de guardar en archivos .json el norm de cada documento, y crear y guardar el indexinverted.



``` python 
def preapp_static():
    clean_data(params.static_path_folder, params.static_path_clean)

    charge_data(params.static_path_clean)
    create_update_tsvector()
    create_index()

    stop_words = generateStopFile(params.stoplist_file)

    N = generateIndexInv(params.static_path_clean, stop_words, 'spanish',
                         params.index_path)
    generateNorm(params.index_path, N, params.norm_path)
```

Tambien se debe cambiar a la base de datos donde quiere que se cree:
```
app.config['SQLALCHEMY_DATABASE_URI'] 
```


Una vez se haya ejecutado pre_consult ya se puede ejecutar los comandos que serviran tanto para poder empezar el backend y frontend:
### FrontEnd
``` 
npm start
```
### Backend
```
py app.py
```




## Video:
https://youtu.be/BgBZyesfh4s
