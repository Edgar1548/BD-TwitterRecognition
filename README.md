# BDproyect

## Integrantes:
-Edgar Chacón 
-Paulo Cuaresma

## Introducción:
Utec search

Nuestro proyecto es capaz de realizar consultas a una cantidad de 479945 twitts que han sido recompilados anteriormente.

## Fronted:
Vista del FrontEnd:

El FrontEnd se implemento con React, y debido a que el programa se basa en hacer una consulta dado 2 parametro no hay mucho que resaltar excepto por la función que se encarga de eso:




## Backend:
El Backend de deasrrollo en python, usando Flask, SQLAlchemy.

Dentro del backend primero se debe ejecutar la función pre_app, que se encargara de llenar la data en nuestra base de datos, asi como tambien de guardar en archivos .json el norm de cada documento, y tambien el indexinverted.

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


## Video:
