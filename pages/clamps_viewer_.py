from distutils.command import config
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
import dash_bootstrap_components as dbc
import dash_labs as dl
import plotly.express as px
import dash_daq as daq
from dash import dcc, html, dash_table, Input, Output, State, callback
import dash
dash.register_page(__name__, path="/")

# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.5/dbc.min.css"
# 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/slate/bootstrap.min.css'

df = px.data.tips()
days = df.day.unique()

layout = html.Div(
    [
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": x, "value": x} for x in days],
            value=days[0],
            clearable=False,
            style={"width": "50%"}
        ),
        dcc.Graph(id="bar-chart", config={'displaylogo': False}),
    ]
)


@callback(Output("bar-chart", "figure"), Input("dropdown", "value"))
def update_bar_chart(day):
    mask = df["day"] == day
    fig = px.bar(df[mask], x="sex", y="total_bill",
                 color="smoker", barmode="group")
    return fig
