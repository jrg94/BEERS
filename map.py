import plotly.graph_objects as go 
import pandas as pd
import dash
from dash import dcc
from dash import html

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

gb = df.groupby(['Code']).mean()

dataForHover = df.groupby(['Code', 'Product']).mean()

##dataForHover['text'] = df['state'] + '<br>' + \
##    'Beef ' + df['beef'] + ' Dairy ' + df['dairy'] + '<br>' + \
##    'Fruits ' + df['total fruits'] + ' Veggies ' + df['total veggies'] + '<br>' + \
##    'Wheat ' + df['wheat'] + ' Corn ' + df['corn']

print(dataForHover)
print(dataForHover['NRx_Month_1'])

fig = go.Figure(data=go.Choropleth(
    locations=gb.index, # Spatial coordinates
    z = gb['NRx_Month_1'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "Prescription Count",
    text=df['text'], # hover text
    marker_line_color='white', # line markers between states
))

fig.update_layout(
    title_text = 'Veeva Data',
    geo_scope='usa', # limit map scope to USA
)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)  # Turn off reloader if inside Jupyter