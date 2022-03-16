import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd


# here's the list of possible columns to choose from.
list_of_columns = ['code', 'state', 'category', 'total exports', 'beef', 'pork',
                   'poultry',
                   'dairy', 'fruits fresh', 'fruits proc', 'total fruits',
                   'veggies fresh',
                   'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton']

mycolumn = 'corn'
myheading1 = f"2011 US Agriculture Exports by State"
tabtitle = 'Old McDonald'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/austinlasseter/dash-map-usa-agriculture'

# Set up the chart
df = pd.read_csv('assets/usa-2011-agriculture.csv')

# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

# Render layout
app.layout = html.Div(
    children=[
        html.H1(myheading1),
        html.Div([
            html.Div([
                html.Label("Select a export item for analysis:"),
                dcc.Dropdown(
                    id='selected_item',
                    options=[{'label': v, 'value': v}
                             for v in list_of_columns[3:]],
                    # placeholder='Select a export item for analysis:',
                    style={
                        'width': '100%',
                        'padding': '0px',
                        'font-size': '20px',
                        'text-align-last': 'left'},
                    value=list_of_columns[3],)], className='two columns'),],),
        html.Div([
            dcc.Graph(
                id='figure-1',
                # figure=update_figure()
            ),], className='ten columns'),
        html.A('Code on Github', href=githublink),
        html.Br(),
        html.A("Data Source", href=sourceurl),])

# Connecting the Dropdown values to the graph
@app.callback(
    Output('figure-1', 'figure'),
    [Input('selected_item', 'value')])
def update_figure(v):
    graph_title = f'Exports of {v} in 2011'
    color_scale = 'greens'  # Note: The error message will list possible color
    # scales.
    color_bar_title = 'Millions USD'

    fig = go.Figure(
        data=go.Choropleth(
            locations=df['code'],  # Spatial coordinates
            z=df[v].astype(float),  # Data to be color-coded
            locationmode='USA-states',
            # set of locations match entries in `locations`
            colorscale=color_scale,
            colorbar={'title':color_bar_title},))

    fig.update_layout(
        title_text=graph_title,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)