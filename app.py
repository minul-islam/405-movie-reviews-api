import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from helpers.key_finder import api_key
from helpers.api_call import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import requests

#from bs4 import BeautifulSoup
#import json
#from pandas.json import json_normalize

########### Define a few variables ######

tabtitle = 'Movies'
sourceurl = 'https://www.kaggle.com/tmdb/tmdb-movie-metadata'
sourceurl2 = 'https://developers.themoviedb.org/3/getting-started/introduction'
githublink = 'https://github.com/farkasdilemma/405-movie-reviews-api'

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    dcc.Store(id='tmdb-store', storage_type='session'),
    dcc.Store(id='summary-store', storage_type='session'),
    html.Div([
        html.H1(['Movie Reviews']),
        html.Div([
            html.Div([
                html.Div('Randomly select a movie summary'),
                html.Button(id='eek-button', n_clicks=0, children='API call', style={'color': 'rgb(255, 255, 255)'}),
                html.Div(id='movie-title', children=[]),
                html.Div(id='movie-release',children=[]),
                html.Div(id='movie-overview', children=[]),
                html.Div(id='movie-senti', children=[]),

            ], style={ 'padding': '12px',
                    'font-size': '22px',
                    # 'height': '400px',
                    'border': 'thick blue solid',
                    'color': 'rgb(0, 0, 255)',
                    'backgroundColor': '#536869',
                    'textAlign': 'left',
                    },
            className='six columns'),

        ], className='twelve columns'),
        html.Br(),

    ], className='twelve columns'),


        # Output
    html.Div([
        # Footer
        html.Br(),
        html.A('Code on Github', href=githublink, target="_blank"),
        html.Br(),
        html.A("Data Source: Kaggle", href=sourceurl, target="_blank"),
        html.Br(),
        html.A("Data Source: TMDB", href=sourceurl2, target="_blank"),
    ], className='twelve columns'),



    ]
)

########## Callbacks

# TMDB API call
@app.callback(Output('tmdb-store', 'data'),
              [Input('eek-button', 'n_clicks')],
              [State('tmdb-store', 'data')])
def on_click(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks==0:
        data = {'title':' ', 'release_date':' ', 'overview':' ',}
    elif n_clicks>0:
        data = api_pull(random.choice(ids_list))
        
    return data



@app.callback([Output('movie-title', 'children'),
                Output('movie-release', 'children'),
                Output('movie-overview', 'children'),
                Output('movie-sentitment', 'children'),
                ],
              [Input('tmdb-store', 'modified_timestamp')],
              [State('tmdb-store', 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate
    else:
        #sentiment part 
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(data['overview'])
        # decide sentiment as positive, negative and neutral
        if sentiment_dict['compound'] >= 0.05 :
            final="Happy"
        elif sentiment_dict['compound'] <0.05 :
            final="Sad"
        else :
            final="Neutral"
        # responses
        # response1=f"Overall sentiment dictionary is : {sentiment_dict}"
        #response2=f"Sentence rated as {round(sentiment_dict['neg']*100, 2)}% Sad"
        #response3=f"Sentence rated as {round(sentiment_dict['neu']*100, 2)}% Neutral"
        #response4=f"Sentence rated as {round(sentiment_dict['pos']*100,2 )}% Happy"
        data['movie_senti']=f"Movie review is overall rated as {final} with {round(sentiment_dict['neg']*100, 2)}% Negative vs {round(sentiment_dict['pos']*100,2 )}% Positive words"
        return data['title'], data['release_date'], data['overview'], data['movie_senti']


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
