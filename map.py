import plotly.graph_objects as go 
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

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


## Reading in data
df = pd.read_csv('Veeva_Prescriber_Data.csv')
df['Code'] = df['State'].map(us_state_to_abbrev)
df = df.sort_values('TRx_Month_1')
products = df['Product'].unique()
active_products = dict(zip(products, [True, True, True, True]))

gb = df.groupby(['Code']).sum()

dataForHover = df.groupby(['Code', 'Product']).sum().reset_index().astype(str)

##Month 1 for data by default
dataForHover['text'] = dataForHover['Product'] + ': ' + dataForHover['NRx_Month_1'] + '<br>'
dataForHover = dataForHover.groupby(['Code']).sum()

gb = df.groupby(['Product'])

##Figure 2 is the error bar chart
fig2 = go.Figure()

## Figure 2_ALT is drug with full prescriber information
fig3 = go.Figure()

#compile TRx over 6 months to provide mean
df['TRxMean'] = (df['TRx_Month_1'] + df['TRx_Month_2'] + df['TRx_Month_3']+ df['TRx_Month_4']+df['TRx_Month_5']+ df['TRx_Month_6'])/6
df = df.sort_values('TRxMean')

#Need to add the conditional here to cut out bottom 90% 
gb = df.groupby(['Product'])

#Figure 3 is the scatter on individual people to show top sellers
fig3 = px.scatter(
    x=gb.get_group('Cholecap')['last_name'].values, 
    y=gb.get_group('Cholecap')['TRxMean'].values)

fig3.show()

#add each plots
fig2.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5, 6], #hard coded months
        #y=[2, 1, 3, 4], #need to pull values
        y = [gb.get_group('Cholecap')[f'NRx_Month_{i}'].sum() for i in range(1, 7)],
        name = 'Cholecap'
        #error_y=dict(
        #    type='percent',
        #    symmetric=False,
        #    value=y_Drug1['NRx_Month_1'].max()-y_Drug1['NRx_Month_1'].mean(), # error bar calculate off max
        #    valueminus=y_Drug1['NRx_Month_1'].mean()-y_Drug1['NRx_Month_1'].max() # error bar calculate off min
        #    )
))

fig2.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5, 6], #hard coded months
        #y=[2, 1, 3, 4], #need to pull values
        y = [gb.get_group('Zap-a-Pain')[f'NRx_Month_{i}'].sum() for i in range(1, 7)],
        name = 'Zap-a-Pain'
        #error_y=dict(
        #    type='percent',
        #    symmetric=False,
        #    value=y_Drug1['NRx_Month_1'].max()-y_Drug1['NRx_Month_1'].mean(), # error bar calculate off max
        #    valueminus=y_Drug1['NRx_Month_1'].mean()-y_Drug1['NRx_Month_1'].max() # error bar calculate off min
        #    )
))
fig2.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5, 6], #hard coded months
        #y=[2, 1, 3, 4], #need to pull values
        y = [gb.get_group('Nasalclear')[f'NRx_Month_{i}'].sum() for i in range(1, 7)],
        name = 'Nasalclear'
        #error_y=dict(
        #    type='percent',
        #    symmetric=False,
        #    value=y_Drug1['NRx_Month_1'].max()-y_Drug1['NRx_Month_1'].mean(), # error bar calculate off max
        #    valueminus=y_Drug1['NRx_Month_1'].mean()-y_Drug1['NRx_Month_1'].max() # error bar calculate off min
        #    )
))
fig2.add_trace(go.Scatter(
        x=[1, 2, 3, 4, 5, 6], #hard coded months
        y = [gb.get_group('Nova-itch')[f'NRx_Month_{i}'].sum() for i in range(1, 7)],
        name = 'Nova-itch',
        error_y=dict(
            type='percent',
            symmetric=False,
            array=[gb.get_group('Nova-itch')[f'NRx_Month_{i}'].max() - gb.get_group('Nova-itch')[f'NRx_Month_{i}'].sum() for i in range(1, 7)], # error bar calculate off max
            arrayminus=[gb.get_group('Nova-itch')[f'NRx_Month_{i}'].sum() - gb.get_group('Nova-itch')[f'NRx_Month_{i}'].min()for i in range(1, 7)] # error bar calculate off min
            )
))

fig2.update_layout(
    title_text = 'Veeva Data Graph',
)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),

    dcc.Slider(
        id = 'month-slider',
        min=1,
        max=6,
        marks={i: 'Month {}'.format(i) for i in range(1, 7)},
        value=1
    ),
    html.Div(id='my-output'),

        dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': 'All Drugs', 'value': 'SUMMARY'},
            {'label': 'Drug 1', 'value': 'M1'},
            {'label': 'Drug 2', 'value': 'M2'},
            {'label': 'Drug 3', 'value': 'M3'},
            {'label': 'Drug 4', 'value': 'M4'}
        ],
        value='MC'
    ),

    dcc.Graph(figure=fig2,
    id='graph-with-error-bars')

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('month-slider', 'value'), Input('graph-with-error-bars', 'restyleData')]
)
def update_figure(month: int, selected: list):
    month_key = f'NRx_Month_{month}'

    gb = df
    if selected is not None:
        index = selected[1][0]
        active_products[products[index]] = not active_products[products[index]]
        active = [drug for drug, value in active_products.items() if value]
        gb = df[df['Product'].isin(active)]
    gb = gb.groupby(['Code']).sum()

    dataForHover = df.groupby(['Code', 'Product']).sum().reset_index().astype(str)

    dataForHover['text'] = dataForHover['Product'] + ': ' + dataForHover[month_key] + '<br>'
    dataForHover = dataForHover.groupby(['Code']).sum()

    ## Figure 1 is the USA map
    fig = go.Figure(data=go.Choropleth(
        locations=gb.index, # Spatial coordinates
        z = gb[month_key].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Prescription Count",
        text=dataForHover['text'], # hover text
        marker_line_color='white', # line markers between states
    ))

    fig.update_layout(
        title_text = 'Veeva Data',
        geo_scope='usa', # limit map scope to USA
        transition_duration=500
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
