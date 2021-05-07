import sys

import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json

import DataBase


def main():
    client = paho.mqtt.client.Client("temperatura_olla", False)
    client.qos = 0
    client.connect(host='localhost')

    inferior = 0
    superior = 150
    temperature = np.random.uniform(inferior, superior)
    message = "El agua ya hirvió"

    while True:
        random = np.random.randint(0, 1)
        if random == 1:
            if int(temperature) == 100:
                payload = {
                    "temperatura": str(temperature),
                    "mensaje": message
                }
                item = {
                    "data": str("Temperatura: " + str(temperature) + " " + "Mensaje: " + message)
                }
                query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(3, %(data)s);"""
            else:
                payload = {
                    "temperatura": str(temperature)
                }
                item = {
                    "data": str("Temperatura: " + str(temperature))
                }
                query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(3, %(data)s);"""

            client.publish('casa/cocina/temperatura_olla', json.dumps(payload), qos=0)
            DataBase.on_connect_db(query, item)
        time.sleep(1)


if __name__ == '__main__':
    main()
    sys.exit(0)
