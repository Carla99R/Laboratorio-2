import sys
import paho.mqtt.client
import psycopg2
from psycopg2 import Error
import json
from queue import Queue


def on_connect_db(query, item):
    try:
        connection = psycopg2.connect(user="ioqvfjqb", password="2JPre4f6MfVT-ZxL9XCYVFhBlMhBN5W0",
                                      host="queenie.db.elephantsql.com", database="ioqvfjqb")
        cursor = connection.cursor()
        cursor.execute(query, item)
        connection.commit()
        print("Insert realizado con éxito")

    except(Exception, Error) as e:
        print("Error al conectar con la base de datos", e)
    except(Exception, psycopg2.Error) as e:
        print("Error al fetching la data de PostgreSQL", e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def on_connect(client, userdata, flags, rc):
    print('connected (%s)' % client._client_id)
    client.subscribe(topic='casa/#', qos=2)


def on_message(client, userdata, message):
    print('------------------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print('qos: %d' % message.qos)
    content = message.payload
    jsondecoded = json.loads(content.decode('utf-8'))
    query = crear_query(message.topic)
    on_connect_db(query, jsondecoded["item"])


def crear_query(topic):
    query = """"""
    if topic == "casa/cocina/temperatura_nevera":
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(1, %(data)s);"""
    if topic == "casa/cocina/temperatura_olla":
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(2, %(data)s);"""
    if topic == "casa/sala/contador_personas":
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(3, %(data)s);"""
    if topic == "casa/sala/alexa_echo":
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(4, %(data)s);"""
    if topic == "casa/baño/nivel_tanque":
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(5, %(data)s);"""

    return query


def main():
    client = paho.mqtt.client.Client(client_id='carla-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='127.0.0.1', port=1883)
    client.loop_forever()


if __name__ == '__main__':
    main()
    sys.exit(0)
