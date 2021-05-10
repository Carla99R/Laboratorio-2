import sys

import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json

import Suscriptor


def main():
    client = paho.mqtt.client.Client("temperatura_olla", False)
    client.qos = 0
    client.connect(host='localhost')

    inferior = 0
    superior = 150
    message = "El agua ya hirvio"

    variable = time.time()
    variable2 = time.time()
    while True:
        temperature = int(np.random.uniform(inferior, superior))
        res = int(variable - variable2)
        random = np.random.randint(0, 2)
        if random == 1:
            if int(temperature) >= 100:
                payload = {
                    "reporte": temperature,
                    "mensaje": message,
                    "tiempo": res
                }
                item = {
                    "data": str("Reporte: " + str(temperature) + " " + "Mensaje: " + str(message) + " " + "Tiempo: " + str(res))
                }
                query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(3, %(data)s);"""
            else:
                payload = {
                    "reporte": temperature,
                    "tiempo": res
                }
                item = {
                    "data": str("Reporte: " + str(temperature) + " " + "Tiempo: " + str(res))
                }
                query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(3, %(data)s);"""

            client.publish('casa/cocina/temperatura_olla', json.dumps(payload), qos=0)
            Suscriptor.on_connect_db(query, item)
        time.sleep(1)
        variable = time.time()


if __name__ == '__main__':
    main()
    sys.exit(0)
