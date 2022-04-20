import dash
from dash.dependencies import Output, Input, State
from dash import dcc, html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import datetime

# some random values
a = datetime.datetime.today()
numdays = 100
dateList = []
for x in range(0, numdays):
    dateList.append(a - datetime.timedelta(days=x))
xy = [dateList, np.random.rand(100)]
df = pd.DataFrame(data=xy[1], columns=["y"], index=xy[0])


# Graph data
dataS = [dict(
    x=df.index,
    y=df['y'],
    name='meter',
    mode='lines'
)]

# Graph layout
layoutS = go.Layout(
    title="Meter",
    xaxis=dict(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    ),
    yaxis=dict(range=[0, 2])
)

# Dash app layout
app = dash.Dash()
app.title = 'Random'

app.layout = html.Div(
    html.Div([
        html.H1(children='Random nums'),
        html.Div(children='''
            Rand rand rand.
        '''),

        dcc.Input(
            id='input-y',
            placeholder='Insert y value',
            type='number',
            value='',
        ),
        html.Div(id='result'),

        dcc.Graph(id='RandGraph', figure=dict(data=dataS, layout=layoutS))
    ])
)

# # client side implementation
app.clientside_callback(
    """
    function(relOut, Figure) {
        if (typeof relOut !== 'undefined') {
            if (typeof relOut["xaxis.range"] !== 'undefined') {
                //get active filter from graph
                fromS = new Date(relOut["xaxis.range"][0]).getTime()
                toS = new Date(relOut["xaxis.range"][1]).getTime()

                xD = Figure.data[0].x
                yD = Figure.data[0].y

                //filter y data with graph display
                yFilt = xD.reduce(function (pV,cV,cI){
                    sec = new Date(cV).getTime()
                    if (sec >= fromS && sec <= toS) {
                        pV.push(yD[cI])
                    }
                    return pV
                }, [])

                yMax = Math.max.apply(Math, yFilt)
                yMin = Math.min.apply(Math, yFilt)
            } else {
                yMin = Math.min.apply(Math, Figure.data[0].y)
                yMax = Math.max.apply(Math, Figure.data[0].y)
            }
        } else {
            yMin = Math.min.apply(Math, Figure.data[0].y)
            yMax = Math.max.apply(Math, Figure.data[0].y)
        }
        Figure.layout.yaxis = {
            'range': [yMin,yMax],
            'type': 'linear'
        }
        return {'data': Figure.data, 'layout': Figure.layout};
    }
    """,
    Output('RandGraph', 'figure'),
    [Input('RandGraph', 'relayoutData')], [State('RandGraph', 'figure')]
)

# Server side implementation (slow)


# @app.callback(
#     Output('RandGraph', 'figure'),
#     [Input('RandGraph', 'relayoutData')], [State('RandGraph', 'figure')]
# )
# def update_result(relOut, Fig):
#     ymin = df.loc[relOut['xaxis.range'][1]:relOut['xaxis.range'][0], 'y'].min()
#     ymax = df.loc[relOut['xaxis.range'][1]:relOut['xaxis.range'][0], 'y'].max()
#     newLayout = go.Layout(
#         title="OL Meter",
#         xaxis=dict(
#             rangeslider_visible=True,
#             rangeselector=dict(
#                 buttons=list([
#                     dict(count=0, label="1m", step="month", stepmode="backward"),
#                     dict(count=6, label="6m", step="month", stepmode="backward"),
#                     dict(count=1, label="YTD", step="year", stepmode="todate"),
#                     dict(count=1, label="1y", step="year", stepmode="backward"),
#                     dict(count=5, label="5y", step="year", stepmode="backward"),
#                     dict(step="all")
#                 ])
#             ),
#             range=relOut['xaxis.range']
#         ),
#         yaxis=dict(range=[ymin, ymax])
#     )

#     Fig['layout'] = newLayout
#     return Fig


# if __name__ == '__main__':
#     app.run_server(debug=True, port=8888)
