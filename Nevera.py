import sys
import paho.mqtt.client
import paho.mqtt.publish
import time
import numpy as np
import json
import Suscriptor


def on_connect(client, userdata, flags, rc):
    print('conectado publicador')


def main():
    client = paho.mqtt.client.Client("temperatura_nevera", False)
    client.qos = 0
    client.connect(host='localhost')

    meanGrades = 10
    stdGrades = 2

    inferior = 0
    superior = 10

    variable = time.time()
    variable2 = time.time()
    while True:
        res = int(variable - variable2)

        temperature = int(np.random.normal(meanGrades, stdGrades))
        ice = int(np.random.uniform(inferior, superior))

        if res % 300 == 0:
            payload = {
                "reporte": temperature,
                "tiempo": res
            }
            item = {
                "data": str("Reporte: " + str(temperature) + " " + "Tiempo: " + str(res))
            }
            client.publish('casa/cocina/temperatura_nevera', json.dumps(payload), qos=0)
            query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(1, %(data)s);"""
            Suscriptor.on_connect_db(query, item)

        if res % 600 == 0:
            payload = {
                "reporte": temperature,
                "hielo": ice,
                "tiempo": res
            }
            item = {
                "data": str("Reporte: " + str(temperature) + " " + "Capacidad hielo: " + str(ice) + " " + "Tiempo: " + str(res))
            }
            client.publish('casa/cocina/temperatura_nevera', json.dumps(payload), qos=0)
            query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(2, %(data)s);"""
            Suscriptor.on_connect_db(query, item)
        time.sleep(1)
        variable = time.time()


if __name__ == '__main__':
    main()
    sys.exit(0)
