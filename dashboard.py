import pandas as pd
import dash
import plotly.graph_objs as go
from dash import dcc
from dash import html

data  = pd.read_csv('gapminder.csv')
#print(data.head())

app = dash.Dash(__name__)

# app.layout = html.H1(children='My Dash App', style={'textAlign': 'center', 'fontSize': 60,'color': 'royalblue'})
app.layout = html.Div([
    html.Div(children=[
        html.H1(children='My Dash App', style={'textAlign': 'center', 'fontSize': 60,'color': 'royalblue'})
    ], style={'broder': '1px black solid', 'float': 'left', 'width': '100%', 'height': '150px'}),

    html.Div(children=[
        dcc.Graph(id = 'scatter-plot',
                  figure = {
                      'data': [go.Scatter(
                          x = data['pop'],
                        y = data['gdpPercap'],
                          mode = 'markers',
                      )],
                      'layout': go.Layout(title = 'Scatter Plot',)
                  })
    ],style={'broder': '1px black solid', 'float': 'left', 'width': '49.7%'}),
    html.Div(children=[
        dcc.Graph(id = 'box-plot',
                  figure = {'data': [go.Box(
                           x = data['gdpPercap']
                      )],
                      'layout': go.Layout(title = 'Box Plot',)
                  })

    ],
             style={'broder': '1px black solid', 'float': 'left', 'width': '49.7%'}),
])
if __name__ == '__main__':
    app.run(debug=True)
