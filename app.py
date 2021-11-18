from collections import OrderedDict

import dash
import pandas as pd
from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output, State
from Query_executor import QueryExecutor

describe = {'poi' : '', 'location-type': '', 'location': ''}
query_1 = {'poi': '', 'location-type': '', 'location': ''}
query_2 = {'poi': '', 'location-type': '', 'location': ''}
query_3 = {'poi': '', 'location-type': ''}
query_4 = {'poi': '', 'location-type': '', 'another_poi': '', 'name_of_another_poi': ''}
query_5 = {'poi': '', 'associated-with': '', 'pattern': ''}
query_6 = {'period': '', 'poi': ''}
query_7 = {'poi': '', 'period-type': '', 'another_poi': '', 'name_of_another_poi': ''}

app = dash.Dash(__name__)
app.title = 'Irish History'
points_of_interest = ['Pilgrim Path', 'Museum', 'Walled Towns', 'Landmarks']
location = ['Locality', 'County']

data = QueryExecutor().loading_default_data()
counties = data[0]
counties.pop(31)
#print(counties);
print("\n")
towns = data[1]
#print(towns);
print("\n")
museums = data[2]
##print(museums);
print("\n")
landmarks = data[3]
#print(landmarks);
print("\n")
walledTowns = data[4]
#print(walledTowns);
print("\n")
pilgrimPaths = data[5]
print(pilgrimPaths)
print("\n")
historicPeriods = data[6]
#print(historicPeriods)
historicCenturies = data[7][1:]
#print(historicCenturies)
years = data[8]
#print(years)

app.layout = html.Div([

    html.Div(

        style={'backgroundColor': '#1d6b01', 'position': 'center', 'height': '20vh'},
        children=[
            html.H2(children='Irish History Knowledge Graph Application',
                    style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh', 'color': 'white'})
        ]
    ),

    html.H2(children="Give details about a specific point of interest", style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
     style={'backgroundColor': '#FFFFFF'},
     children=[html.H4(children="Describe the"),
            dcc.Dropdown(
                id='describe-poi-dropdown-type',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                placeholder="Select point of interest",
            ),
            html.H4(children='called'),
            # another dropdown for names of another poi
            html.H4(children=""),
            dcc.Dropdown(
                id='describe-poi-names',
                style={'width': '60%'},
                value='',
            ),
            html.H4(children=""),
            html.Button('Submit', id='describe-submit', n_clicks=0),
            html.Div(id='describe-output'),
     ]
    ),


    html.H2(children="Discover the historical points of interest according to location", style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),

        dcc.Dropdown(
                id='poi-dropdown',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point of interests type",
            ),
            html.H4(children="located in"),
            dcc.Dropdown(
                id='location-dropdown',
                style={'width': '40%'},
                options=[{'label': l, 'value': l} for l in location],
                value='',
                placeholder="Select location type",
            ),
            html.H4(children=f"{query_1['location-type']}"),
            dcc.Dropdown(
                id='location-town-county-dropdown',
                style={'width': '40%'},
                placeholder="Select location",
            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_1', n_clicks=0),
            html.Div(id='query1-output'),

        ]
    ),

    html.H2(children="Discover the number of historical points of interest according to location",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[

            html.H4(children="Get the number of"),
            dcc.Dropdown(
                id='poi-dropdown-3',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point of interest type",
            ),
            html.H4(children="In all of the"),
            dcc.Dropdown(
                id='location-dropdown-3',
                style={'width': '40%'},
                options=[{'label': l, 'value': l} for l in location],
                value='',
                placeholder="Select location type",
            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_3', n_clicks=0),
            html.H4(children=""),
            html.Div(id='query3-output'),

        ]
    ),

    html.H2(children="Discover other historical points of interests in the same location as a specific historical "
                     "point of interest",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),

            dcc.Dropdown(
                id='poi-dropdown-4',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point of interest type",
            ),
            html.H4(children="in the same"),
            dcc.Dropdown(
                id='location-dropdown-4',
                style={'width': '40%'},
                options=[{'label': l, 'value': l} for l in location],
                value='',
                placeholder="Select location type",
            ),

            html.H4(children="as the point of interest"),

            dcc.Dropdown(
                id='another-poi-dropdown-4',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                placeholder="Select a type of point of interest",
            ),
            # another dropdown for names of another poi
            html.H4(children=""),

            dcc.Dropdown(
                id='choice-poi-dropdown-4',
                style={'width': '60%'},
                placeholder="Select point of interest",
                ),


            html.H4(children=""),
            html.Button('Submit', id='submit_4', n_clicks=0),
            html.Div(id='query4-output'),

        ]
    ),

    html.H2(children="Discover the historical points of interest related to time",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),

            dcc.Dropdown(
                id='poi-dropdown-5',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point of interest type",
            ),
            html.H4(children="Related to the"),
            dcc.Dropdown(
                id='period-dropdown',
                style={'width': '40%'},
                options=[
                    {'label': 'year', 'value': 'year'},
                    {'label': 'historicCentury', 'value': 'historicCentury'},
                    {'label': 'historicalPeriod', 'value': 'historicalPeriod'},
                ],
                value='',
                placeholder="Select time type",
            ),
            html.H4(children=""),
            dcc.Dropdown(
                id='pattern-dropdown',
                style={'width': '40%'},
                value='',
                placeholder="Select time",
            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_5', n_clicks=0),
            html.Div(id='query5-output'),

        ]
    ),

    html.H2(children="Discover the number of historical points of interest related to time",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[

            html.H4(children="Get the number of"),
            dcc.Dropdown(
                id='poi-dropdown-6',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point(s) of interest",
            ),
            html.H4(children="Related to"),
            dcc.Dropdown(
                id='period-dropdown-6',
                style={'width': '40%'},
                options=[
                    {'label': 'year', 'value': 'year'},
                    {'label': 'historicCentury', 'value': 'historicCentury'},
                    {'label': 'historicalPeriod', 'value': 'historicalPeriod'},
                ],
                value='',
                placeholder="Select period",
            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_6', n_clicks=0),
            html.Div(id='query6-output'),

        ]
    ),

    html.H2(children="Discover other historical points of interests in the same time as a specific historical point of interest",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),

            dcc.Dropdown(
                id='poi-dropdown-7',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point(s) of interest",
            ),
            html.H4(children="In the Same"),
            dcc.Dropdown(
                id='period-dropdown-7',
                style={'width': '40%'},
                options=[
                    {'label': 'year', 'value': 'year'},
                    {'label': 'historicCentury', 'value': 'historicCentury'},
                    {'label': 'historicalPeriod', 'value': 'historicalPeriod'},
                ],
                value='',
                placeholder="Select period",
            ),

            html.H4(children="As"),
            dcc.Dropdown(
                id='another-poi-dropdown-7',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                placeholder="Select point of interest",
            ),

            # another dropdown for names of another poi
            html.H4(children=""),
            dcc.Dropdown(
                id='poi-names',
                style={'width': '60%'},

                value='',

            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_7', n_clicks=0),
            html.Div(id='query7-output'),

        ]
    ),

    html.H2(children="Discover historical points of interest in the same location and associated with the same time",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),

            dcc.Dropdown(
                id='poi-dropdown-8',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point(s) of interest",
            ),
            html.H4(children="Located in"),
            dcc.Dropdown(
                id='location-dropdown-8',
                style={'width': '40%'},
                options=[{'label': l, 'value': l} for l in location],
                value='',
                placeholder="Select location type",
            ),
            html.H4(children=""),
            dcc.Dropdown(
                id='location-town-county-dropdown-8',
                style={'width': '40%'},
            ),
            html.H4(children="Associated with"),
            dcc.Dropdown(
                id='period-dropdown-8',
                style={'width': '40%'},
                options=[
                    {'label': 'year', 'value': 'year'},
                    {'label': 'historicCentury', 'value': 'historicCentury'},
                    {'label': 'historicalPeriod', 'value': 'historicalPeriod'},
                ],
                value='',
                placeholder="Select period",
            ),

            html.H4(children=""),
            dcc.Dropdown(
                id='period-pattern-8',
                style={'width': '60%'},

                value='',

            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_8', n_clicks=0),
            html.Div(id='query8-output'),

        ]
    )
])

@app.callback(
    Output('describe-output', 'children'),
    Input('describe-submit', 'n_clicks'),
    State('describe-poi-dropdown-type', 'value'),
    State('describe-poi-names', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, location_type, location):
    describe['location-type'] = location_type
    describe['location'] = location
    details = QueryExecutor().describe(location_type, location)
    if(location_type == 'Museum'):
        museum_blurb = [e['blurb']['value'] for e in details['results']['bindings']]
        museum_phone = [e['phone']['value'] for e in details['results']['bindings']]
        museum_website = [e['website']['value'] for e in details['results']['bindings']]
        data = OrderedDict(
        [
            ("Blurb", museum_blurb),
            ("Phone", museum_phone),
            ("Website", museum_website)
        ]
        )
        df = pd.DataFrame(data)
        data = df.to_dict('records')
        columns = [{'id': c, 'name': c} for c in df.columns]
        return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_data={ 'whiteSpace': 'normal', 'height': 'auto', },
        style_cell={'textAlign': 'left'})

    elif(location_type == 'Landmarks'):

        landmark_website = [e['website']['value'] for e in details['results']['bindings']]
        lanmark_history = [e['propertyHistory']['value'] for e in details['results']['bindings']]
        data = OrderedDict(
        [
            ("Website", landmark_website),
            ("Property History", lanmark_history),
        ]
        )
        df = pd.DataFrame(data)
        data = df.to_dict('records')
        columns = [{'id': c, 'name': c} for c in df.columns]
        return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_data={ 'whiteSpace': 'normal', 'height': 'auto', },
        style_cell={'textAlign': 'left'})

    elif(location_type == 'Walled Towns'):

        walledTown_category = [e['category']['value'] for e in details['results']['bindings']]
        data = OrderedDict(
        [
            ("Category", walledTown_category),
        ]
        )
        df = pd.DataFrame(data)
        data = df.to_dict('records')
        columns = [{'id': c, 'name': c} for c in df.columns]
        return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_data={ 'whiteSpace': 'normal', 'height': 'auto', },
        style_cell={'textAlign': 'left'})

    else: 
        pilgrimPath_duration = [e['duration']['value'] for e in details['results']['bindings']]
        pilgrimPath_difficulty = [e['difficulty']['value'] for e in details['results']['bindings']]
        data = OrderedDict(
        [
            ("Duration", pilgrimPath_duration),
            ("Difficulty", pilgrimPath_difficulty),
        ]
        )
        df = pd.DataFrame(data)
        data = df.to_dict('records')
        columns = [{'id': c, 'name': c} for c in df.columns]
        return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_data={ 'whiteSpace': 'normal', 'height': 'auto', },
        style_cell={'textAlign': 'left'})

@app.callback(
    dash.dependencies.Output('describe-poi-names', 'options'),
    [dash.dependencies.Input('describe-poi-dropdown-type', 'value')],
    prevent_initial_call=True)
def set_poi_options(value):
    if value == 'Museum':
        return museums
    elif value == 'Landmarks':
        return landmarks
    elif value == 'Walled Towns':
        return walledTowns
    else:
        return pilgrimPaths

@app.callback(
    Output('query1-output', 'children'),
    Input('submit_1', 'n_clicks'),
    State('poi-dropdown', 'value'),
    State('location-dropdown', 'value'),
    State('location-town-county-dropdown', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, poi, location_type, location):
    query_1['poi'] = poi
    query_1['location-type'] = location_type
    query_1['location'] = location
    print(f"query 1: {query_1}")

    # Get results of query
    print(poi, location)
    print("HERE: ")


    point_of_interests = QueryExecutor().query_1(poi, location)
    #return f'output: {point_of_interests}'
    # Extract Type, Name and URI
    poi_type = [e['thing']['value'] for e in point_of_interests['results']['bindings']]
    print(poi_type)

    # Format Type
    for i in range(0, len(poi_type), 1):
        print()
        if "dbpedia.org" in poi_type[i]: 
            poi_type[i] = poi_type[i].split("http://dbpedia.org/ontology/", 1)[1]
        else:  poi_type[i] = poi_type[i].split("#", 1)[1]

    poi_name = [e['name']['value'] for e in point_of_interests['results']['bindings']]
    poi_uri = [e['place']['value'] for e in point_of_interests['results']['bindings']]

    print("name", poi_name)
    print(poi_uri)
    print(poi_type)
    # Format the data
    data = OrderedDict(
        [
            ("Type", poi_type),
            ("Name", poi_name),
            ("Uri", poi_uri)
        ]
    )
    df = pd.DataFrame(data)
    data = df.to_dict('records')
    columns = [{'id': c, 'name': c} for c in df.columns]

    # Return Table
    return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'left'})


# callback to chain the dropdowns
@app.callback(
    dash.dependencies.Output('location-town-county-dropdown', 'options'),
    [dash.dependencies.Input('location-dropdown', 'value')],
    prevent_initial_call=True)
def set_cities_options(value):
    return counties if value == 'County' else towns


@app.callback(
    Output('query3-output', 'children'),
    Input('submit_3', 'n_clicks'),
    State('poi-dropdown-3', 'value'),
    State('location-dropdown-3', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, poi, location_type):
    query_3['poi'] = poi
    query_3['location-type'] = location_type
    print(f"query 3: {query_3}")
    output = QueryExecutor().query_2(poi, location_type)


    # Extract Type, Name and URI
    location_names = [e['name']['value'] for e in output['results']['bindings']]
    print(location_names)

    counts = [e['count']['value'] for e in output['results']['bindings']]

    print(counts)

    # Format the data
    data = OrderedDict(
        [
            (location_type, location_names),
            ("Counts", counts),
        ]
    )
    df = pd.DataFrame(data)
    data = df.to_dict('records')
    columns = [{'id': c, 'name': c} for c in df.columns]

    # Return Table
    return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'left'})

    #return f'Max and Min selected point of interests are located in {output["max"][0]} and {output["min"][0]} with a count of {output["max"][1]} and {output["min"][1]} respectively.'


@app.callback(
    Output('query4-output', 'children'),
    Input('submit_4', 'n_clicks'),
    State('poi-dropdown-4', 'value'),
    State('location-dropdown-4', 'value'),
    State('another-poi-dropdown-4', 'value'),
    State('choice-poi-dropdown-4', 'value'),
    prevent_initial_call=True
)

def update_output(n_clicks, poi, location_type, another_poi, choice_poi):

    query_4['poi'] = poi
    query_4['location-type'] = location_type
    query_4['another_poi'] = another_poi
    query_4['name_of_another_poi'] = choice_poi

    # TODO: name of another poi using sparql query

    #print(f"query 4: {query_4}")
    #output = QueryExecutor.query_4(poi, location_type, another_poi, choice_poi)
    #return f'{poi}'

    point_of_interests = QueryExecutor().query_4(poi, location_type, choice_poi)

    #return f'output: {point_of_interests}'
    # Extract Type, Name and URI
    poi_type = [e['POI']['value'] for e in point_of_interests['results']['bindings']]
    print(poi_type)

    # Format Type
    for i in range(0, len(poi_type), 1):
        print()
        if "dbpedia.org" in poi_type[i]: 
            poi_type[i] = poi_type[i].split("http://dbpedia.org/ontology/", 1)[1]
        else:  poi_type[i] = poi_type[i].split("#", 1)[1]

    poi_name = [e['name']['value'] for e in point_of_interests['results']['bindings']]
    poi_uri = [e['place']['value'] for e in point_of_interests['results']['bindings']]

    print("name", poi_name)
    print(poi_uri)
    print(poi_type)
    # Format the data
    data = OrderedDict(
        [
            ("Type", poi_type),
            ("Name", poi_name),
            ("Uri", poi_uri)
        ]
    )
    df = pd.DataFrame(data)
    data = df.to_dict('records')
    columns = [{'id': c, 'name': c} for c in df.columns]

    # Return Table
    return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'left'})
    #return f'Other POIs in same location as selected POI: {output["otherPOIs"]}'
    #return f'POI: {poi}, location type: {location_type}, another poi: {another_poi}, chosen poi: {choice_poi}'


# callback to chain the dropdowns
@app.callback(
    dash.dependencies.Output('choice-poi-dropdown-4', 'options'),
    [dash.dependencies.Input('another-poi-dropdown-4', 'value')],
    prevent_initial_call=True)
def set_cities_options(value):
    if value == 'Museum':
        return museums
    elif value == 'Landmarks':
        return landmarks
    elif value == 'Walled Towns':
        return walledTowns
    else:
        return pilgrimPaths



@app.callback(
    Output('query5-output', 'children'),
    Input('submit_5', 'n_clicks'),
    State('poi-dropdown-5', 'value'),
    State('period-dropdown', 'value'),
    State('pattern-dropdown', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, poi, period, pattern):
    query_5['poi'] = poi
    query_5['associated-with'] = period
    query_5['pattern'] = ''
    print(f"query 5: {query_5}")
    point_of_interests = QueryExecutor().query_5(poi, pattern)
    poi_type = [e['POI']['value'] for e in point_of_interests['results']['bindings']]
    print(poi_type)

    # Format Type
    for i in range(0, len(poi_type), 1):
        print()
        if "dbpedia.org" in poi_type[i]: 
            poi_type[i] = poi_type[i].split("http://dbpedia.org/ontology/", 1)[1]
        else:  poi_type[i] = poi_type[i].split("#", 1)[1]

    poi_name = [e['name']['value'] for e in point_of_interests['results']['bindings']]
    poi_uri = [e['place']['value'] for e in point_of_interests['results']['bindings']]

    print("name", poi_name)
    print(poi_uri)
    print(poi_type)
    # Format the data
    data = OrderedDict(
        [
            ("Type", poi_type),
            ("Name", poi_name),
            ("Uri", poi_uri)
        ]
    )
    df = pd.DataFrame(data)
    data = df.to_dict('records')
    columns = [{'id': c, 'name': c} for c in df.columns]

    # Return Table
    return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'left'})

    #return f'POI: {poi}, associated_with: {period}, pattern: {pattern}'


@app.callback(
    dash.dependencies.Output('pattern-dropdown', 'options'),
    [dash.dependencies.Input('period-dropdown', 'value')],
    prevent_initial_call=True)
def set_cities_options(value):
    if value == 'year':
        return years[2:]
    elif value == 'historicCentury':
        return historicCenturies
    else:
        return historicPeriods


@app.callback(
    Output('query6-output', 'children'),
    Input('submit_6', 'n_clicks'),
    State('period-dropdown-6', 'value'),
    State('poi-dropdown-6', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, period, poi):
    query_6['period'] = period
    query_6['poi'] = poi
    # TODO: max and min poi(s)
    print(f"query 6: {query_6}")
    results = QueryExecutor().query_6(poi, period)
    timePeriod_name = [e['name']['value'] for e in results['results']['bindings']]
    timePeriod_count = [e['count']['value'] for e in results['results']['bindings']]

    data = OrderedDict(
        [
            ("Name", timePeriod_name),
            ("Count", timePeriod_count),
        ]
    )
    df = pd.DataFrame(data)
    data = df.to_dict('records')
    columns = [{'id': c, 'name': c} for c in df.columns]

    # Return Table
    return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'left'})

@app.callback(
    Output('query7-output', 'children'),
    Input('submit_7', 'n_clicks'),
    State('poi-dropdown-7', 'value'),
    State('period-dropdown-7', 'value'),
    State('poi-names', 'value'),
    prevent_initial_call=True
)

def update_output(n_clicks, poi, period_type, another_poi):
    query_7['poi'] = poi
    query_7['period_type'] = period_type
    query_7['another_poi'] = another_poi
    print("another_poi: ", another_poi)

    point_of_interests = QueryExecutor().query_7(poi, period_type, another_poi)
    poi_type = [e['POI1']['value'] for e in point_of_interests['results']['bindings']]
    print(poi_type)

    # Format Type
    for i in range(0, len(poi_type), 1):
        print()
        if "dbpedia.org" in poi_type[i]: 
            poi_type[i] = poi_type[i].split("http://dbpedia.org/ontology/", 1)[1]
        else:  poi_type[i] = poi_type[i].split("#", 1)[1]

    poi_name = [e['name']['value'] for e in point_of_interests['results']['bindings']]
    poi_uri = [e['place']['value'] for e in point_of_interests['results']['bindings']]

    print("name", poi_name)
    print(poi_uri)
    print(poi_type)
    # Format the data
    data = OrderedDict(
        [
            ("Type", poi_type),
            ("Name", poi_name),
            ("Uri", poi_uri)
        ]
    )
    df = pd.DataFrame(data)
    data = df.to_dict('records')
    columns = [{'id': c, 'name': c} for c in df.columns]

    # Return Table
    return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'left'})
   

# callback to chain the dropdowns
@app.callback(
    dash.dependencies.Output('poi-names', 'options'),
    [dash.dependencies.Input('another-poi-dropdown-7', 'value')],
    prevent_initial_call=True)
def set_cities_options(value):
    if value == 'Museum':
        return museums
    elif value == 'Landmarks':
        return landmarks
    elif value == 'Walled Towns':
        return walledTowns
    else:
        return pilgrimPaths


@app.callback(
    Output('query8-output', 'children'),
    Input('submit_8', 'n_clicks'),
    State('poi-dropdown-8', 'value'),
    State('location-dropdown-8', 'value'),
    State('location-town-county-dropdown-8', 'value'),
    State('period-dropdown-8', 'value'),
    State('period-pattern-8', 'value'),

    prevent_initial_call=True
)
def update_output(n_clicks, poi, location_type, location, period, period_pattern):
    print("here" , poi, location_type, location, period, period_pattern)
    results = QueryExecutor().query_8(poi, location_type, location, period, period_pattern)
    print(results)
    poi_type = [e['POI']['value'] for e in results['results']['bindings']]
    print(poi_type)

    # Format Type
    for i in range(0, len(poi_type), 1):
        print()
        if "dbpedia.org" in poi_type[i]:
            poi_type[i] = poi_type[i].split("http://dbpedia.org/ontology/", 1)[1]
        else:
            poi_type[i] = poi_type[i].split("#", 1)[1]

    poi_name = [e['name']['value'] for e in results['results']['bindings']]
    poi_uri = [e['something']['value'] for e in results['results']['bindings']]

    print(poi_name)
    print(poi_uri)

    # Format the data
    data = OrderedDict(
        [
            ("Type", poi_type),
            ("Name", poi_name),
            ("Uri", poi_uri)
        ]
    )
    df = pd.DataFrame(data)
    data = df.to_dict('records')
    columns = [{'id': c, 'name': c} for c in df.columns]

    # Return Table
    return dash_table.DataTable(
        id='table',
        columns=columns,
        data=data,
        style_cell={'textAlign': 'left'})
    #return f'{results}'

 #callback to chain the dropdowns
@app.callback(
    dash.dependencies.Output('period-pattern-8', 'options'),
    [dash.dependencies.Input('period-dropdown-8', 'value')],
    prevent_initial_call=True)
def set_cities_options(value):
    if value == 'year':
        return years[2:]
    elif value == 'historicCentury':
        return historicCenturies
    else:
        return historicPeriods



@app.callback(
    dash.dependencies.Output('location-town-county-dropdown-8', 'options'),
    [dash.dependencies.Input('location-dropdown-8', 'value')],
    prevent_initial_call=True)
def set_cities_options(value):
    return counties if value == 'County' else towns


if __name__ == '__main__':
    app.run_server(debug=True)
