import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json

import DataBase


def vaciar(indicador):
    mean = 0.10
    std = 0.05
    capacity = np.random.normal(mean, std)

    indicador -= capacity


def llenar(indicador):
    mean = 0.20
    std = 0.05
    capacity = np.random.normal(mean, std)

    indicador += capacity


def reportar(indicador):
    client = paho.mqtt.client.Client("nivel_tanque", False)
    client.qos = 0
    client.connect(host='localhost')

    alertL = "Queda la mitad o menos de agua"
    alertN = "Se acabó el agua"

    if indicador <= 50:
        payload = {
            "cantidad_agua": indicador,
            "alerta": alertL
        }

    if indicador == 0:
        payload = {
            "cantidad_agua": indicador,
            "alerta": alertN
        }
    item = {
        "data": str("Cantidad agua: " + payload['cantidad_agua'] + " " + "Alerta: " + payload['alerta'])
    }

    client.publish('casa/cocina/temperatura_olla', json.dumps(payload), qos=0)
    query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(6, %(data)s);"""
    DataBase.on_connect_db(query, item)


def main():
    indicador = 100
    variable = time.time()
    variable2 = time.time()
    while True:
        res = int(variable - variable2)
        if res % 600 == 0:
            vaciar(indicador)
            reportar(indicador)
        if res % 1800 == 0:
            llenar(indicador)
        time.sleep(1)
        variable = time.time()


if __name__ == '__main__':
    main()
