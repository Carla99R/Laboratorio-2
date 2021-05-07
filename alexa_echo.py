import json
import sys

import requests
import time
import paho.mqtt.client
import paho.mqtt.publish

import DataBase


def main():
    client = paho.mqtt.client.Client("alexa_echo", False)
    client.qos = 0
    client.connect(host='localhost')

    while True:

        complete_url = "http://api.openweathermap.org/data/2.5/weather?lat=10.491&lon=-66.902&appid=0c16fe21b93a1d6f05e452e746e12403"

        response = (requests.get(complete_url)).json()

        if response["cod"] != "404":

            data = response["main"]

            current_temperature = data["temp"]
            current_pressure = data["pressure"]
            current_humidity = data["humidity"]

        else:
            print(" Ciudad no encontrada")

        payload = {
            "temperatura": str(current_temperature),
            "presion": str(current_pressure),
            "humedad": str(current_humidity)
        }

        item = {
            "data": str("temperatura: " + str(current_temperature) + " " + "presion: " + str(current_pressure) + " " + "humedad: " + str(current_humidity))
        }

        client.publish('casa/sala/alexa_echo', json.dumps(payload), qos=0)
        query = """INSERT INTO suscripciones(tipo_suscripcion_id, suscripcion) VALUES(5, %(data)s);"""
        DataBase.on_connect_db(query, item)
        time.sleep(300)


if __name__ == '__main__':
    main()
    sys.exit(0)
