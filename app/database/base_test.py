import os
from unittest import TestCase

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
 


class BaseTest(TestCase):
    pass


def copy_database_with_pg_dump(target_db_params):
    print("*" * 100)
    print("copiando base de datos ")
    print("*" * 100)
    try: 
        conn = psycopg2.connect(
            dbname="fake_database",
            user="postgres",
            password="postgres",
            host=target_db_params[
                "host"
            ],  
            port=target_db_params["port"],
        )
        cur = conn.cursor()
        conn.autocommit = True 

        copy_db_sql = sql.SQL("CREATE DATABASE {} TEMPLATE fake_database").format(
            sql.Identifier(target_db_params["dbname"])
        )
        cur.execute(copy_db_sql)
        conn.commit()
        cur.close()
        conn.close()
        print("Base de datos copiada exitosamente.")
    except Exception as e:
        print(f"No se pudo copiar la base de datos: {e}")


def init_testing(function_name):
    # Este se ejecuta una sola vez al inicio de la clase no al inicio de cada test

    load_dotenv(dotenv_path=".env") 
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_HOST_WRITER"] = "localhost"
    os.environ["DB_HOST_READ"] = "localhost"
    os.environ["DB_PORT"] = "5432" 
    database_name = f"{function_name}_test"
    os.environ["SECRET_KEY"] = "secret_key" 
    os.environ["FUNCTION_NAME"] = function_name
    os.environ["ENVIRONMENT"] = "unit_test"
    os.environ["DB_NAME"] = database_name   
    copy_database_with_pg_dump(
        {
            "host": os.environ["DB_HOST"],
            "dbname": database_name,
            "user": "postgres",
            "password": "postgres",
            "port": os.environ["DB_PORT"],
        }
    ) 