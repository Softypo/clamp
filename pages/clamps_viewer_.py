from dv_dashboard import themes, CONTENT_STYLE
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url, load_figure_template
import dash_bootstrap_components as dbc
import dash_labs as dl
import plotly.graph_objects as go
import plotly.express as px
import dash_daq as daq
from dash import dcc, html, dash_table, Input, Output, State, callback
import dash

dash.register_page(__name__, path="/")

# data

clamps = pd.read_hdf("data/446/446cd.h5", "446cd")
clamp_types = clamps['type'].unique()

# body


layout = html.Div(
    [
        # dbc.Row([
        #         dbc.Col([
        #             html.P("Settings", className="offcanvas-title h5"), ],
        #             xl=12, lg=12, md=12, sm=12, xs=12,),
        #         ], className="mt-2"),
        dbc.Row([
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
                        dbc.CardBody(id="card-content", className="card-text"),
                    ],)
                    ],
                xl=7, lg=6, md=12, sm=12, xs=12,
                #style={"padding-right": "0.2rem"},
                    ),
            dbc.Col([
                dcc.Dropdown(
                    clamp_types,
                    clamp_types[1:],
                    multi=True,
                    searchable=False,
                    persistence=True,
                    persistence_type='memory',
                    id="dropdown_cd",
                ),
                dcc.Graph(id="cd_polar", animate=False,
                          config={'displaylogo': False},
                          style={'height': '30vh'},),
                dash_table.DataTable(clamps.to_dict('records'),
                                     id='cd_table',
                                     page_action='none',
                                     sort_action='native',
                                     style_as_list_view=True,
                                     fixed_rows={'headers': True, 'data': 0},
                                     style_table={'minHeight': 'auto', 'height': '55vh', 'maxHeight': '100vh',
                                                  'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto'},
                                     )
            ],
                xl=5, lg=6, md=12, sm=12, xs=12,
                #style={"padding-left": "0.2rem"},
            ),
        ],),
    ],
    style=CONTENT_STYLE,)


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
              animate=False,
              responsive=True,
              config={'displaylogo': False,
                      'modeBarButtonsToRemove': ['zoom', 'pan2d', 'boxZoom', 'lasso2d', 'select2d']},
              style={'height': '80vh'},
              ),
],
    'tubeview': [
    dcc.Dropdown(
        clamp_types,
        clamp_types[1:],
        multi=True,
        searchable=False,
        persistence=True,
        persistence_type='memory',
        id="dropdown_cd2",
    ),
    dcc.Graph(id="cd_overview2",
              animate=False,
              config={'displaylogo': False},
              style={'height': '80vh'},
              ),
]
}


# callbacks

@ callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    return tabs[active_tab]


@ callback(Output("cd_overview", "figure"),
           Input("dropdown_cd", "value"),
           Input("themeToggle", "value"),
           Input('cd_overview', 'relayoutData'),
           State("cd_overview", "figure"),
           )
def clamps_overview(clamps_types, themeToggle, relayoutData, fig):

    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    cc = clamps.copy()

    # update template only
    if trigger == 'themeToggle':
        fig = go.Figure(fig)
        fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
        return fig

    # update fiver cable only
    elif trigger == 'dropdown_cd':
        fig = go.Figure(fig)
        fig.layout.shapes = []
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
        fig.update_yaxes(autorange="reversed")
        return fig

    # fix right click bug
    elif trigger == 'cd_overview' and relayoutData is not None:
        if 'xaxis.range[1]' in relayoutData and 'yaxis.range[1]' in relayoutData:
            if relayoutData['xaxis.range[0]'] == relayoutData['xaxis.range[1]'] and relayoutData['yaxis.range[0]'] == relayoutData['yaxis.range[1]']:
                fig = go.Figure(fig)
                fig.update_yaxes(autorange="reversed")
                return fig
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
                                     mode='markers', name=type, customdata=cc.loc[cc['type'] == type, ['hadware_name', 'angle_rounded']]))

        fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
                                 name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))

        fig.update_traces(
            hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
        fig.update_layout(hovermode="y", title="Fiber cable orientation overview", title_x=0.5, legend_title="Type", legend_orientation="h", yaxis_title="Depth",
                          xaxis_title='AngleFromHighSideClockwiseDegrees', autosize=True, margin=dict(l=0, r=0, b=0, t=50), showlegend=False)
        fig.update_yaxes(autorange="reversed")
        # fig.update_xaxes(dtick=20, tickangle=45)
        fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
        fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
        return fig


@ callback(Output("cd_polar", "figure"),
           Input("dropdown_cd", "value"),
           Input("themeToggle", "value"),
           # State("cd_overview", "figure"),
           )
def clamps_overview(clamps_types, themeToggle):
    fig = go.Figure()
    fiber = clamps[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                    'fiber_angle_rounded']].loc[clamps['type'].isin(clamps_types)]

    # add delta
    nogozone_polar = pd.DataFrame([[angle+10, angle-10, depth]
                                   for angle, depth in fiber[['fiber_plot_angle', 'depth']].values])

    # fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
    #                                fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

    # Add traces
    for type in clamps['type'].unique():
        fig.add_trace(go.Scatterpolar(theta=clamps.loc[clamps['type'] == type, 'plot_angle'], r=clamps.loc[clamps['type'] == type, 'depth'],
                                      mode='markers', name=type, customdata=clamps.loc[clamps['type'] == type, ['hadware_name', 'fiber_angle_rounded']]))

    # Add traces
    # fig.add_trace(go.Scatterpolar(r=nogozone_polar['depth'], theta=nogozone_polar['fiber_plot_angle'], mode='lines+markers',
    #                               name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))
    fig.add_trace(go.Scatterpolar(r=fiber['depth'], theta=fiber['fiber_plot_angle'], mode='lines+markers',
                                  name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))
    fig.update_traces(hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
    fig.update_layout(title="Fiber cable orientation polarplot", title_x=0.5,
                      legend_title="Type", legend_orientation="h", autosize=True, margin=dict(t=50, b=40, l=40, r=40))
    fig.update_polars(
        hole=0.05,
        radialaxis=dict(
            range=[max(clamps['depth'])+100, min(clamps['depth'])-100]),
        angularaxis=dict(
            dtick=15,
            rotation=90,  # start position of angular axis
            direction="clockwise",
        ))
    fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
    if themeToggle == False:
        fig.update_polars(bgcolor='rgb(58, 63, 68)')
    # fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
    return fig
