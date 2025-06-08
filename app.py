import pandas as pd
import dash
import plotly.graph_objs as go
from dash import dcc, html, Input, Output

# Load data
data = pd.read_csv('gapminder.csv')

# Extract summary info
total_countries = data['country'].nunique()
total_continents = data['continent'].nunique()
years = sorted(data['year'].unique())

# App init
app = dash.Dash(__name__)
app.title = "Gapminder Dashboard"

# Layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#f4f4f4', 'padding': '20px'}, children=[
    html.Div([
        html.H1("🌍 Gapminder Insights Dashboard", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '20px'}),
    ]),

    html.Div([
        html.Div([
            html.Div([
                html.H4("🌐 Total Countries", style={'color': '#7f8c8d'}),
                html.H2(f"{total_countries}", style={'color': '#2980b9'})
            ], className='card'),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Div([
                html.H4("🌍 Continents", style={'color': '#7f8c8d'}),
                html.H2(f"{total_continents}", style={'color': '#27ae60'})
            ], className='card'),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Div([
                html.H4("📅 Years Range", style={'color': '#7f8c8d'}),
                html.H2(f"{years[0]} - {years[-1]}", style={'color': '#8e44ad'})
            ], className='card'),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'textAlign': 'center'}),

    html.Div([
        html.Label("Filter by Continent:", style={'fontSize': '18px', 'marginRight': '10px'}),
        dcc.Dropdown(
            id='continent-filter',
            options=[{'label': c, 'value': c} for c in sorted(data['continent'].unique())] + [{'label': 'All', 'value': 'All'}],
            value='All',
            clearable=False,
            style={'width': '300px'}
        ),
    ], style={'padding': '20px', 'textAlign': 'center'}),

    html.Div([
        dcc.Graph(id='scatter-plot'),
    ], style={'width': '100%', 'padding': '10px'}),

    html.Div([
        dcc.Graph(id='box-plot'),
    ], style={'width': '100%', 'padding': '10px'})
])

# Callback for interactivity
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('box-plot', 'figure')],
    [Input('continent-filter', 'value')]
)
def update_graphs(selected_continent):
    filtered = data if selected_continent == 'All' else data[data['continent'] == selected_continent]

    scatter = go.Figure(data=[
        go.Scatter(
            x=filtered['pop'],
            y=filtered['gdpPercap'],
            mode='markers',
            marker=dict(color=filtered['lifeExp'], colorscale='Viridis', showscale=True),
            text=filtered['country'],
            hovertemplate='Country: %{text}<br>GDP per Cap: %{y}<br>Population: %{x:,}<extra></extra>'
        )
    ])
    scatter.update_layout(title='GDP per Capita vs Population', xaxis_title='Population', yaxis_title='GDP per Capita')

    box = go.Figure(data=[
        go.Box(x=filtered['continent'], y=filtered['gdpPercap'], boxpoints='all', jitter=0.5, pointpos=-1.8)
    ])
    box.update_layout(title='GDP per Capita Distribution by Continent', xaxis_title='Continent', yaxis_title='GDP per Capita')

    return scatter, box

# Run
if __name__ == '__main__':
    app.run(debug=True)
