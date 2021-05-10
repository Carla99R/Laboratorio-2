import json
import sys

import requests
import time
import paho.mqtt.client
import paho.mqtt.publish

import Suscriptor


def main():
    client = paho.mqtt.client.Client("alexa_echo", False)
    client.qos = 0
    client.connect(host='localhost')

    variable = time.time()
    variable2 = time.time()
    while True:
        res = int(variable - variable2)
        complete_url = "http://api.openweathermap.org/data/2.5/weather?lat=10.491&lon=-66.902&appid=0c16fe21b93a1d6f05e452e746e12403"

        response = (requests.get(complete_url)).json()

        if response["cod"] != "404":

            data = response["main"]

            current_temperature = data["temp"]

        else:
            print(" Ciudad no encontrada")

        payload = {
            "reporte": current_temperature,
            "tiempo": res
        }

        item = {
            "data": str("Reporte: " + str(current_temperature)+"K" + " " + "Tiempo: " + str(res))
        }

        client.publish('casa/sala/alexa_echo', json.dumps(payload), qos=0)
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(5, %(data)s);"""
        Suscriptor.on_connect_db(query, item)
        time.sleep(300)
        variable = time.time()


if __name__ == '__main__':
    main()
    sys.exit(0)
