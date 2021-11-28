import boto3
import psycopg2
import pandas as pd


# Base de datos en Dynamo
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Proyecto4CN_OV_Players')
# print(table.creation_date_time)


# Base de Datos con Docker
engine = None
resultDataFrame = None
try:
    print("Connecting...\n")

    engine = psycopg2.connect(
        database = "proyecto3cn_db",
        user = "postgres",
        password = "adminpostgres",
        host = "184.72.170.105",
        port = "5432"
    )
    cursorDB = engine.cursor()

    query = 'SELECT id, name, age, overall, club, nationalteam, photourl FROM player'
    out = pd.read_sql_query(query, engine).sort_values(by = ['overall'], ascending = False).iloc[:1000]

    # print(out.head())
    # print(out.shape)

    print('Insertando a DynamoDB...')
    
    for i in range(out.shape[0]):
        fila = list(out.iloc[i])
        table.put_item(
            Item = {
                'player_name': str(fila[1]),
                'player_id': int(fila[0]),
                'player_age': int(fila[2]),
                'player_overall': int(fila[3]),
                'player_club': str(fila[4]),
                'player_nationalteam': str(fila[5]),
                'player_photourl': str(fila[6])
            }
        )

    print("\nDisconnecting...")
except(Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)
finally:
    if engine is not None:
        engine.close()