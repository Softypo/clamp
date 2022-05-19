#from dv_dashboard import CONTENT_STYLE
import pandas as pd
# from dash_bootstrap_templates import template_from_url, load_figure_template
import dash_bootstrap_components as dbc
# import dash_labs as dl
import plotly.graph_objects as go
# import plotly.express as px
# import dash_daq as daq
from dash import dcc, html, dash_table, Input, Output, State, callback
import dash

from pil_utilities import loader_pil_multiprocess, loader_pil

from dash import clientside_callback
from dash.dependencies import ClientsideFunction

dash.register_page(__name__, path="/")

CONTENT_STYLE = {
    "marginTop": '8px',
    # "padding": "0.5rem",
    "height": "93vh",
    "minHeight": "20em",
    "display": "flex",
    "flexFlow": "column",
}

# data

# clamps = pd.read_hdf("data/446/446cd.h5", "cd446")
clamps = pd.read_pickle("data/446/446cd.pkl")
clamp_types = clamps['type'].unique()
clamp_imgs = loader_pil('data/446/tubeviews/cdc')


# functions

def clampsoverview_fig(clamp_types, clamps, fiver=True):
    fig = go.Figure()
    cc = clamps.copy()
    fiber = cc[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                'fiberTOH']].loc[cc['type'].isin(clamp_types)]

    # add delta
    nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
        ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
            fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

    fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
                      fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

    # Add traces
    for type in cc['type'].unique():
        fig.add_trace(go.Scatter(x=cc.loc[cc['type'] == type, 'plot_angle'], y=cc.loc[cc['type'] == type, 'depth'],
                                 mode='markers', name=type, customdata=cc.loc[cc['type'] == type, ['hadware_name', 'clampsTOH']].round(0)))
    if fiver:
        fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
                                 name='Fiber Wire', marker_color='crimson', customdata=fiber[['type', 'fiberTOH']].round(0)))

    fig.update_traces(
        hovertemplate='%{customdata[0]}<br>%{customdata[1]} deg (TOH)')
    fig.update_layout(hovermode="y unified", legend_title="Type", legend_orientation="h", yaxis_title="Depth (m)",
                      showlegend=False,
                      xaxis_title='AngleFromHighSideClockwiseDegrees', autosize=True, margin=dict(l=80, r=40, b=25, t=20, pad=4),
                      # title="Fiber cable orientation overview",
                      # title_x=0.5,
                      )
    # fig.update_xaxes(range=[-185, 185])
    fig.update_yaxes(autorange="reversed", ticksuffix=" m")
    fig.layout.modebar = {'orientation': 'v'}
    # fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
    return fig


def clampview_fig(clamp_types, clamp_img, fiver=True):

    # Create figure
    fig = go.Figure()

    # Constants
    img_width = clamp_img.size[0]
    img_height = clamp_img.size[1]
    scale_factor = 0.5

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source=clamp_img)
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    #fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
    return fig


def clampspolar_fig(clamp_types, clamps, fiver=True):
    fig = go.Figure()
    fiber = clamps[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                    'fiberTOH']].loc[clamps['type'].isin(clamp_types)]

    # add delta
    # nogozone_polar = pd.DataFrame([[angle+10, angle-10, depth]
    #                                for angle, depth in fiber[['fiber_plot_angle', 'depth']].values])

    # fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
    #                                fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

    # Add traces
    for type in clamps['type'].unique():
        fig.add_trace(go.Scatterpolar(theta=clamps.loc[clamps['type'] == type, 'plot_angle'], r=clamps.loc[clamps['type'] == type, 'depth'],
                                      mode='markers', name=type, customdata=clamps.loc[clamps['type'] == type, ['type', 'depth', 'clampsTOH']].round(0)))

    # Add traces
    # fig.add_trace(go.Scatterpolar(r=nogozone_polar['depth'], theta=nogozone_polar['fiber_plot_angle'], mode='lines+markers',
    #                               name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))
    if fiver:
        fig.add_trace(go.Scatterpolar(r=fiber['depth'], theta=fiber['fiber_plot_angle'], mode='lines+markers',
                      name='Fiber Wire', marker_color='crimson', customdata=fiber[['type', 'depth', 'fiberTOH']].round(0)))

    fig.update_traces(
        hovertemplate='%{customdata[1]} m<br>%{customdata[2]} deg (TOH)')
    fig.update_layout(title="Fiber cable orientation polarplot",
                      dragmode='turntable',
                      title_x=0.5,
                      legend_title="Type",
                      legend_orientation="h",
                      autosize=True,
                      margin=dict(t=40, b=40, l=40, r=40))
    fig.update_polars(
        hole=0.05,
        radialaxis=dict(
            range=[max(clamps['depth'])+100, min(clamps['depth'])-100]),
        angularaxis=dict(
            dtick=15,
            rotation=90,  # start position of angular axis
            direction="clockwise",
        ))
    # fig.layout.transition = {'duration': 1000, 'easing': 'circle-in-out'}
    return fig


['linear', 'quad', 'cubic', 'sin', 'exp', 'circle',
 'elastic', 'back', 'bounce', 'linear-in', 'quad-in',
 'cubic-in', 'sin-in', 'exp-in', 'circle-in', 'elastic-in',
 'back-in', 'bounce-in', 'linear-out', 'quad-out',
 'cubic-out', 'sin-out', 'exp-out', 'circle-out',
 'elastic-out', 'back-out', 'bounce-out', 'linear-in-out',
 'quad-in-out', 'cubic-in-out', 'sin-in-out', 'exp-in-out',
 'circle-in-out', 'elastic-in-out', 'back-in-out',
 'bounce-in-out']


# body

layout = dbc.Row([
    dcc.Store(id="ctbl", storage_type="memory",
              data=clamps.iloc[:, [0, 1, 4, 5, 6]].to_dict('records')),
    dcc.Store(id="cover", storage_type="memory",
              data=clampsoverview_fig(clamp_types, clamps)),
    dcc.Store(id="cpolar", storage_type="memory",
              data=clampspolar_fig(clamp_types, clamps)),
    dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Overview",
                                    tab_id="overview", key="overview"),
                            dbc.Tab(label="Tubeview",
                                    tab_id="tubeview", key="tubeview"),
                        ],
                        id="card-tabs",
                        active_tab="overview",
                        persistence=True,
                        persistence_type="memory",
                    )
                ),
                dbc.CardBody(
                    id="card-content", className="card-text", style={'height': '100%'}),
            ], style={'height': '100%'}),
            ],
            xl=7, lg=6, md=12, sm=12, xs=12,
            style=CONTENT_STYLE,
            ),
    dbc.Col([
            dbc.Row(
                dcc.Graph(id="cd_polar",
                          animate=False,
                          responsive=True,
                          config={'displaylogo': False,
                                  'doubleClick': 'reset',
                                  # 'scrollZoom': True,
                                  # 'staticPlot': True,
                                  'responsive': True,
                                  'modeBarButtonsToRemove': ['zoom', 'select2d'],
                                  'toImageButtonOptions': {'format': 'png', 'filename': 'Overview', 'height': 600, 'width': 600, 'scale': 3}},
                          style={'minHeight': '20em', 'height': '30vh'},
                          ),
            ),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        clamp_types,
                        clamp_types[1:],
                        multi=True,
                        searchable=False,
                        persistence=True,
                        persistence_type='memory',
                        id="dropdown_cd",
                        style={"width": "100%"},
                    ), width=11,),
                dbc.Col(
                    dcc.Clipboard(
                        id="table_copy",
                        style={
                            "fontSize": 15,
                            "position": "relative",
                            "top": "0.5rem",
                            "right": "0.5rem",
                            # "padding": "50%",
                        },
                    ),
                ), ], style={'height': 'auto'}),
            dbc.Row(
                dash_table.DataTable(id='cd_table',
                                     # clamps.iloc[:, [0, 1, 4, 5, 6]].to_dict('records'),
                                     page_action='native',
                                     sort_action='native',
                                     style_as_list_view=True,
                                     fixed_rows={'headers': True, 'data': 0},
                                     style_table={
                                         'minHeight': '10%', 'height': '100%', 'maxHeight': '100%',
                                         'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto'},
                                        style_header={
                                            'text-align': 'left', 'fontWeight': 'bold', 'fontSize': '0.8em', 'font-style': 'italic'},
                                        style_cell={
                                            'text-align': 'left', 'fontSize': '1em'},
                                        style_data_conditional=[
                                         {
                                             'if': {'row_index': 'even'},
                                             'backgroundColor': 'slategrey',
                                         }
                                     ],
                                     ), style={'height': '100%'}),
            ],
            xl=5, lg=6, md=12, sm=12, xs=12,
            style=CONTENT_STYLE,
            ),
])


tabs = {'overview': [
    # dcc.Dropdown(
    #     clamp_types,
    #     clamp_types[1:],
    #     multi=True,
    #     searchable=False,
    #     persistence=True,
    #     persistence_type='memory',
    #     id="dropdown_cd",
    # ),
    dcc.Graph(id="cd_overview",
              # figure=clampsoverview_fig(clamp_types, clamps, False),
              animate=False,
              responsive=True,
              config={'displaylogo': False,
                      'modeBarButtonsToRemove': ['zoom', 'pan2d', 'boxZoom', 'lasso2d', 'select2d', 'resetScale2d'],
                      'toImageButtonOptions': {'format': 'png', 'filename': 'Overview', 'height': 1080, 'width': 600, 'scale': 3}},
              style={'height': '100%'},
              ),
],
    'tubeview': [
    # dcc.Dropdown(
    #     clamp_types,
    #     clamp_types[1:],
    #     multi=True,
    #     searchable=False,
    #     persistence=True,
    #     persistence_type='memory',
    #     id="dropdown_cd2",
    # ),
    dcc.Graph(id="cd_view",
              figure=clampview_fig(
                  clamp_types, clamp_imgs['clamp_clampCDC1'], fiver=True),
              animate=False,
              responsive=True,
              config={'displaylogo': False,
                      'doubleClick': 'reset',
                      'modeBarButtonsToRemove': ['zoom', 'pan2d', 'boxZoom', 'lasso2d', 'select2d', 'resetScale2d'],
                      'toImageButtonOptions': {'format': 'png', 'filename': 'Overview', 'height': 1080, 'width': 600, 'scale': 3}},
              style={'height': '100%'},
              ),
    # dbc.Carousel(
    #     items=[
    #         {"key": "1", "src": "data/446/tubeviews/cdc/clamp_clampCDC1.jpeg"}
    #         {"key": "2", "src": "/static/images/slide2.svg"},
    #         {"key": "3", "src": "/static/images/slide3.svg"},
    #     ],
    #     controls=True,
    #     indicators=True,
    # ),

]
}


# callbacks

@ callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")])
def tab_content(active_tab):
    return tabs[active_tab]


# @ callback(
#     Output("cd_table", "data"),
#     Input("dropdown_cd", "value"),
# )
# def filterclamps_table(value):
#     return clamps[clamps.type.isin(value)].iloc[:, [0, 1, 4, 5, 6]].round(3).to_dict('records')


clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="clampstable_listener"
    ),
    Output("cd_table", "data"),
    Input("dropdown_cd", "value"),
    Input("ctbl", "data"),
    State("cd_table", "data"),
)


# @ callback(
#     Output("table_copy", "content"),
#     Input("table_copy", "n_clicks"),
#     State("cd_table", "data"),
# )
# def customcopy_table(_, data):
#     # See options for .to_csv() or .to_excel() or .to_string() in the  pandas documentation
#     return pd.DataFrame(data).to_csv(index=False)  # includes headers

clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="clampstable_tocsv"
    ),
    Output("table_copy", "content"),
    Input("table_copy", "n_clicks"),
    State("cd_table", "data"),
)


clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="clampsoverview_listener"
    ),
    Output("cd_overview", "figure"),
    Input("dropdown_cd", "value"),
    # Input("themeToggle", "value"),
    # Input("unitsToggle", "value"),
    Input('cd_overview', 'relayoutData'),
    Input("cover", "data"),
    State('cd_overview', 'figure'),
    # State("themes", "data"),
)

clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="clampspolar_listener"
    ),
    Output("cd_polar", "figure"),
    Input("dropdown_cd", "value"),
    Input('cd_overview', 'relayoutData'),
    Input("cpolar", "data"),
    State('cd_polar', 'figure'),
    # State("themes", "data"),
)

clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="cstore_switcher",
    ),
    Output("ctbl", "data"),
    Output("cover", "data"),
    Output("cpolar", "data"),
    Input("themeToggle", "value"),
    Input("unitsToggle", "value"),
    State("ctbl", "data"),
    State("cover", "data"),
    State("cpolar", "data"),
    State("themes", "data"),
)

# clientside_callback(
#     """
#     function(themeToggle, Figure) {
#         if (themeToggle) {
#         Figure['layout']['modebar'] = {
#                 'orientation': 'v',
#                 'bgcolor': 'salmon',
#                 'color': 'white',
#                 'activecolor': '#9ED3CD'};
#         }
#         else{
#         Figure['layout']['modebar'] = {
#             'orientation': 'v',
#             'bgcolor': 'red',
#             'color': 'white',
#             'activecolor': '#9ED3CD'};
#         }
#         return Figure;
#     }
#     """,
#     (Output("cd_overview", "figure"),
#      # Input("dropdown_cd", "value"),
#      Input("themeToggle", "value"),
#      State("cover", "data"),
#      # State("themes", "data"),
#      ),
# )

# @ callback(Output("cd_overview", "figure"),
#            Input("dropdown_cd", "value"),
#            Input("themeToggle", "value"),
#            Input('cd_overview', 'relayoutData'),
#            State("cd_overview", "figure"),
#            prevent_initial_call=True)
# def clampsoverview_listener(clamps_types, themeToggle, relayoutData, fig):

#     trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

#     cc = clamps.copy()

#     print('trigger: ', trigger)
#     print('relayout: ', relayoutData)

#     # update template only
#     if trigger == 'themeToggle':
#         print("themeToggle")
#         fig = go.Figure(fig)
#         # fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
#         if themeToggle:
#             fig.layout.template = themes['_light']['fig']
#             fig.layout.modebar = {
#                 'orientation': 'v',
#                 'bgcolor': 'salmon',
#                 'color': 'white',
#                 'activecolor': '#9ED3CD'}
#         else:
#             fig.layout.template = themes['_dark']['fig']
#             fig.layout.modebar = {
#                 'orientation': 'v',
#                 'bgcolor': 'rgb(39, 43, 48)',
#                 'color': 'white',
#                 'activecolor': 'grey'}
#             fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
#         return fig

#     # update fiver cable only
#     elif trigger == 'dropdown_cd':
#         print('update fiver cable only')
#         fig = go.Figure(fig)
#         fig.layout.shapes = []
#         fig.data = [fig.data[0], fig.data[1], fig.data[2]]
#         fiber = cc[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
#                     'fiber_angle_rounded']].loc[cc['type'].isin(clamps_types)]

#         # # Add windows
#         nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
#             ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
#                 fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

#         fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
#                                        fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

#         # Add traces
#         fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
#                                  name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))
#         fig.update_traces(
#             hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
#         # fig.update_yaxes(autorange="reversed")
#         return fig

#     # elif trigger == 'cd_overview':
#     #     try:
#     #         if relayoutData['xaxis.range[0]'] == relayoutData['xaxis.range[1]'] and relayoutData['yaxis.range[0]'] == relayoutData['yaxis.range[1]']:
#     #             print(
#     #                 'xaxis.range[0] == xaxis.range[1] and yaxis.range[0] == yaxis.range[1]')
#     #             fig = go.Figure(fig)
#     #             fig.update_yaxes(autorange="reversed")
#     #             return fig
#     #     except:
#     #         return dash.no_update
#     # fix right click bug
#     elif trigger == 'cd_overview' and fig is not None:
#         print('fixing right click bug')
#         #print('fig: ', fig)
#         if relayoutData is not None:
#             print('len: ', len(relayoutData))
#             if len(relayoutData) > 1:
#                 print('len > 1')
#                 if 'xaxis.range[1]' in relayoutData and 'yaxis.range[1]' in relayoutData:
#                     print('xaxis.range[1] and yaxis.range[1]')
#                     if relayoutData['xaxis.range[0]'] == relayoutData['xaxis.range[1]'] and relayoutData['yaxis.range[0]'] == relayoutData['yaxis.range[1]']:
#                         print(
#                             'xaxis.range[0] == xaxis.range[1] and yaxis.range[0] == yaxis.range[1]')
#                         fig = go.Figure(fig)
#                         fig.update_yaxes(autorange="reversed")
#                         return fig
#                     else:
#                         return dash.no_update
#                 else:
#                     return dash.no_update
#             else:
#                 return dash.no_update
#         else:
#             return dash.no_update

#     # update everything
#     else:
#         print('update everything')
#         fig = go.Figure()
#         fiber = cc[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
#                     'fiber_angle_rounded']].loc[cc['type'].isin(clamps_types)]

#         # add delta
#         nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
#             ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
#                 fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

#         fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
#                                        fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

#         # Add traces
#         for type in cc['type'].unique():
#             fig.add_trace(go.Scatter(x=cc.loc[cc['type'] == type, 'plot_angle'], y=cc.loc[cc['type'] == type, 'depth'],
#                                      mode='markers', name=type, customdata=cc.loc[cc['type'] == type, ['hadware_name', 'angle_rounded']]))

#         fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
#                                  name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))

#         fig.update_traces(
#             hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
#         fig.update_layout(hovermode="y", title="Fiber cable orientation overview", title_x=0.5, legend_title="Type", legend_orientation="h", yaxis_title="Depth",
#                           xaxis_title='AngleFromHighSideClockwiseDegrees', autosize=True, margin=dict(l=0, r=0, b=0, t=50), showlegend=False)
#         fig.update_yaxes(autorange="reversed")
#         # fig.update_xaxes(dtick=20, tickangle=45)
#         # fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
#         fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
#         if themeToggle:
#             fig.layout.template = themes['_light']['fig']
#             fig.layout.modebar = {
#                 'orientation': 'v',
#                 'bgcolor': 'salmon',
#                 'color': 'white',
#                 'activecolor': '#9ED3CD'}
#         else:
#             fig.layout.template = themes['_dark']['fig']
#             fig.layout.modebar = {
#                 'orientation': 'v',
#                 'bgcolor': 'rgb(39, 43, 48)',
#                 'color': 'white',
#                 'activecolor': 'grey'}
#         return fig


# @ callback(Output("cd_polar", "figure"),
#            Input("dropdown_cd", "value"),
#            Input("themeToggle", "value"),
#            # State("cd_overview", "figure"),
#            )
# def clampspolar_listener(clamps_types, themeToggle):
#     fig = go.Figure()
#     fiber = clamps[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
#                     'fiberTOH']].loc[clamps['type'].isin(clamps_types)]

#     # add delta
#     nogozone_polar = pd.DataFrame([[angle+10, angle-10, depth]
#                                    for angle, depth in fiber[['fiber_plot_angle', 'depth']].values])

#     # fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
#     #                                fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

#     # Add traces
#     for type in clamps['type'].unique():
#         fig.add_trace(go.Scatterpolar(theta=clamps.loc[clamps['type'] == type, 'plot_angle'], r=clamps.loc[clamps['type'] == type, 'depth'],
#                                       mode='markers', name=type, customdata=clamps.loc[clamps['type'] == type, ['hadware_name', 'clampsTOH']].round(0)))

#     # Add traces
#     # fig.add_trace(go.Scatterpolar(r=nogozone_polar['depth'], theta=nogozone_polar['fiber_plot_angle'], mode='lines+markers',
#     #                               name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))
#     fig.add_trace(go.Scatterpolar(r=fiber['depth'], theta=fiber['fiber_plot_angle'], mode='lines+markers',
#                                   name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiberTOH']].round(0)))
#     fig.update_traces(hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
#     fig.update_layout(title="Fiber cable orientation polarplot", title_x=0.5,
#                       legend_title="Type", legend_orientation="h", autosize=True, margin=dict(t=50, b=40, l=40, r=40))
#     fig.update_polars(
#         hole=0.05,
#         radialaxis=dict(
#             range=[max(clamps['depth'])+100, min(clamps['depth'])-100]),
#         angularaxis=dict(
#             dtick=15,
#             rotation=90,  # start position of angular axis
#             direction="clockwise",
#         ))
#     # fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
#     if themeToggle:
#         fig.layout.template = themes['_light']['fig']
#         fig.layout.modebar = {
#             'orientation': 'v',
#             'bgcolor': 'salmon',
#             'color': 'white',
#             'activecolor': '#9ED3CD'}
#     else:
#         fig.layout.template = themes['_dark']['fig']
#         fig.update_polars(bgcolor='rgb(58, 63, 68)')
#         fig.layout.modebar = {
#             'orientation': 'v',
#             'bgcolor': 'rgb(39, 43, 48)',
#             'color': 'white',
#             'activecolor': 'grey'}
#     # fig.layout.transition = {'duration': 1000, 'easing': 'circle-in-out'}
#     return fig
