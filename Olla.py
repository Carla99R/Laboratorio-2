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
            if temperature >= 100:
                item = {
                    "data": str("Reporte: " + str(temperature) + " " + "Mensaje: " + str(message) + " " + "Tiempo: " + str(res))
                }
                payload = {
                    "reporte": temperature,
                    "mensaje": message,
                    "tiempo": res,
                    "item": item
                }

            else:
                item = {
                    "data": str("Reporte: " + str(temperature) + " " + "Tiempo: " + str(res))
                }
                payload = {
                    "reporte": temperature,
                    "tiempo": res,
                    "item": item
                }

            client.publish('casa/cocina/temperatura_olla', json.dumps(payload), qos=0)
        time.sleep(1)
        variable = time.time()


if __name__ == '__main__':
    main()
    sys.exit(0)
