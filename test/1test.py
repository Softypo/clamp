import json

from dash import Dash, dcc, html
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

clamps = pd.read_hdf("data/446/446cd.h5", "446cd")
clamp_types = clamps['type'].unique()


app.layout = html.Div([
    dcc.Dropdown(
        clamp_types,
        clamp_types[1:],
        multi=True,
        searchable=False,
        persistence=True,
        persistence_type='memory',
        id="dropdown_cd",
    ),
    dcc.Graph(id="cd_overview",
              animate=False,
              responsive=True,
              config={'displaylogo': False,
                      'modeBarButtonsToRemove': ['zoom', 'pan2d', 'boxZoom', 'lasso2d', 'select2d']},
              style={'height': '50vh'},
              ),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])


@app.callback(
    Output('hover-data', 'children'),
    Input('cd_overview', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    Input('cd_overview', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    Input('cd_overview', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    Input('cd_overview', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


@ app.callback(Output("cd_overview", "figure"),
               Input("dropdown_cd", "value"),
               #Input("themeToggle", "value"),
               Input('cd_overview', 'relayoutData'),
               State("cd_overview", "figure"),
               )
def clamps_overview(clamps_types, relayoutData, fig):

    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    print(trigger)

    cc = clamps.round(
        {'plot_angle': 2, 'fiber_plot_angle': 2, 'depth': 2}).copy()
    # cc['depth'] = cc['depth']*(-1)

    # update template only
    if trigger == 'themeToggle':
        fig = go.Figure(fig)
        # fig.update_yaxes(autorange="reversed")
        #fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
        return fig

    # update fiver cable only
    elif trigger == 'dropdown_cd':
        fig = go.Figure(fig)
        #fig.layout.shapes = []
        fig.data = [fig.data[0], fig.data[1], fig.data[2]]
        fiber = cc[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                    'fiber_angle_rounded']].loc[cc['type'].isin(clamps_types)]

        # # Add windows
        nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
            ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
                fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

        fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
                                       fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

        # Add traces
        fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
                                 name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))
        fig.update_traces(
            hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
        # fig.update_yaxes(autorange="reversed")
        return fig

    elif trigger == 'cd_overview' and relayoutData is not None:
        print(relayoutData)
        print(fig)
        if 'xaxis.range[1]' in relayoutData and 'yaxis.range[1]' in relayoutData:
            if relayoutData['xaxis.range[0]'] == relayoutData['xaxis.range[1]'] and relayoutData['yaxis.range[0]'] == relayoutData['yaxis.range[1]']:
                fig = go.Figure(fig)
                # fig.update_layout(xaxis=dict(autorange=True),
                #                   yaxis=dict(autorange=True), autosize=True)
                # fig.update_xaxes(autorange=True)
                # fig.update_yaxes(autorange=True)
                fig.update_yaxes(autorange="reversed")
                #fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
                return fig
                #trigger = 'relayoutData'
            else:
                return dash.no_update
        else:
            return dash.no_update

    # update everything
    else:
        fig = go.Figure()
        fiber = cc[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                    'fiber_angle_rounded']].loc[cc['type'].isin(clamps_types)]

        # add delta
        nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
            ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
                fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

        fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
                                       fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

        # Add traces
        for type in cc['type'].unique():
            fig.add_trace(go.Scatter(x=cc.loc[cc['type'] == type, 'plot_angle'], y=cc.loc[cc['type'] == type, 'depth'],
                                     mode='markers', name=type, customdata=cc.loc[cc['type'] == type, ['hadware_name', 'fiber_angle_rounded']]))

        fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
                                 name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))

        fig.update_traces(
            hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
        fig.update_layout(hovermode="y", title="Fiber cable orientation overview", legend_title="Type", legend_orientation="h", yaxis_title="Depth",
                          xaxis_title='AngleFromHighSideClockwiseDegrees', autosize=True, margin=dict(l=0, r=0, b=0, t=50))
        fig.update_yaxes(autorange="reversed")
        # fig.update_xaxes(dtick=20, tickangle=45)
        #fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
        fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
        return fig
    # else:
    #     return dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
