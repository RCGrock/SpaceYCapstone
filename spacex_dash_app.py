# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    ],
                                                value='ALL',
                                                placeholder="Select a Launch site",
                                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 1000: '1,000', 2000:'2,000', 
                                                        3000:'3,000', 4000:'4,000', 5000:'5,000', 6000:'6,000',
                                                        7000:'7,000', 8000:'8,000', 9000:'9,000', 10000:'10,000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # data
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
        names='Launch Site', 
        title='Total Success Launch for all sites')
        return fig
    else:
        filtered_df = filtered_df.groupby('class', as_index=False).size()
        fig = px.pie(filtered_df, values='size', 
        names='class', 
        title='Total Success Launch per Launch Site')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
            [Input(component_id='site-dropdown', component_property='value'), 
            Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(site, payload_range):
    filtered_df = spacex_df[spacex_df['Launch Site'] == site]
    low = payload_range[0]
    high = payload_range[1]
    if site == "ALL":
        fig = px.scatter(spacex_df[spacex_df["Payload Mass (kg)"].between(low,high)], x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        hover_data=['Booster Version'],
        title="Correlation between Payload mass and Success for all sites")
        return fig
    else:
        fig = px.scatter(filtered_df[filtered_df["Payload Mass (kg)"].between(low,high)], x="Payload Mass (kg)", y="class",
        color="Booster Version Category",
        hover_data=['Booster Version'],
        title=f"Correlation between Payload mass and Success for {site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
