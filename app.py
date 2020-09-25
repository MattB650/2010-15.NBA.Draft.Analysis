#Importing Necessary Packages
import pandas as pd
import plotly.express as px
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

sheet = pd.read_csv('Combined.Draft.csv', index_col=0, encoding='cp1252')

##Remove Rows Where WS is null (Did not play in NBA) (Old Idea)
##sheet = sheet[sheet['WS'].notna()]

#Remove Rows Where FIC is null(Did not have pre-draft season that met requirements)
sheet = sheet.query('FIC!=0')

#Rename Z-Score Column
sheet['Adjusted Draft Score'] = sheet['Z-Score']

#Set Parameters for Scatter Plot
fig = px.scatter(sheet, x='VA', y='Adjusted Draft Score', color='Adjusted Draft Score',
                 title='NBA 2010-15 Drafts: Floor Impact Counter vs Adjusted Draft Score',
                 hover_data=(['Player', 'Pos', 'Year', 'FIC', 'Adjusted Draft Score']))

fig.update_traces(mode='markers', marker_size=15)

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)


#Set Style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Initialize Dash Server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

#Set App Layout

app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**
                Mouse over a point to reveal team and lineup.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),
        
        html.Div([
            dcc.Markdown("""
                **Description**
            
                This plot includes the best 5-man lineup (min. 100
                possessions played, per CleaningTheGlass) from each
                2018-19 NBA team. The two metrics used are D-RAPTOR
                (per FiveThirtyEight) and SY Q-RAD (per Andrew Patton
                and B-Ball Index), with the latter looking at how
                much on average a defender deterrs an offensive player
                from attempting high efficiency shots (corner threes,
                layups, etc.). This plot aims to provide an alternative
                way to measure team defense.
                """),
                html.Pre(id='description', style=styles['pre'])
            ], className='three columns')
        ])
    ])


#Run Dash Server

if __name__ == '__main__':
    app.run_server()
