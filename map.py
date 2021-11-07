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


def generate_product_line_plot(df: pd.DataFrame, products: list[str]):
    """
    Generates a line plot for each product in the list of products.
    Line plots include errors.

    :param df: the dataframe containing the data to be plotted
    :param products: a list of products to be plotted
    """
    line_plot = go.Figure()
    for product in products:
        line_plot.add_trace(
            go.Scatter(
                x=[1, 2, 3, 4, 5, 6],
                y=[df.get_group(product)[f'NRx_Month_{i}'].sum() for i in range(1, 7)],
                name=product
            )
        )
    line_plot.update_layout(
        title_text = 'Veeva Data Graph',
    )
    return line_plot


def generate_map_plot(month_key: str, df: pd.DataFrame):
    """
    Generates a plot of the map of the US. The map is colored based on the
    total number of prescriptions for each state. The hover data is the
    total prescriptions of each product in each state. 

    :param month_key: the month of data to be plotted in the form NRx_Month_#
    :param df: the dataframe containing the data to be plotted
    """    
    fig = go.Figure(data=go.Choropleth(
        locations=df.index, # Spatial coordinates
        z = df[month_key].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Prescription Count",
        text=df['text'], # hover text
        marker_line_color='white', # line markers between states
    ))

    fig.update_layout(
        title_text = 'Veeva Data',
        geo_scope='usa', # limit map scope to USA
        transition_duration=500
    )

    return fig

def generate_scatter_plot(df: pd.DataFrame):
    """
    Generates a scatter plot of the data where the x-axis is the name of
    the prescriber and the y-axis is the mean number of prescriptions.
    """
    return go.Figure(
        go.Scatter(
            x=df.get_group('Cholecap')['last_name'].values, 
            y=df.get_group('Cholecap')['TRxMean'].values
        )
    )


# Reading in data
df = pd.read_csv('Veeva_Prescriber_Data.csv')
df['Code'] = df['State'].map(us_state_to_abbrev)
df = df.sort_values('TRx_Month_1')
products = df['Product'].unique()
active_products = dict(zip(products, [True, True, True, True]))

# Compile TRx over 6 months to provide mean
df['TRxMean'] = (df['TRx_Month_1'] + df['TRx_Month_2'] + df['TRx_Month_3']+ df['TRx_Month_4']+df['TRx_Month_5']+ df['TRx_Month_6'])/6
df = df.sort_values('TRxMean')

# Create product group
product_group = df.groupby(['Product'])

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

    dcc.Graph(figure=generate_product_line_plot(product_group, products), id='graph-with-error-bars'),

    dcc.Graph(figure=generate_scatter_plot(product_group))

])

@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('month-slider', 'value'), Input('graph-with-error-bars', 'restyleData')]
)
def update_map(month: int, selected: list):
    month_key = f'NRx_Month_{month}'

    map_data = df.copy()
    if selected is not None:
        index = selected[1][0]
        active_products[products[index]] = not active_products[products[index]]
        active = [drug for drug, value in active_products.items() if value]
        map_data = df[df['Product'].isin(active)]

    map_data = map_data.groupby(['Code']).sum()  # Sums data by state
    dataForHover = df.groupby(['Code', 'Product']).sum().reset_index().astype(str)
    dataForHover['text'] = dataForHover['Product'] + ': ' + dataForHover[month_key] + '<br>'
    map_data['text'] = dataForHover.groupby(['Code']).sum()['text']

    return generate_map_plot(month_key, map_data)

if __name__ == '__main__':
    app.run_server(debug=True)
