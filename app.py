from collections import OrderedDict

import dash
import pandas as pd
from dash import dcc, dash_table
from dash import html
from dash.dependencies import Input, Output, State
from Query_executor import QueryExecutor

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
towns = data[1]
museums = data[2]
landmarks = data[3]
walledTowns = data[4]
pilgrimPaths = data[5]
historicPeriods = data[6]

historicCenturies = data[7]

years = data[8]


app.layout = html.Div([

    html.Div(

        style={'backgroundColor': '#1d6b01', 'position': 'center', 'height': '20vh'},
        children=[
            html.H2(children='Irish History Knowledge Graph Application',
                    style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh', 'color': 'white'})
        ]
    ),
    html.H2(children="Discover Historical Sites According to Location", style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
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

    html.H2(children="Discover the Locations with the Max and Min Historical Points of Interest",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),
            dcc.Dropdown(
                id='location-dropdown-3',
                style={'width': '40%'},
                options=[{'label': l, 'value': l} for l in location],
                value='',
                placeholder="Select location type",
            ),
            html.H4(children="with the max and min"),
            dcc.Dropdown(
                id='poi-dropdown-3',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point of interest type",
            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_3', n_clicks=0),
            html.Div(id='query3-output'),

        ]
    ),

    html.H2(children="Find Other Historical Points of Interests near a Specific Historical Point of Interest",
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

    html.H2(children="Discover Historical Sites According to Time",
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

    html.H2(children="Find the time period with Max and Min Historical Points of Interest ",
            style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),
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
            html.H4(children="with max and min"),
            dcc.Dropdown(
                id='poi-dropdown-6',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point(s) of interest",
            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_6', n_clicks=0),
            html.Div(id='query6-output'),

        ]
    ),

    html.H2(children="Discover other Historical Points of Interest in the same time period as a Specific Historical Point "
                     "of Interest",
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

    html.H2(children="Discover Historical Points of Interest located in a region associated with a specific time period",
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
    ),


    html.H2(
        children="Discover Points of interest located in a region associated with a time period same as a Specific Point of Interest",
        style={'textAlign': 'center', 'verticalAlign': 'middle', 'line-height': '20vh'}),
    html.Div(
        style={'backgroundColor': '#FFFFFF'},
        children=[
            html.H4(children="Get the"),

            dcc.Dropdown(
                id='poi-dropdown-9',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                multi=True,
                placeholder="Select point(s) of interest",
            ),
            html.H4(children="located in"),
            dcc.Dropdown(
                id='location-dropdown-9',
                style={'width': '40%'},
                options=[{'label': l, 'value': l} for l in location],
                value='',
                placeholder="Select location type",
            ),

            html.H4(children="and associated with the"),
            dcc.Dropdown(
                id='period-dropdown-9',
                style={'width': '40%'},
                options=[
                    {'label': 'year', 'value': 'year'},
                    {'label': 'historicCentury', 'value': 'historicCentury'},
                    {'label': 'historicalPeriod', 'value': 'historicalPeriod'},
                ],
                value='',
                placeholder="Select period",
            ),
            html.H4(children="of"),

            dcc.Dropdown(
                id='another-poi-dropdown-9',
                style={'width': '60%'},
                options=[{'label': poi, 'value': poi} for poi in points_of_interest],
                value='',
                placeholder="Select point of interest",
            ),
            # another dropdown for names of another poi
            html.H4(children=""),
            dcc.Dropdown(
                id='poi-names-9',
                style={'width': '60%'},
                value='',

            ),
            html.H4(children=""),
            html.Button('Submit', id='submit_9', n_clicks=0),
            html.Div(id='query9-output'),

        ]
    )

])


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
    point_of_interests = QueryExecutor().query_1(poi, location)
    #Extract Type, Name and URI
    poi_type = [e['thing']['value'] for e in point_of_interests['results']['bindings']]
    # Format Type
    for i in range(0, len(poi_type), 1):
        print()
        poi_type[i] = poi_type[i].split("#", 1)[1]
    poi_name = [e['name']['value'] for e in point_of_interests['results']['bindings']]
    poi_uri = [e['place']['value'] for e in point_of_interests['results']['bindings']]

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

    return f'Max and Min selected point of interests are located in {output["max"][0]} and {output["min"][0]} with a count of {output["max"][1]} and {output["min"][1]} respectively.'


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

    print(f"query 4: {query_4}")
    #output = QueryExecutor.query_4(poi, location_type, another_poi, choice_poi)
    #return f'{poi}'
    return f'output: {QueryExecutor().query_4(poi, location_type, choice_poi)}'
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
    return f'POI: {poi}, associated_with: {period}, pattern: {pattern}'


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
    return f'period: {period}, poi(s): {poi}"'


@app.callback(
    Output('query7-output', 'children'),
    Input('submit_7', 'n_clicks'),
    State('poi-dropdown-7', 'value'),
    State('period-dropdown-7', 'value'),
    State('another-poi-dropdown-7', 'value'),
    prevent_initial_call=True
)
def update_output(n_clicks, poi, period_type, another_poi):
    query_7['poi'] = poi
    query_7['period_type'] = period_type
    query_7['another_poi'] = another_poi

    # TODO: name of another poi using sparql query

    print(f"query 7: {query_7}")
    return f'POI: {poi}, period type: {period_type}, another poi: {another_poi}'

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

    prevent_initial_call=True
)
def update_output(n_clicks, poi, location_type, location, period):
    print(poi, location_type, location, period)
    return f'POI: {poi}, location type: {location_type}, location: {location} period type: {period}'

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


@app.callback(
    Output('query9-output', 'children'),
    Input('submit_9', 'n_clicks'),
    State('poi-dropdown-9', 'value'),
    State('location-dropdown-9', 'value'),
    State('period-dropdown-9', 'value'),
    State('another-poi-dropdown-9', 'value'),

    prevent_initial_call=True
)
def update_output(n_clicks, poi, location_type, period, another_poi):
    print(poi, location_type, location, period)
    return f'POI: {poi}, location type: {location_type}, period type: {period}, another_poi: {another_poi}'

@app.callback(
    dash.dependencies.Output('poi-names-9', 'options'),
    [dash.dependencies.Input('another-poi-dropdown-9', 'value')],
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



if __name__ == '__main__':
    app.run_server(debug=True)
