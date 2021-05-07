import psycopg2
from psycopg2 import Error


def on_connect_db(query, item):
    try:
        connection = psycopg2.connect(user="ioqvfjqb", password="2JPre4f6MfVT-ZxL9XCYVFhBlMhBN5W0", host="queenie.db.elephantsql.com", database="ioqvfjqb")
        cursor = connection.cursor()
        cursor.execute(query, item)
        connection.commit()
        print("Insert realizado con éxito")

    except(Exception, Error) as e:
        print("Error al conectar con la base de datos", e)
    except(Exception, psycopg2.Error) as e:
        print("Error al fetching la data de PostgreSQL", e)
    finally:
        if connection:
            cursor.close()
            connection.close()
