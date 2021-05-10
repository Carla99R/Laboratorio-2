import sys

import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json

import Suscriptor


def main():
    client = paho.mqtt.client.Client("contador_persona", False)
    client.qos = 0
    client.connect(host='localhost')

    inferior = 0
    superior = 10
    alert = "Hay mas de 5 personas en la sala"

    variable = time.time()
    variable2 = time.time()
    while True:
        cant_personas = int(np.random.uniform(inferior, superior))
        res = int(variable - variable2)
        if cant_personas > 5:
            item = {
                "data": str("Reporte: " + str(cant_personas) + " " + "Alerta: " + alert + " " + "Tiempo: " + str(res))
            }
            payload = {
                "reporte": cant_personas,
                "alerta": alert,
                "tiempo": res,
                "item": item
            }

        else:
            item = {
                "data": str("Reporte: " + str(cant_personas) + " " + "Tiempo: " + str(res))
            }
            payload = {
                "reporte": cant_personas,
                "tiempo": res,
                "item": item
            }

        client.publish('casa/sala/contador_persona', json.dumps(payload), qos=0)
        time.sleep(60)
        variable = time.time()


if __name__ == '__main__':
    main()
    sys.exit(0)
