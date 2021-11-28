##########################################################################
# IMPORTAR LIBRERIAS #####################################################

import pandas as pd
import numpy as np
import plotly.express as px

import psycopg2
import boto3
import random
import requests

from dash import Dash, dcc, html
from PIL import Image
from dash.dependencies import Input, Output, State


##########################################################################
# BLOQUE PRINCIPAL DE INSTRUCCIONES ######################################


# Servicio SNS AWS
sns = boto3.resource('sns')
topic = sns.Topic(arn = 'arn:aws:sns:us-east-1:150839082595:Proyecto4CN_OV_Comments')


# Base de datos DynamoDB
dynamodb = boto3.resource('dynamodb')
table1 = dynamodb.Table('Proyecto4CN_OV_Players')
table2 = dynamodb.Table('Proyecto4CN_OV_Comments')


# Base de datos PostgreSQL con Docker
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

    query1 = 'SELECT Nationality, Overall FROM player'
    query2 = 'SELECT PreferredFoot FROM player'
    query3 = 'SELECT Name, Overall, League FROM team ORDER BY Overall DESC'
    query4 = 'SELECT Name, Overall FROM player'

    out1 = pd.read_sql_query(query1, engine)
    out2 = pd.read_sql_query(query2, engine)
    out3 = pd.read_sql_query(query3, engine)
    out4 = pd.read_sql_query(query4, engine).sort_values(by = ['overall'], ascending = False).iloc[:1000]

    print('Consultas Realizadas...')

    print("\nDisconnecting...")
except(Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)
finally:
    if engine is not None:
        engine.close()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Fifa 22 Teams and Players'
server = app.server


# Graficas importantes de la pagina
fig1 = px.scatter(out1, x = 'nationality', y = 'overall', color = 'overall', title = 'For the Players, Nationality vs Overall')
fig2 = px.pie(out2, names = 'preferredfoot', title = 'For the players, PreferredFoot Count (Total: {0})'.format(out2.shape[0]))
fig3 = px.scatter(out3.iloc[:70], x = 'name', y = 'overall', color = 'league', title = 'For the Teams, Name VS Overall (The best 70 group by League)')


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


txt_fifa = open('FIFA.txt')
txt1 = open('Graph1.txt')
txt2 = open('Graph2.txt')
txt3 = open('Graph3.txt')

tf = txt_fifa.read().split('\n')
t1 = txt1.read()
t2 = txt2.read()
t3 = txt3.read()


# Cargar la capa de la aplicacion web
app.layout = html.Div(style = {'backgroundColor': colors['background']}, children = [
    html.Br(),

    html.H1(children = '\n Fifa 22 Teams and Players.', style = {
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(children = 'A web board of three graphics made with Dash in Python (PostgresDB in Docker).', style = {
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Br(),

    html.P(children = tf[0], style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.P(children = tf[2], style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.P(children = tf[4], style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.P(children = tf[6], style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.P(children = tf[8], style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.Br(),

    dcc.Graph(
        id = 'NationalityVSoverall',
        figure = fig1
    ),

    html.Br(),

    html.P(children = t1, style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.Br(),

    dcc.Graph(
        id = 'preferredFootCount',
        figure = fig2
    ), 

    html.Br(),

    html.P(children = t2, style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.Br(),

    dcc.Graph(
        id = 'teamNameVSoverall',
        figure = fig3
    ),

    html.Br(),

    html.P(children = t3, style = {
        'textAlign': 'left',
        'color': colors['text']
    }),

    html.Br(),
    html.Br(),
    html.Br(),

    html.P(
        children = 'Enter a player name to see his information and photo.',
        style = {
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.P(
        children = "Suggestions: " + ', '.join(list(out4['name'])[:100]) + '...',
        style = {
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Br(),

    html.P(
        children = 'Player:',
        style = {
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Div(
        dcc.Input(
            id = 'my_input1',
            type = 'text',
            debounce = True,
            pattern = r'^[A-Za-z].*',
            spellCheck = True,
            inputMode = 'latin',
            name = 'text'
        )
    ),

    html.Br(),

    html.Button(
        'Consult', 
        id = 'my_button1', 
        n_clicks = 1,
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Br(),

    html.Div(
        id = 'my_output1',
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Br(),
    html.Br(),
    html.Br(),

    html.P(
        children = "If you have comments regarding the content of this page, write them below and we will work to improve your experience.",
        style = {
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Br(),

    html.P(
        children = "Username:",
        style = {
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Div(
        dcc.Input(
            id = 'my_input2',
            type = 'text',
            debounce = True,
            pattern = r'^[A-Za-z].*',
            spellCheck = True,
            inputMode = 'latin',
            name = 'text'
        )
    ),

    html.P(
        children = "Comment:",
        style = {
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Div(
        dcc.Input(
            id = 'my_input3',
            type = 'text',
            debounce = True,
            pattern = r'^[A-Za-z].*',
            spellCheck = True,
            inputMode = 'latin',
            name = 'text'
        )
    ),

    html.Br(),

    html.Button(
        'Send', 
        id = 'my_button2', 
        n_clicks = 1,
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Br(),

    html.Div(
        id = 'my_output2',
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Br(),
    html.Br(),

    html.Button(
        'More', 
        id = 'my_button3', 
        n_clicks = 1,
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Br(),

    html.Div(
        id = 'my_output3',
        style = {
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Br()
])


# Callback para mostrar info de los jugadores
@app.callback(
    Output('my_output1', 'children'),
    Input('my_button1', 'n_clicks'),
    State('my_input1', 'value')
)
def update_output1(n_clicks, value):
    engine = psycopg2.connect(
        database = "proyecto3cn_db",
        user = "postgres",
        password = "adminpostgres",
        host = "184.72.170.105",
        port = "5432"
    )
    query = "SELECT id FROM player where name = '{0}'".format(value)
    out = pd.read_sql_query(query, engine)
    engine.close()
    if(n_clicks != 1):
        if(out.empty):
            return 'Player Not Found'
        else:
        # print(out.head())
            response = table1.get_item(
                Key = {
                    'player_name': value,
                    'player_id': int(list(out.iloc[0])[0])
                }
            )
            item = response['Item']

            msg1 = 'The player is: {0}'.format(item['player_name'])
            msg2 = 'His age is: {0}'.format(item['player_age'])
            msg3 = 'His overall is: {0}'.format(item['player_overall'])
            msg4 = 'His club is: {0}'.format(item['player_club'])
            msg5 = 'His national team is: {0}'.format(item['player_nationalteam'])
            fig4 = px.imshow(Image.open(requests.get(item['player_photourl'], stream = True).raw), title = item['player_name'])
            fig4.update_layout(
                plot_bgcolor=colors['background'],
                paper_bgcolor=colors['background'],
                font_color=colors['text'],
                xaxis_visible=False,
                yaxis_visible=False
            )
            return html.Div(
                children = [
                    html.Br(),

                    html.P(
                        children = msg1
                    ),
                    html.P(
                        children = msg2
                    ),
                    html.P(
                        children = msg3
                    ),
                    html.P(
                        children = msg4
                    ),
                    html.P(
                        children = msg5
                    ),

                    html.Br(),

                    dcc.Graph(
                        id = 'player_image',
                        figure = fig4
                    ),

                    html.P(
                        children = 'Sorry for the images quality :(.'
                    )

                ],
                style = {
                    'textAlign': 'center',
                    'color': colors['text']
                }
            )


# Callback para realizar comentarios 
@app.callback(
    Output('my_output2', 'children'),
    Input('my_button2', 'n_clicks'),
    State('my_input2', 'value'),
    State('my_input3', 'value')
)
def update_output2(n_clicks, value1, value2):
    txt4 = open('n_comments.txt', 'r')
    idx = int(txt4.read())
    txt4.close()
    if(n_clicks != 1):
        if(value1 != None and value2 != None):
            msg = 'Message from FIFA 22 PLAYERS AND TEAMS APP: \n\n'
            msg += 'Username: {0} \n'.format(value1)
            msg += 'Comment: {0} \n\n'.format(value2)
            msg += 'Duplied in DynamoDB. '
            topic.publish(Message = msg)
            idx += 1
            table2.put_item(
                Item = {
                    'comment_id': idx,
                    'username': value1,
                    'comment': value2
                }
            )
            txt4 = open('n_comments.txt', 'w')
            txt4.write(str(idx))
            txt4.close()
            return 'Thanks for your commentary {0}!'.format(value1)
        else:
            return 'Please, the fields must be not null.'


# Callback para mostrar algunos comentarios
@app.callback(
    Output('my_output3', 'children'),
    Input('my_button3', 'n_clicks'),
)
def update_output3(n_clicks):
    if(n_clicks != 1):
        txt4 = open('n_comments.txt', 'r')
        idx = int(txt4.read())
        txt4.close()
        msgs = []
        for i in random.sample(range(1, idx + 1), 5):
            # print(i)
            response = table2.get_item(
                Key = {
                    'comment_id': i
                }
            )
            item = response['Item']
            msgs.append('{0}: {1}'.format(item['username'], item['comment']))
        return html.Div(
            children = [
                html.Br(),

                html.H2(
                    children = "Comments"
                ),

                html.P(
                    children = msgs[0]
                ),
                html.P(
                    children = msgs[1]
                ),
                html.P(
                    children = msgs[2]
                ),
                html.P(
                    children = msgs[3]
                ),
                html.P(
                    children = msgs[4]
                ),

                html.Br()
            ],
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        )


if(__name__ == '__main__'):
    app.run_server(debug = True)
