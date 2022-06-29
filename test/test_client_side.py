import dash
from dash.dependencies import Output, Input, State
from dash import dcc, html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import datetime


# data

clamps = pd.read_pickle("data/446/446cd.pkl")
clamp_types = clamps['type'].unique()


# functions

def clampsoverview_fig(clamp_types, clamps):
    fig = go.Figure()
    cc = clamps.copy()
    fiber = cc[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                'fiber_angle_rounded']].loc[cc['type'].isin(clamp_types)]

    # add delta
    nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
        ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
            fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

    fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
                      fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

    # Add traces
    for type in cc['type'].unique():
        fig.add_trace(go.Scatter(x=cc.loc[cc['type'] == type, 'plot_angle'], y=cc.loc[cc['type'] == type, 'depth'],
                                 mode='markers', name=type, customdata=cc.loc[cc['type'] == type, ['hadware_name', 'angle_rounded']]))

    fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
                             name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))

    fig.update_traces(hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
    fig.update_layout(hovermode="y", title="Fiber cable orientation overview", title_x=0.5, legend_title="Type", legend_orientation="h", yaxis_title="Depth",
                      xaxis_title='AngleFromHighSideClockwiseDegrees', autosize=True, margin=dict(l=80, r=80, b=25, t=50, pad=4), showlegend=False)
    fig.update_yaxes(autorange="reversed")
    fig.layout.modebar = {'orientation': 'v'}
    fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
    return fig


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
    modebar=dict(orientation='v'),
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
        dcc.Store(id='memory', storage_type='memory',
                  data=clampsoverview_fig(clamp_types, clamps)),
        dcc.Input(
            id='input-y',
            placeholder='Insert y value',
            type='number',
            value='',
        ),
        html.Div(id='result'),

        dcc.Graph(id='RandGraph')
    ])
)

# # client side implementation
app.clientside_callback(
    """
    function(relOut, Figure) {
        if (relOut > 5) {
        Figure['layout']['modebar'] = {
                'orientation': 'v',
                'bgcolor': 'salmon',
                'color': 'white',
                'activecolor': '#9ED3CD'};
        }
        return Figure;
    }
    """,
    Output('RandGraph', 'figure'),
    [Input('input-y', 'value')], [State('memory', 'data')]
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


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
