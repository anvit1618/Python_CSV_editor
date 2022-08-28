#----------------------------------------------------------
#IMPORTING LIBRARIES
#----------------------------------------------------------

from dash import Dash, dcc, Output, Input, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import datetime


#----------------------------------------------------------
#BUILDING COMPONENTS
#----------------------------------------------------------

def create_dash_application(flask_app):
    df = pd.read_csv("price1.csv")
    df["DATE"] = pd.to_datetime(df["DATE"]).dt.date
    dash_app = Dash(server=flask_app, name="Dashboard", external_stylesheets=[dbc.themes.VAPOR], url_base_pathname="/dash/")

    mytitle = dcc.Markdown(children="")
    mygraph = dcc.Graph(figure={})
    dropdown = dcc.Dropdown(options=df.columns.values[1:],
                            value='TCS',
                            clearable=False)
    #----------------------------------------------------------
    #CUSTOMIZING LAYOUT
    #----------------------------------------------------------
    def serve_layout():
        return html.H1('The time is: ' + str(datetime.datetime.now()))
    input_types = ['search', 'number']
    dash_app.layout = serve_layout
    dash_app.layout =  dbc.Container([
        dbc.Row([
            dbc.Col([mytitle], width=6)
        ], justify='center'),
        dbc.Row([
            dbc.Col([mygraph], width=10)
        ], justify='center'),
        dbc.Row([
            dbc.Col([dropdown], width=6)
        ], justify='center')


    ], fluid=True)

    
    #----------------------------------------------------------
    #CALLBACKS [allows components to interact]
    #----------------------------------------------------------

    @dash_app.callback(
        Output(mygraph, 'figure'),
        Output(mytitle, 'children'),
        Input(dropdown, 'value')
    )
    def update_graph(column_name):

        fig = px.line(df,
                    height=600,
                    x='DATE',
                    y=column_name)

        return fig, '# '+column_name
    
    
    return dash_app