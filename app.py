import dash
import numpy as np
from dash import dcc
from dash import html
# import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests

countyNames = []
townNames = []


ontologyBaseURI = 'http://www.semanticweb.org/ashutoshbansal/ontologies/2021/10/project-ontology/'

selectAllCountiesQuery = '''PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A
PREFIX%20ours%3A%20%3Chttp%3A%2F%2Fwww.semanticweb.org%2Fashutoshbansal%2Fontologies%2F2021%2F10%2Fproject-ontology%3E%0A
select DISTINCT ?name ?county where {
 	?county rdf:type ours:county .
    ?county ours:name ?name .
}&Accept=application/sparql-results%2Bjson'''
urlForSelectAllCounties = f'http://localhost:7200/repositories/KDE-project?query={selectAllCountiesQuery}'
countyResponse = requests.request('GET', urlForSelectAllCounties)
counties = countyResponse.json();
countyNames = [e['name']['value'] for e in counties['results']['bindings']];
countyIRIs = [e['county']['value'] for e in counties['results']['bindings']];

selectAllTownsQuery = '''PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A
PREFIX%20ours%3A%20%3Chttp%3A%2F%2Fwww.semanticweb.org%2Fashutoshbansal%2Fontologies%2F2021%2F10%2Fproject-ontology%3E%0A
select DISTINCT ?name ?town where {
 	?town rdf:type ours:town .
    ?town ours:name ?name .
}&Accept=application/sparql-results%2Bjson'''
urlForSelectAllTowns = f'http://localhost:7200/repositories/KDE-project?query={selectAllTownsQuery}' 
townResponse = requests.request('GET', urlForSelectAllTowns)
towns = townResponse.json();
townNames = [e['name']['value'] for e in towns['results']['bindings']];
townIRIs = [e['town']['value'] for e in towns['results']['bindings']];

townsForDropdown = []
for i in range(len(townNames)):
    townsForDropdown.append({'label': townNames[i], 'value' : townIRIs[i]});
     
countiesForDropdown = []
for i in range(len(countyNames)):
    countiesForDropdown.append({'label': countyNames[i], 'value' : countyIRIs[i]});

query_1 = {'poi': '', 'location-type': '', 'location': ''}
query_2 = {'poi': '', 'location-type': '', 'location': ''}
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

points_of_interest = ['Pilgrim Path', 'Museum', 'Walled Towns', 'Landmarks']
location = ['Town', 'County']


app.layout = html.Div([

    html.Div(

            style={'backgroundColor': '#1d6b01', 'position': 'center', 'height': '20vh'},
            children=[
            html.H1(children='Query Historic Knowledge Graph', style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh', 'color': 'white'})
            ]
            ),
    html.H1(children="Question 1", style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFF00'},
        children=[
            html.H3(children="Select a point of interest"),

            dcc.Dropdown(
                id='poi-dropdown',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select a point of interest",
            ),
            html.H3(children="Select location type"),
            dcc.Dropdown(
                id='location-dropdown',
                style={'width': '40%'},
                options=[{'label': l, 'value': l} for l in location],
                value='',
                placeholder="Select location type",
            ),
            html.H3(children=f"Select town/county"),
            dcc.Dropdown(
                id='location-town-county-dropdown',
                style={'width': '40%'},
            ),
            html.Button('Submit', id='submit_1', n_clicks=0),
            html.Div(id='poi-output'),
            html.Div(id='location-output'),
            html.Div(id='location-town-county-output'),
        ]
    ),

    html.H1(children="Question 2", style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
        html.Div(
            style={'backgroundColor': '#FFFF00'},
            children=[
                html.H3(children="Select a point of interest"),

                dcc.Dropdown(
                    id='poi1-dropdown',
                    style={'width': '60%'},
                    options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                    value='',
                    multi=True,
                    placeholder="Select a point of interest",
                ),
                html.H3(children="Select location type"),
                dcc.Dropdown(
                    id='location1-dropdown',
                    style={'width': '40%'},
                    options=[{'label': l, 'value': l} for l in location],
                    value='',
                    placeholder="Select location type",
                ),
                html.Button('Submit', id='submit_2', n_clicks=0),
                html.Div(id='poi1-output'),
                html.Div(id='location1-output'),

            ]
        )

])


#call back to fetch value for poi
@app.callback(
    Output('poi-output', 'children'),
    Input('submit_1', 'n_clicks'),
    State('poi-dropdown', 'value'),
    State('location1-dropdown', 'value')
)
def update_output(n_clicks, value, locationType):
    print(value, locationType)
    query_1['poi'] = value
    query_1['location-type'] = locationType
   # POIs = getPointsOfInterestInPlace(entityType, location)
    return 'The selected point of interest "{}"'.format(
        value
    )


#call back to fetch value for location type (town/county)
@app.callback(
    Output('location-output', 'children'),
    Input('submit_1', 'n_clicks'),
    State('location-dropdown', 'value')
)
def update_output(n_clicks, value):
    query_1['location-type'] = value
    print(value)
    return 'The selected location. "{}"'.format(
        value
    )


#call back to fetch location eg. dublin/cork
@app.callback(
    Output('location-town-county-output', 'children'),
    Input('submit_1', 'n_clicks'),
    State('location-town-county-dropdown', 'value')
)

def update_output(n_clicks, value):
    query_1['location'] = value
    print(value)
    print(query_1)
    return 'The selected location. "{}"'.format(
        value
    )


#callback to chain the dropdowns
@app.callback(
    dash.dependencies.Output('location-town-county-dropdown', 'options'),
    [dash.dependencies.Input('location-dropdown', 'value')])
def set_cities_options(value):
    return countiesForDropdown if value == 'County' else townsForDropdown




def getPointsOfInterestInPlace(entityType, location):
    listOfTypes = 'FILTER (?place IN ('
    numTypes = 0
     
    for t in entityType:
        if(numTypes > 0): listOfTypes = listOfTypes + ','

        if(t == 'Pilgrim Path' ):
            listOfTypes = listOfTypes + 'ours:pilgrimPath'
        elif(t == 'Walled Towns'):
            listOfTypes = listOfTypes + 'ours:walledTown'
        elif(t == 'Museum'):
            listOfTypes = listOfTypes + 'dbo:Museum'
        elif(t == 'Landmarks'):
            listOfTypes = listOfTypes + 'ours:landmark'
        numTypes = numTypes + 1
        
    listOfTypes = listOfTypes + '))'
    
    
    selectPointsOfInterestQuery = '''PREFIX%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0A
PREFIX%20ours%3A%20%3Chttp%3A%2F%2Fwww.semanticweb.org%2Fashutoshbansal%2Fontologies%2F2021%2F10%2Fproject-ontology%3E%0A
select DISTINCT ?name ?place where {
 	?place rdf:type ?place .
    ?place ours:name ?name .
    ?place ours:locatedIn {location}
    {listOfTypes}
}&Accept=application/sparql-results%2Bjson'''
    urlForSelectPOI = f'http://localhost:7200/repositories/KDE-project?query={selectPointsOfInterestQuery}' 
    POIresponse = requests.request('GET', urlForSelectPOI)
    POIs = POIresponse.json();
    poiNames = [e['name']['value'] for e in POIs['results']['bindings']];
    poiIRIs = [e['town']['value'] for e in POIs['results']['bindings']];

    #townsForDropdown = []
    #for i in range(len(townNames)):
    #    townsForDropdown.append({'label': townNames[i], 'value' : townIRIs[i]});
    return np.column_stack((poiNames, poiIRIs))


# @app.callback(
# #     Output('poi1-output', 'children'),
# #     Input('submit_2', 'n_clicks'),
# #     State('poi1-dropdown', 'value')
# # )
# # def update_output(n_clicks, value):
# #     query_1['poi'] = value
# #     return 'The selected point of interest "{}"'.format(
# #
# #         value
# #     )
# #
# # @app.callback(
# #     Output('location1-output', 'children'),
# #     Input('submit_2', 'n_clicks'),
# #     State('location1-dropdown', 'value')
# # )
# # def update_output(n_clicks, value):
# #     query_1['location'] = value
# #     return 'The selected location. "{}"'.format(
# #         value
# #     )
if __name__ == '__main__':
    app.run_server(debug=True)
