# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
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
                                                         {'label': 'site1', 'value': 'CCAFS LC-40'},
                                                         {'label': 'site2', 'value': 'VAFB SLC-4E'},
                                                         {'label': 'site3', 'value': 'KSC LC-39A'},
                                                         {'label': 'site4', 'value': 'CCAFS SLC-40'},
                                                      ],
                                                      value='ALL',
                                                      placeholder="Select a Launch Site here",
                                                      searchable=True
                                                      ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                        min=min_payload, max=max_payload, step=1000,
                                        value=[min_payload, max_payload]),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
               Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")] )
def get_pie_chart(entered_site,slider):
    
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title="Total Success Launches by {fname} sites".format(fname = entered_site))

        scoto = spacex_df[spacex_df['Payload Mass (kg)'].between(slider[0], slider[1])]
        figaro = px.scatter(scoto, x ='Payload Mass (kg)', y ='class', 
                            color="Booster Version Category",
                            title= "Correlation between Payload mass and launch success at {fname} sites".format(fname = entered_site))
        return fig, figaro
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df_2 = filtered_df.groupby(['class'])['class'].count().reset_index(name='count')
        fig2 = px.pie(filtered_df_2, values='count', 
        names='class',
        title="Total Success Launches at site {fname}".format(fname = entered_site))

        scotan = filtered_df[filtered_df['Payload Mass (kg)'].between(slider[0], slider[1])]
        figari = px.scatter(scotan, x ='Payload Mass (kg)', y ='class', 
                            color="Booster Version Category",
                            title= "Correlation between Payload mass and launch success at {fname}".format(fname = entered_site))
        
        return fig2,figari




        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
