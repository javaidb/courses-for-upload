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

dropdown_options=[{'label': 'All Sites', 'value': 'ALL'}]
launch_sites = list(spacex_df['Launch Site'].unique())
dropdown_options += [{'label': launch_site, 'value': launch_site} for launch_site in launch_sites]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(
                                    id='site-dropdown',
                                    options=dropdown_options,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    )),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={x: str(x) for x in range(1000,10000,1000)},
                                                value=[min_payload, max_payload])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df.copy()
    if entered_site == 'ALL':
        data = filtered_df.loc[filtered_df['class'] == 1]
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='All Launch Site Outcomes')
        return fig
    else:
        data = filtered_df.loc[filtered_df['Launch Site'] == entered_site]
        class_counts = data['class'].value_counts(normalize=True) * 100
        # data_grouped = data.groupby('Launch Site')['class']
        # print(data_grouped)
        fig = px.pie(values=class_counts.values, 
        names=class_counts.index.astype(str), 
        title=f'Total Successful Outcomes for {entered_site}')
        return fig

        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, payload_slider):
    # print(payload_slider)
    filtered_df = spacex_df.copy()
    filtered_df = filtered_df.loc[(filtered_df['Payload Mass (kg)'] >= min(payload_slider)) & (filtered_df['Payload Mass (kg)'] <= max(payload_slider))]
    if entered_site == 'ALL':
        # data = filtered_df.loc[filtered_df['class'] == 1]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                #  labels={'binary_values': 'Binary Values', 'x': 'Index'},
                 title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        data = filtered_df.loc[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                #  labels={'binary_values': 'Binary Values', 'x': 'Index'},
                 title=f'Correlation between Payload and Success for {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
