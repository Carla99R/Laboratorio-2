import sys
import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json
import DataBase


def on_connect(client, userdata, flags, rc):
    print('conectado publicador')


def neveraT():
    client = paho.mqtt.client.Client("temperatura_nevera", False)
    client.qos = 0
    client.connect(host='localhost')

    meanGrades = 10
    stdGrades = 2
    temperature = np.random.normal(meanGrades, stdGrades)

    while True:
        payload = {
            "temperatura_nevera": str(temperature)
        }
        item = {
            "data": str("Temperatura: " + str(temperature))
        }
        client.publish('casa/cocina/temperatura_nevera', json.dumps(payload), qos=0)
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(1, %(data)s);"""
        DataBase.on_connect_db(query, item)
        print(payload)
        time.sleep(300)


def neveraI():
    client = paho.mqtt.client.Client("temperatura_nevera", False)
    client.qos = 0
    client.connect(host='localhost')

    inferior = 0
    superior = 10
    ice = np.random.uniform(inferior, superior)

    while True:
        payload = {
            "capacidad_hielo_nevera": str(ice)
        }
        item = {
            "data": str("Capacidad hielo: " + str(ice))
        }
        client.publish('casa/cocina/temperatura_nevera', json.dumps(payload), qos=0)
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(2, %(data)s);"""
        DataBase.on_connect_db(query, payload)
        time.sleep(600)


def main():
    variable = time.time()
    variable2 = time.time()
    while True:
        res = int(variable - variable2)
        if res % 300 == 0:
            neveraT()
        if res % 600 == 0:
            neveraI()
        time.sleep(1)
        variable = time.time()


if __name__ == '__main__':
    main()
    sys.exit(0)
