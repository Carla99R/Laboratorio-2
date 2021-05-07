import sys

import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json

import DataBase


def main():
    client = paho.mqtt.client.Client("contador_persona", False)
    client.qos = 0
    client.connect(host='localhost')

    inferior = 0
    superior = 10
    cant_personas = np.random.uniform(inferior, superior)
    alert = "Hay más de 5 personas en la sala"

    while True:
        if int(cant_personas) > 5:
            payload = {
                "cantidad_personas": str(cant_personas),
                "alerta": alert
            }
            item = {
                "data": str("Cantidad personas: " + str(cant_personas) + " " + "Alerta: " + alert)
            }
            query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(4, %(data)s);"""
        else:
            payload = {
                "cantidad_personas": str(cant_personas)
            }
            item = {
                "data": str("Cantidad personas: " + str(cant_personas))
            }
            query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(4, %(data)s);"""

        client.publish('casa/sala/contador_persona', json.dumps(payload), qos=0)
        DataBase.on_connect_db(query, item)
        time.sleep(60)


if __name__ == '__main__':
    main()
    sys.exit(0)
