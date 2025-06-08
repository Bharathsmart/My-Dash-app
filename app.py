import pandas as pd
import dash
import plotly.graph_objs as go
import plotly.express as px
from dash import dcc, html, Input, Output

# Load data
data = pd.read_csv('gapminder.csv')

# Summary info
total_countries = data['country'].nunique()
total_continents = data['continent'].nunique()
years = sorted(data['year'].unique())

# App setup
app = dash.Dash(__name__)
app.title = "Gapminder Dashboard"

# Layout
app.layout = html.Div(style={'fontFamily': 'Arial', 'backgroundColor': '#f8f9fa', 'padding': '20px'}, children=[

    html.H1("🌍 Gapminder Insights Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),

    html.Div([
        html.Div([
            html.H4("🌐 Total Countries", style={'color': '#7f8c8d'}),
            html.H2(f"{total_countries}", style={'color': '#2980b9'})
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.H4("🌍 Continents", style={'color': '#7f8c8d'}),
            html.H2(f"{total_continents}", style={'color': '#27ae60'})
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.H4("📅 Year Range", style={'color': '#7f8c8d'}),
            html.H2(f"{years[0]} - {years[-1]}", style={'color': '#8e44ad'})
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
    ], style={'textAlign': 'center'}),

    html.Div([
        html.Label("🔎 Filter by Continent:", style={'fontSize': '18px'}),
        dcc.Dropdown(
            id='continent-filter',
            options=[{'label': c, 'value': c} for c in sorted(data['continent'].unique())] + [{'label': 'All', 'value': 'All'}],
            value='All',
            clearable=False,
            style={'width': '300px'}
        ),
    ], style={'padding': '20px', 'textAlign': 'center'}),

    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='box-plot'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='sunburst-chart'),
    dcc.Graph(id='heatmap')
])

# Callback
@app.callback(
    [Output('scatter-plot', 'figure'),
     Output('box-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('sunburst-chart', 'figure'),
     Output('heatmap', 'figure')],
    [Input('continent-filter', 'value')]
)
def update_charts(selected_continent):
    filtered = data if selected_continent == 'All' else data[data['continent'] == selected_continent]

    latest_year = filtered['year'].max()
    latest_data = filtered[filtered['year'] == latest_year]

    # Scatter Plot
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

    # Box Plot
    box = go.Figure(data=[
        go.Box(x=filtered['continent'], y=filtered['gdpPercap'], boxpoints='all', jitter=0.5)
    ])
    box.update_layout(title='GDP per Capita Distribution by Continent', xaxis_title='Continent', yaxis_title='GDP per Capita')

    # Pie Chart
    pie = px.pie(latest_data, names='continent', values='pop',
                 title='Population Share by Continent (Latest Year)', color_discrete_sequence=px.colors.sequential.RdBu)

    # Sunburst Chart
    sunburst = px.sunburst(latest_data, path=['continent', 'country'], values='pop',
                           title='Population Hierarchy (Continent → Country)', color='lifeExp',
                           color_continuous_scale='RdBu')

    # Heatmap (Correlation)
    corr_df = filtered[['lifeExp', 'gdpPercap', 'pop']].corr()
    heatmap = px.imshow(corr_df,
                        text_auto=True,
                        color_continuous_scale='Blues',
                        title='Correlation Matrix')


    return scatter, box, pie, sunburst, heatmap

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
