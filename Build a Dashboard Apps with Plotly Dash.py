#
# @file         Build a Dashboard Apps with Plotly Dash.py
# @author       Erwin Rabano Pasia
# @version      V1.0
# @date         2023/15/01
# @description  This is the code for the Dashboard Web Apps using Plotly Dash.
#

# Import required libraries
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import html
from dash import dcc


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout, but include an empty "list" called launch_site_list.
launch_site_list = []

# This line adds an element to the launch_site_list list in the form of a dictionary with a 'label' key and 'value' key, 
# both having the value 'All Sites'. The append() method is used to add this element to the end of the list.
launch_site_list.append({'label': 'All Sites', 'value': 'All Sites'})

# This line starts a for loop that iterates through the index of the value counts 
# of the "Launch Site" column of the spacex_df DataFrame. So we automatically pick-up what is in the list.
for item in spacex_df["Launch Site"].value_counts().index:
    launch_site_list.append({'label': item, 'value': item})
app.layout = html.Div(children=[html.H1('-SpaceX Launch Records Dashboard-',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                            # Call here the created function
                                            options = launch_site_list, 
                                            value = 'All Sites', 
                                            placeholder = "Please Select a Launch Site Here:", 
                                            searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload Range (Kgs.):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min = 0, max = 10000, step = 1000, 
                                                value = [min_payload, max_payload], 
                                                marks={ 2500: {'label': '2500 (Kgs.)'}, 5000: {'label': '5000 (Kgs.)'}, 7500: {'label': '7500 (Kgs.)'}}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'All Sites':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count', 
        names='class',
        title=f'Total Success Launched for site {entered_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload):
    low, high = payload
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)]       
    if entered_site == 'All Sites':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        fig = px.scatter(filtered_df[filtered_df['Launch Site'] == entered_site],
        x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title=f'Correlation between Payload and Success for site {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
