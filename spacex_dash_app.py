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
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id = 'site-dropdown',
                                            options = [{'label': 'All Sites', 'value': 'All Sites'},
                                                       {'label': "CCAFS LC-40", 'value': "CCAFS LC-40"},
                                                       {'label': "VAFB SLC-4E", 'value': "VAFB SLC-4E"},
                                                       {'label': "KSC LC-39A", 'value': "KSC LC-39A"},
                                                       {'label': "CCAFS SLC-40", 'value': "CCAFS SLC-40"}],
                                            placeholder = 'Select a Launch Site here',
                                            searchable = True ,
                                            clearable = False,
                                            value = 'All Sites'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([dcc.RangeSlider(id = 'payload_slider',
                                                          min = 0,
                                                          max = 10000,
                                                          step = 1000,
                                                          marks = {0: {'label': '0'},
                                                                   2500: {'label': '2500'},
                                                                   5000: {'label': '5000'},
                                                                   7500: {'label': '7500'},
                                                                   10000: {'label': '10000'},}, 
                                                          value = [min_payload,max_payload]),]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
     Output(component_id = 'success-pie-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value')]
)
def pie_chart(site_dropdown):
    if (site_dropdown == 'All Sites'):
        all_sites  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(
                all_sites,
                names = 'Launch Site',
                title = 'Total Success at All Sites',
            )
    else:
        site_specific  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(
                site_specific,
                names = 'class',
                title = 'Total Success Launches at Site' +site_dropdown,
            )
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
     Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
     [Input(component_id = 'site-dropdown', component_property = 'value'), 
     Input(component_id = "payload_slider", component_property = "value")]
)
def scatter_plot(site_dropdown,payload_slider):
    if (site_dropdown == 'All Sites' or site_dropdown == 'None'):
        low, high = payload_slider
        all_sites  = spacex_df
        inrange = (all_sites['Payload Mass (kg)'] > low) & (all_sites['Payload Mass (kg)'] < high)
        fig = px.scatter(
                all_sites[inrange], 
                x = "Payload Mass (kg)", 
                y = "class",
                title = 'Payload and Success Relationship for all sites',
                color="Booster Version Category"
            )
    else:
        low, high = payload_slider
        site_specific  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        inrange = (site_specific['Payload Mass (kg)'] > low) & (site_specific['Payload Mass (kg)'] < high)
        fig = px.scatter(
                site_specific[inrange],
                x = "Payload Mass (kg)",
                y = "class",
                title = 'Payload and Success Relationship for Site ' +site_dropdown,
                color="Booster Version Category"
            )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
