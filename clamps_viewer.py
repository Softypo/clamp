from ctypes import alignment
from pickle import TRUE
import re
from turtle import width
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash_daq as daq
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.5/dbc.min.css"
# 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/slate/bootstrap.min.css'

# initial config
app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/united_d/bootstrap.min.css', dbc.icons.FONT_AWESOME],
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=2, minimum-scale=1"}], title='DV Dashboard')

app.scripts.config.serve_locally = True

# images
DV_LOGO = 'assets/dv_logo.png'

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",

}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# body

sidebar = html.Div(
    [
        dbc.Offcanvas(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.P("Settings", className="offcanvas-title h5"),
                        ),
                        dbc.Col(
                            html.Button(
                                className="btn-close",
                                id="cls_sidebar",
                            ),
                            width=2,
                        ),
                    ],
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.P("Themes",  # className="lead",
                                   style={"textAlign": "right", "marginTop": "auto", "marginBottom": "auto"}),
                            width=8,
                        ),
                        dbc.Col(
                            [
                                html.Span(className="fa fa-moon",
                                          style={"marginRight": "0.5rem"}),
                                dbc.Switch(value=False, id="theme",
                                           className="d-inline-block ml-2",),
                                html.Span(className="fa fa-sun",
                                          style={"marginRight": "auto"}),
                            ],
                        ),
                        # dbc.Col(
                        #     ThemeChangerAIO(
                        #         aio_id="theme", radio_props={"value": dbc.themes.FLATLY}
                        #     ),
                        # ),
                    ],
                ),
                html.P(
                    "A simple sidebar layout with navigation links", className="lead"
                ),
                dbc.Nav(
                    [
                        dbc.NavLink("Home", href="/", active="exact"),
                        dbc.NavLink("Page 1", href="/page-1", active="exact"),
                        dbc.NavLink("Page 2", href="/page-2", active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            id="offcanvas",
            is_open=False,
            placement="end",
            scrollable=True,
            backdrop='static',
            close_button=False,

        ),
    ],
    id="sidebar",
    # style=SIDEBAR_STYLE,
)

navbar_menu = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.NavItem(dbc.NavLink("login", href="#"))
        ),
        dbc.Col(
            dbc.Checklist(
                options=[
                    {"label": "Settings", "value": 1},
                ],
                value=[1],
                id="sidebar-toggler",
                switch=True,
                style={"color": "grey"},
            ),
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=DV_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Dashboard", class_name="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                navbar_menu,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="black",
    dark=True,
)

content = html.Div(id="page-content",  # style=CONTENT_STYLE
                   )

blank = html.Div(id="blank_output")


# callbacks

@ app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
# add callback for toggling the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@ app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@ app.callback([Output("sidebar-toggler", "value"),
                Output("offcanvas", "is_open"),
                Output("cls_sidebar", "n_clicks")],
               [Input("sidebar-toggler", "value"),
                Input("cls_sidebar", "n_clicks")],
               [State("offcanvas", "is_open")],
               )
def close_sidebar(value, n0, is_open):
    if n0:
        return [1], False, 0
    elif not value:
        return value, True, n0
    elif value:
        return value, False, n0
    else:
        return value, is_open, n0


app.clientside_callback(
    """
    function(themeToggle) {
        //  To use different themes,  change these links:
        const theme1 = "https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/united/bootstrap.min.css"
        const theme2 = "https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/united_d/bootstrap.min.css"
        const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]')
        var themeLink = themeToggle ? theme1 : theme2;
        stylesheet.href = themeLink
    }
    """,
    Output("blank_output", "children"),
    Input("theme", "value"),
)


app.layout = dbc.Container(html.Div(
    [dcc.Location(id="url"), navbar, sidebar, content, blank]), fluid=True, className="dbc")

if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
