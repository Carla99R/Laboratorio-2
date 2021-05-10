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


def main():
    client = paho.mqtt.client.Client(client_id='carla-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='127.0.0.1', port=1883)
    client.loop_forever()


if __name__ == '__main__':
    main()
    sys.exit(0)
