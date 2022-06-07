#from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url, load_figure_template
import dash_bootstrap_components as dbc
# import dash_labs as dl
import plotly.express as px
# import dash_daq as daq
from dash import dcc, html, dash_table, Input, Output, State, callback
import dash
import numpy as np

dash.register_page(__name__, title="DV Dashboard - CasingVision")


np.random.seed(2020)

layout = html.Div(
    [
        dcc.Graph(id="histograms-graph", config={'displaylogo': False}),
        html.P("Mean:"),
        dcc.Slider(
            id="histograms-mean", min=-3, max=3, value=0, marks={-3: "-3", 3: "3"}
        ),
        html.P("Standard Deviation:"),
        dcc.Slider(id="histograms-std", min=1, max=3,
                   value=1, marks={1: "1", 3: "3"}),
    ]
)


# @callback(
#     Output("histograms-graph", "figure"),
#     Input("histograms-mean", "value"),
#     Input("histograms-std", "value"),
#     Input("themeToggle", "value"),
# )
# def display_color(mean, std, themeToggle):
#     data = np.random.normal(mean, std, size=500)
#     fig = px.histogram(data, nbins=30, range_x=[-10, 10])
#     fig.update_layout(showlegend=False)
#     fig.layout.template = themes['_light']['fig'] if themeToggle else themes['_dark']['fig']
#     fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
#     return fig
