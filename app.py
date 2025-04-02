import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html, Input, Output

# FIFA World Cup Winners and Runner-Ups Data
data = [
    {"Year": 2018, "Winner": "France", "Runner-Up": "Croatia"},
    {"Year": 2014, "Winner": "Germany", "Runner-Up": "Argentina"},
    {"Year": 2010, "Winner": "Spain", "Runner-Up": "Netherlands"},
    {"Year": 2006, "Winner": "Italy", "Runner-Up": "France"},
    {"Year": 2002, "Winner": "Brazil", "Runner-Up": "Germany"},
    {"Year": 1998, "Winner": "France", "Runner-Up": "Brazil"},
    {"Year": 1994, "Winner": "Brazil", "Runner-Up": "Italy"},
    {"Year": 1990, "Winner": "West Germany", "Runner-Up": "Argentina"},
    {"Year": 1986, "Winner": "Argentina", "Runner-Up": "West Germany"},
    {"Year": 1982, "Winner": "Italy", "Runner-Up": "West Germany"},
    {"Year": 1978, "Winner": "Argentina", "Runner-Up": "Netherlands"},
    {"Year": 1974, "Winner": "West Germany", "Runner-Up": "Netherlands"},
    {"Year": 1970, "Winner": "Brazil", "Runner-Up": "Italy"},
    {"Year": 1966, "Winner": "England", "Runner-Up": "Germany"},
    {"Year": 1962, "Winner": "Brazil", "Runner-Up": "Czechoslovakia"},
    {"Year": 1958, "Winner": "Brazil", "Runner-Up": "Sweden"},
    {"Year": 1954, "Winner": "West Germany", "Runner-Up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner-Up": "Brazil"},
    {"Year": 1938, "Winner": "Italy", "Runner-Up": "Hungary"},
    {"Year": 1934, "Winner": "Italy", "Runner-Up": "Czechoslovakia"},
    {"Year": 1930, "Winner": "Uruguay", "Runner-Up": "Argentina"}
]

df = pd.DataFrame(data)

df['Winner'] = df['Winner'].replace('West Germany', 'Germany')
df['Runner-Up'] = df['Runner-Up'].replace('West Germany', 'Germany')

win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

runner_up_counts = df['Runner-Up'].value_counts().reset_index()
runner_up_counts.columns = ['Country', 'Runner-Ups']

final_df = pd.merge(win_counts, runner_up_counts, on='Country', how='outer').fillna(0)
final_df['Total Appearances'] = final_df['Wins'] + final_df['Runner-Ups']

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Winners and Runner-Ups Dashboard"),

    dcc.Graph(id='choropleth-map'),

    html.Label("Select a Country:"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': c, 'value': c} for c in final_df['Country']],
        placeholder="Select a country"
    ),
    html.Div(id='country-output'),

    html.Label("Select a Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': y, 'value': y} for y in df['Year']],
        placeholder="Select a year"
    ),
    html.Div(id='year-output')
])

@app.callback(
    Output('choropleth-map', 'figure'),
    Input('country-dropdown', 'value')
)
def update_map(_):
    fig = px.choropleth(
        final_df,
        locations="Country",
        locationmode="country names",
        color="Total Appearances",
        hover_name="Country",
        hover_data={"Wins": True, "Runner-Ups": True, "Total Appearances": False},
        title="FIFA World Cup Winners and Runner-Ups",
        color_continuous_scale="Blues"
    )
    return fig

@app.callback(
    Output('country-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_country_output(selected_country):
    if selected_country:
        wins = final_df.loc[final_df['Country'] == selected_country, 'Wins'].values[0]
        return f"{selected_country} has won the World Cup {int(wins)} times."
    return ""

@app.callback(
    Output('year-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_year_output(selected_year):
    if selected_year:
        row = df[df['Year'] == selected_year]
        return f"In {selected_year}, {row['Winner'].values[0]} won and {row['Runner-Up'].values[0]} was the runner-up."
    return ""

if __name__ == '__main__':
    app.run(debug=True)


# Deployed at https://cp321-aksp.onrender.com/
