# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Find minimum and maximum payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a Dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[

    # Dashboard title
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'site1'},
            {'label': 'VAFB SLC-4E', 'value': 'site2'},
            {'label': 'KSC LC-39A', 'value': 'site3'},
            {'label': 'CCAFS SLC-40', 'value': 'site4'}
        ],
        value='ALL',
        placeholder='Select site',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    # TASK 3: Payload range
    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0',
            1000: '1000',
            2000: '2000',
            3000: '3000',
            4000: '4000',
            5000: '5000',
            6000: '6000',
            7000: '7000',
            8000: '8000',
            9000: '9000',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter chart
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )

])


# TASK 2: Callback for Pie Chart
@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def get_pie_chart(entered_site):

    # If ALL sites are selected
    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df,
            names='class',
            title='Landing Outcomes for All Sites'
        )

        return fig

    # If a specific site is selected
    else:

        if entered_site == 'site1':
            selected_site = 'CCAFS LC-40'

        elif entered_site == 'site2':
            selected_site = 'VAFB SLC-4E'

        elif entered_site == 'site3':
            selected_site = 'KSC LC-39A'

        elif entered_site == 'site4':
            selected_site = 'CCAFS SLC-40'

        # Filter dataframe for selected site
        filtered_df = spacex_df[
            spacex_df['Launch Site'] == selected_site
        ]

        # Create pie chart
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Landing Outcomes for {selected_site}'
        )

        return fig

# TASK 4: Callback for Scatter Chart

@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [
        Input(
            component_id='site-dropdown',
            component_property='value'
        ),
        Input(
            component_id='payload-slider',
            component_property='value'
        )
    ]
)
def get_scatter_chart(entered_site, payload_range):

    # First filter based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]

    # If ALL sites are selected

    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload Mass vs. Landing Outcome for All Sites'
        )

        return fig

    # If a specific site is selected

    else:

        if entered_site == 'site1':
            selected_site = 'CCAFS LC-40'

        elif entered_site == 'site2':
            selected_site = 'VAFB SLC-4E'

        elif entered_site == 'site3':
            selected_site = 'KSC LC-39A'

        elif entered_site == 'site4':
            selected_site = 'CCAFS SLC-40'

        # Filter by selected launch site
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == selected_site
        ]

        # Create scatter plot
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload Mass vs. Landing Outcome for {selected_site}'
        )

        return fig


# Run the application

if __name__ == '__main__':
    app.run(port=1050)