import plotly.graph_objects as go 
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

df = pd.read_csv('Veeva_Prescriber_Data.csv')
df['Code'] = df['State'].map(us_state_to_abbrev)

gb = df.groupby(['Code']).sum()

dataForHover = df.groupby(['Code', 'Product']).sum().reset_index().astype(str)

dataForHover['text'] = dataForHover['Product'] + ': ' + dataForHover['NRx_Month_1'] + '<br>'
dataForHover = dataForHover.groupby(['Code']).sum()

## Figure 1 is the USA map
fig = go.Figure(data=go.Choropleth(
    locations=gb.index, # Spatial coordinates
    z = gb['NRx_Month_1'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Prescription Count",
    text=dataForHover['text'], # hover text
    marker_line_color='white', # line markers between states
))

fig.update_layout(
    title_text = 'Veeva Data',
    geo_scope='usa', # limit map scope to USA
)

##Figure 2 is the error bar chart
fig2 = go.Figure(data=go.Scatter(
        x=[1, 2, 3, 4],
        y=[2, 1, 3, 4],
        error_y=dict(
            type='percent',
            symmetric=False,
            value=15,
            valueminus=25)
    ))

fig.update_layout(
    title_text = 'Veeva Data Graph',
)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig,
    id='graph-with-slider'),

    dcc.Slider(
        id = 'month-slider',
        min=1,
        max=6,
        marks={i: 'Month {}'.format(i) for i in range(1, 7)},
        value=-3
    ),
    html.Div(id='my-output'),

        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'Month 1', 'value': 'M1'},
            {'label': 'Month 2', 'value': 'M2'},
            {'label': 'Month 3', 'value': 'M3'},
            {'label': 'Month 4', 'value': 'M4'}
        ],
        value='MC'
    ),

    dcc.Graph(figure=fig2,
    id='graph-with-error-bars')

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('month-slider', 'value'))

def update_figure(selected_year):
    #filtered_df = df[df.year == selected_year]

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)