import psycopg2
import pandas as pd

engine = None
resultDataFrame = None
try:
    print("Connecting...\n")

    engine = psycopg2.connect(
        database = "proyecto3cn_db",
        user = "postgres",
        password = "adminpostgres",
        host = "54.146.133.130",
        port = "5432"
    )
    cursorDB = engine.cursor()

    print('Insertando a Tablas...')

    file = open('full_tables.sql', 'r')
    lines = file.readlines()
    for l in lines:
        if(len(l) > 5):
            cursorDB.execute(l)
    
    file.close()
    engine.commit()

    print("\nDisconnecting...")
except(Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)
finally:
      if engine is not None:
          engine.close()
