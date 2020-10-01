# Importing Necessary Packages
import pandas as pd
import plotly.express as px
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

sheet = pd.read_csv('Combined.Draft.csv', index_col=0, encoding='cp1252')




# Remove Rows Where FIC is null(Did not have pre-draft season that met requirements)
sheet = sheet.query('FIC!=0')
sheet = sheet.query('VA!=0')

# Rename Z-Score Column
sheet['Adjusted Draft Score'] = sheet['Z-Score']

choices = sheet[['FIC', 'VA']]


# Set Style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize Dash Server
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# Set App Layout

app.layout = html.Div([
    dcc.Graph(
        id='scat',
        animate=True
    ),
    dcc.Dropdown(id='box',
                 options=[
                     {'label': choice, 'value': choice} for choice in choices


                 ],
                 value='FIC'

                 ),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**
                Mouse over a point to reveal player and selected advanced metrics.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Description**


                """),
            html.Pre(id='description', style=styles['pre'])
        ], className='three columns')
    ])
])


@app.callback(
    dash.dependencies.Output(component_id='scat', component_property='figure'),
    [dash.dependencies.Input(component_id='box', component_property='value')])
def update_plot(a_value):
    if a_value == 'FIC':

        fig = px.scatter(sheet, x='FIC', y='Adjusted Draft Score', color='Adjusted Draft Score',
                         title='NBA 2010-15 Drafts: Floor Impact Counter vs Adjusted Draft Score',
                         hover_data=(['Player', 'Pos', 'Year', 'FIC', 'Adjusted Draft Score']))

        fig.update_traces(mode='markers', marker_size=13)

        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        fig.update_xaxes(range=[0, 800])
        return fig
    elif a_value == 'VA':
        fig = px.scatter(sheet, x='VA', y='Adjusted Draft Score', color='Adjusted Draft Score',
                         title='NBA 2010-15 Drafts: Floor Impact Counter vs Adjusted Draft Score',
                         hover_data=(['Player', 'Pos', 'Year', 'FIC', 'Adjusted Draft Score']))

        fig.update_traces(mode='markers', marker_size=13)

        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )

        fig.update_xaxes(range=[0,15])
        return fig









# Run Dash Server

if __name__ == '__main__':
    app.run_server()


