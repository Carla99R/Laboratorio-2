import sys

import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json

import Suscriptor


def vaciar(indicador):
    mean = 10
    std = 5
    capacity = int(np.random.normal(mean, std))
    indicador -= int(capacity)
    return indicador


def llenar(indicador):
    mean = 20
    std = 5
    capacity = int(np.random.normal(mean, std))

    indicador += int(capacity)
    return indicador


def reportar(indicador, tiempo):
    client = paho.mqtt.client.Client("nivel_tanque", False)
    client.qos = 0
    client.connect(host='localhost')

    alertL = "Queda la mitad o menos de agua"
    alertN = "Se acabo el agua"

    if indicador <= 50:
        payload = {
            "reporte": indicador,
            "alerta": alertL
        }
        item = {
            "data": str("Cantidad agua: " + str(indicador) + " " + "Alerta: " + alertL + " " + "Tiempo: " + str(tiempo))
        }

        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(6, %(data)s);"""
        dataBase(query, item, client, payload)

    if indicador == 0:
        payload = {
            "reporte": indicador,
            "alerta": alertN
        }
        item = {
            "data": str("Cantidad agua: " + str(indicador) + " " + "Alerta: " + alertN + " " + "Tiempo: " + str(tiempo))
        }
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(6, %(data)s);"""
        dataBase(query, item, client, payload)


def dataBase(query, item, client, payload):
    client.publish('casa/baño/nivel_tanque', json.dumps(payload), qos=0)
    Suscriptor.on_connect_db(query, item)


def main():
    indicador = 100
    variable = time.time()
    variable2 = time.time()
    while True:
        res = int(variable - variable2)
        if res % 600 == 0:
            indicador = vaciar(indicador)
            reportar(indicador, res)
        if res % 1800 == 0:
            indicador = llenar(indicador)
        time.sleep(1)
        variable = time.time()


if __name__ == '__main__':
    main()
    sys.exit(0)
