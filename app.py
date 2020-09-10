import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from itertools import product


# -------------------------- PYTHON FUNCTIONS ---------------------------- #

class Room:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.coordinates_dict = dict.fromkeys(product(range(length + 1), range(width + 1)), 'Empty')
        self.person_count = 0
        self.add_person(Person((0, 0)))

    def add_person(self, person):
        """Adds a person to the room if no one else in the person's safety perimeter"""
        checks = [check for check in person.buffer if check in self.coordinates_dict.keys()]
        person_checks = []
        for buffer_check in checks:
            if isinstance(self.coordinates_dict.get(buffer_check), Person):
                person_checks.append(True)
            else:
                person_checks.append(False)
        if any(person_checks):
            return False
        else:
            self.coordinates_dict.update({person.location: person})
            self.person_count += 1
            return True

    def maximise_people(self):
        """Add people to the room until no more can be added safely"""
        while True:
            coords = self.coordinates_dict.keys()
            available = [position for position in coords if not isinstance(self.coordinates_dict.get(position), Person)]
            for space in available:
                person_added = self.add_person(Person(space))
                if person_added is True:
                    continue
            break
        return self.person_count


class Person:
    def __init__(self, location):
        self.location = location
        self.buffer = self.buffer_coordinates()

    def buffer_coordinates(self):
        """Define 1m buffer around coordinates to check for other people"""
        buffer_coords = []
        adjustments = [(0, 1), (0, -1), (1, 0), (1, -1), (-1, 0), (-1, 1), (-1, -1), (1, 1)]
        for adjustment in adjustments:
            adj_length, adj_width = adjustment
            coord_length, coord_width = self.location
            buffer_coords.append((coord_length + adj_length, coord_width + adj_width))
        return buffer_coords


# -------------------------- DASH ---------------------------- #
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

# -------------------------- PROJECT DASHBOARD ---------------------------- #
app.layout = html.Div(children=[
    html.H1(children='Room Capacity Calculator'),
    html.H3(children='''Not to be used to belittle hospital support staff!'''),

    html.Br(),

    html.Div(children='''Please enter the room dimensions in meters'''),

    html.Div(dcc.Input(id='input-on-length', type='number', placeholder='Length', value=2)),

    html.Div(dcc.Input(id='input-on-width', type='number', placeholder='Width', value=2)),

    html.Br(),

    dcc.Graph(id='example-graph'),

])


@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input('input-on-length', 'value'),
     Input('input-on-width', 'value')]
)
def create_graph(length, width):
    room = Room(length, width)
    max_people = room.maximise_people()
    coordinates = [coords for coords in room.coordinates_dict.keys() if room.coordinates_dict.get(coords) != 'Empty']
    X = list()
    Y = list()
    for x, y in coordinates:
        X.append(x)
        Y.append(y)

    fig = go.Figure()

    fig.add_shape(type="rect", xref="x", yref="y",
                  x0=0, y0=0, x1=room.length, y1=room.width,
                  line=dict(color="RoyalBlue", width=3, ), fillcolor="LightSkyBlue", )

    fig.update_shapes(dict(
        opacity=0.5,
        xref="x",
        yref="y",
        layer="below"
    ))

    fig.update_layout(title=f"Max Capacity = {max_people}")

    fig.add_trace(go.Scatter(
        mode='markers',
        x=X,
        y=Y,
        marker=dict(
            color='Red',
            size=10,
            line=dict(
                color='MediumPurple',
                width=2
            ))
    ))
    return fig


# -------------------------- MAIN ---------------------------- #

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
