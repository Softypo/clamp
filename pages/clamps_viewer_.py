from distutils.command.config import config
from re import template
from turtle import st, width
from dv_dashboard import themes
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
df = px.data.tips()
days = df.day.unique()

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
                xl=6, lg=6, md=12, sm=12, xs=12,
                    ),
            dbc.Col([
                dcc.Dropdown(
                    id="dropdown",
                    options=[{"label": x, "value": x} for x in days],
                    value=days[0],
                    clearable=False,
                ),
                dcc.Graph(id="bar-chart", animate=False,
                          config={'displaylogo': False}),
            ],
                xl=6, lg=6, md=12, sm=12, xs=12,),
        ],),
    ],
)


tabs = {'overview': [
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
              config={'displaylogo': False},
              style={'height': '83vh'},
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
              style={'height': '83vh'},
              ),
]
}


# callbacks

@callback(
    Output("card-content", "children"), [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    return tabs[active_tab]


@ callback(Output("cd_overview", "figure"),
           Input("dropdown_cd", "value"),
           Input("session", "data"),
           State("cd_overview", "figure"),
           )
def clamps_overview(clamps_types, theme, fig):

    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'session':
        fig = go.Figure(fig)
        fig.layout.template = themes['_light']['fig'] if theme else themes['_dark']['fig']
        return fig

    else:
        fiber = clamps[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                        'fiber_angle_rounded']].loc[clamps['type'].isin(clamps_types)]

        fig = go.Figure()

        # # Add windows
        nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
            ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
                fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

        fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
                                       fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

        # Add traces
        for type in clamps['type'].unique():
            fig.add_trace(go.Scatter(x=clamps.loc[clamps['type'] == type, 'plot_angle'], y=clamps.loc[clamps['type'] == type, 'depth'],
                                     mode='markers', name=type, customdata=clamps.loc[clamps['type'] == type, ['hadware_name', 'fiber_angle_rounded']]))

        fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
                                 name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))

        fig.update_traces(hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(hovermode="y", title="Fiber cable orientation overview", legend_title="Type", legend_orientation="h", yaxis_title="Depth",
                          xaxis_title='AngleFromHighSideClockwiseDegrees')
        # fig.update_xaxes(range=[-185, 185])
        fig.layout.template = themes['_light']['fig'] if theme else themes['_dark']['fig']
        fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
        return fig
    # else:
    #     return dash.no_update


@ callback(Output("bar-chart", "figure"),
           Input("dropdown", "value"),
           Input("session", "data")
           #Input("template", "children"),
           )
def update_bar_chart(day, theme):
    mask = df["day"] == day
    fig = px.bar(df[mask], x="sex", y="total_bill",
                 color="smoker", barmode="group")
    fig.layout.template = themes['_light']['fig'] if theme else themes['_dark']['fig']
    fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
    return fig
