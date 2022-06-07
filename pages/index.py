from dash import html
import dash

dash.register_page(__name__, path="/", title="DV Dashboard")


layout = html.H1("Custom Home")
