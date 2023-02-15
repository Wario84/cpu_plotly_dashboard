import dash
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd
import plotly.graph_objs as go # for the pie chart
import plotly.express as px # for the scatter plot

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Load the dataset
#df = pd.read_csv("test_cpus.csv")
df = pd.read_csv("https://raw.githubusercontent.com/Wario84/blog/main/assets/data/test_cpus.csv")

app.layout = html.Div([
    html.H1('CPU Benchmark Data'),
    html.Hr(),
    html.H3('Data Preview:'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(10).to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        sort_action='native',
        page_action='none',
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }]
    ),
    html.Br(),
    html.H4('Histogram variable:'),
    dcc.Dropdown(
        id='variable-selector',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='cpu_value(higher_is_better)'
    ),
    dcc.RadioItems(
        id='sort-order',
        options=[{'label': i, 'value': i} for i in ['Ascending', 'Descending']],
        value='Ascending',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(
        id='histogram',
        figure={}
    ),
        html.Br(),
    html.H4('Pie-chart variable:'),
     dcc.Dropdown(
                id="variable-selector-2",
                options=[
                    {"label": "Ghz", "value": "ghz"},
                    {"label": "Cores", "value": "cores"},
                    {"label": "Threads", "value": "threads"},
                    {"label": "Year", "value": "year"},
                    #"ghz","cores","threads"

                ],
                #style={"width": "45%"}
                value="cores"
                
            ),
             dcc.Graph(id="pie-chart"),
             html.Br(),
    html.H4('Scatter-Plot variable:'),
    dcc.Dropdown(
        id='variable-selector-3',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='cpu_name'
    ),
             
             dcc.Graph(id="scatter-plot"),
])

@app.callback(
    [dash.dependencies.Output('histogram', 'figure'),
     dash.dependencies.Output('table', 'data')],
    [dash.dependencies.Input('variable-selector', 'value'),
     dash.dependencies.Input('sort-order', 'value')]
)
def update_histogram_and_table(variable, sort_order):
    df_sorted = df.sort_values(by='cpu_value(higher_is_better)', ascending=False)
    if sort_order == 'Ascending':
        df_sorted = df_sorted.iloc[::-1]
    data_table = df_sorted.head(10).to_dict('records')

    fig = {
        'data': [{
            'x': df[variable],
            'type': 'histogram'
        }],
        'layout': {
            'title': 'Histogram of ' + variable,
            'xaxis': {'title': variable},
            'yaxis': {'title': 'Count'}
        }
    }

    return fig, data_table

@app.callback(
    dash.dependencies.Output("pie-chart", "figure"),
    [dash.dependencies.Input("variable-selector-2", "value")]
)

def update_pie_chart(selected_column):
    #filtered_df = df[df['year'] == selected_column]
    values = df[selected_column].value_counts().values
    labels = df[selected_column].value_counts().index
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    #fig.update_layout(title=f"{selected_column} distribution in {selected_column}")
    return fig

@app.callback(
    dash.dependencies.Output("scatter-plot", "figure"),
    [dash.dependencies.Input("variable-selector-3", "value")]
)
def update_scatter_plot(variable):
    return px.scatter(df, x="price_usd", y=variable).update_layout(
        xaxis={"title": "Price (USD)"},
        yaxis={"title": variable.capitalize()},
        margin={"l": 40, "b": 40, "t": 10, "r": 10},
        height=300,
    )

if __name__ == '__main__':
    app.run_server(debug=False)
