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
        dbc.Row([
                dbc.Col([
                    html.P("Settings", className="offcanvas-title h5"), ],
                    xl=12, lg=12, md=12, sm=12, xs=12,),
                ], className="mt-3",
                ),
        dbc.Row([
            dbc.Col([
                    dcc.Dropdown(
                        clamp_types,
                        clamp_types[1:],
                        multi=True,
                        id="dropdown_cd",
                    ),
                dcc.Graph(id="cd_overview",
                          animate=True,
                          config={'displaylogo': False},
                          style={'height': '85vh'},
                          ),
                    ],
                xl=6, lg=6, md=12, sm=12, xs=12,
                # style={'height': '100vh'},
                    ),
            dbc.Col([
                dcc.Dropdown(
                    id="dropdown",
                    options=[{"label": x, "value": x} for x in days],
                    value=days[0],
                    clearable=False,
                ),
                dcc.Graph(id="bar-chart", animate=True,
                          config={'displaylogo': False}),
            ],
                xl=6, lg=6, md=12, sm=12, xs=12,),
        ],
        ),
    ],
    # style={'height': '100vh'},
)

# callbacks


@ callback(Output("cd_overview", "figure"),
           Input("dropdown_cd", "value"),
           Input("template", "children"),
           )
def clamps_overview(clamps_types, template):

    fiber = clamps[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                    'fiber_angle_rounded']].loc[clamps['type'].isin(clamps_types)]

    load_figure_template(themes[1][1] if template else themes[0][1])

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
    # fig.update_layout(template=template)
    #fig.update_xaxes(range=[-200, 200])
    return fig


@ callback(Output("bar-chart", "figure"),
           Input("dropdown", "value"),
           Input("template", "children"),
           )
def update_bar_chart(day, template):
    mask = df["day"] == day
    fig = px.bar(df[mask], x="sex", y="total_bill",
                 color="smoker", barmode="group")
    # fig.update_layout(template=template)
    return fig
