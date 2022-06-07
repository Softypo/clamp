from time import sleep
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback, clientside_callback
# import dash_daq as daq
import dash_labs as dl
import dash_bootstrap_components as dbc
# from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO
from dash.dependencies import ClientsideFunction


# import plotly.io as pio

# To use different themes,  change these links:
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.5/dbc.min.css"
themes = {'_dark': {'css': 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/_dark/bootstrap.css',
                    'fig': 'slate', 'json': 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/_dark/slate.json'},
          '_light': {'css': 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/_light/bootstrap.min.css',
                     'fig': 'united', 'json': 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/_light/united.json'}
          }

# initial config
app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[themes['_dark']['css'], dbc.icons.FONT_AWESOME],
                suppress_callback_exceptions=False,
                title='DV Dashboard',
                serve_locally=True,
                meta_tags=[
                    {"name": "color-scheme", "content": "light dark"},
                    {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=2, minimum-scale=1"}],
                # external_scripts=['https://cdn.plot.ly/plotly-2.11.1.min.js']
                )
application = app.server  # <<<<<<<<for debuging in vscode only


# load_figure_template(themes['_light']['fig'])
# load_figure_template(themes['_dark']['fig'])
# load_figure_template([themes['_dark']['fig'], themes['_light']['fig']])

# app.scripts.config.serve_locally = True

# images
DV_LOGO = 'assets/dv_logo.png'

# styles
# SIDEBAR_STYLE = {
#     # "position": "fixed",
#     # "top": 0,
#     # "left": 0,
#     # "bottom": 0,
#     # "width": "16rem",
#     # "padding": "2rem 1rem",

# }

# NAVBAR_STYLE = {
#     "padding": "0.4rem",
#     #"height": "4vh",
# }

CONTENT_STYLE = {
    "marginTop": '8px',
    # "padding": "0.5rem",
    "height": "93vh",
    "minHeight": "20em",
    "display": "flex",
    "flexFlow": "column",
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
                            html.P("Theme",
                                   style={"textAlign": "right", "marginTop": "auto", "marginBottom": "auto"}),
                            width=8,
                        ),
                        dbc.Col(
                            [
                                html.Span(className="fa fa-moon",
                                          style={"marginRight": "0.5rem"}),
                                dbc.Switch(value=False, id="themeToggle",
                                           className="d-inline-block ml-2",
                                           persistence=True, persistence_type='local'),
                                html.Span(className="fa fa-sun",
                                          style={"marginRight": "auto"}),
                            ],
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.P("Unit System",
                                   style={"textAlign": "right", "marginTop": "auto", "marginBottom": "auto"}),
                            width=8,
                        ),
                        dbc.Col(
                            [
                                html.Span(className="fa fa-globe",
                                          style={"marginRight": "0.5rem"}),
                                dbc.Switch(value=False, id="unitsToggle",
                                           className="d-inline-block ml-2",
                                           persistence=True, persistence_type='local'),
                                html.Span(className="fa fa-flag-usa",
                                          style={"marginRight": "auto"}),
                            ],
                        ),
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
        dbc.Col(
            dbc.Nav(
                [html.Hr()]
                +
                [dbc.NavItem(dbc.NavLink(page["name"], href=page["path"], active="exact"))
                 for page in dash.page_registry.values() if page["module"] != "pages.not_found_404"]
                +
                [
                    html.Hr(),
                    dbc.NavItem(
                        dcc.Dropdown(
                            ['well1', 'well2', 'well3'],
                            multi=False,
                            clearable=False,
                            searchable=True,
                            placeholder='Select well...',
                            persistence=True,
                            persistence_type='memory',
                            id="well",
                            optionHeight=25,
                            style={"width": "15rem"},
                        ),
                        style={'marginTop': "auto", 'marginBottom': 'auto',
                               'marginLeft': '0.5rem'
                               },
                    ),
                    html.Hr(),
                    dbc.NavItem(
                        dbc.Checklist(
                            options=[
                                {"label": "Settings",
                                 "value": 1},
                            ],
                            value=[1],
                            id="sidebar_toggler",
                            switch=True,
                            style={"color": "grey", "marginLeft": "0.5rem", },
                        ),
                        style={'marginTop': "auto", 'marginBottom': 'auto'}
                    )],
                # pills=False,
                # card=True,
                # justified=False,
                # fill=True,
                # horizontal='end',
                # navbar=True,
            ),
        ),
    ],
    className="g-0 mx-auto flex-nowrap my-auto mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.A([html.Img(src=DV_LOGO, height="30rem")],
                            href="https://darkvisiontech.com/", style={"textDecoration": "none"},),),
                    # dbc.Col(html.Span(className="fa fa-chart-line")),
                    dbc.Col(dbc.NavbarBrand(
                        "  Dashboard", class_name="my-auto fa fa-chart-line", style={"fontSize": "0.9rem"})),
                ],
                align="center",
                className="g-0",
            ),
            dbc.NavbarToggler(id="navbar_toggler", n_clicks=0),
            dbc.Collapse(
                navbar_menu,
                id="navbar_collapse",
                is_open=False,
                navbar=True,
            ),
        ],
    ),
    color="black",
    dark=True,
    style={"padding": "0.4rem"},
    class_name="rounded-3",
    expand="lg",
    # fixed="top",
    sticky="top",
)

content = dl.plugins.page_container

stores = html.Div([dcc.Store(id="dw", storage_type="session"),
                   dcc.Store(id="themes", storage_type="local", data=themes)],
                  id="stores")

initial_load = html.Div(
    [
        dbc.Spinner(color="#e95420", fullscreen=True, id="spinner",
                    fullscreen_style={"position": "fixed", "top": "0", "left": "0", "right": "0",
                                      "bottom": "0", "z-index": "9999", "background-color": "rgba(0,0,0,0.97)"}
                    ),
    ]
)
voids = html.Div([html.Div(id='void1'), html.Div(id='void2')],
                 id="voids", style={"display": "none"})


# callbacks

# @ app.callback(
#     Output("navbar_collapse", "is_open"),
#     Input("navbar_toggler", "n_clicks"),
#     State("navbar_collapse", "is_open"),
# )
# # add callback for toggling the collapse on small screens
# def toggle_navbar_collapse(n_clicks, is_open):
#     if n_clicks:
#         return not is_open
#     return is_open


# @ app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname == "/":
#         return html.P("This is the content of the home page!")
#     elif pathname == "/page-1":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/page-2":
#         return html.P("Oh cool, this is page 2!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )


# @ app.callback(Output("sidebar_toggler", "value"),
#                Output("offcanvas", "is_open"),
#                Output("cls_sidebar", "n_clicks"),
#                Input("sidebar_toggler", "value"),
#                Input("cls_sidebar", "n_clicks"),
#                State("offcanvas", "is_open"),
#                )
# def close_sidebar(value, n0, is_open):
#     if n0:
#         return [1], False, 0
#     elif not value:
#         return value, True, n0
#     elif value:
#         return value, False, n0
#     else:
#         return value, is_open, n0

app.clientside_callback(
    ClientsideFunction(
        namespace="dv_dashboard",
        function_name="toggle_navbar_collapse",
    ),
    Output("navbar_collapse", "is_open"),
    Input("navbar_toggler", "n_clicks"),
    State("navbar_collapse", "is_open"),
)

app.clientside_callback(
    ClientsideFunction(
        namespace="dv_dashboard",
        function_name="close_sidebar",
    ),
    Output("sidebar_toggler", "value"),
    Output("offcanvas", "is_open"),
    Output("cls_sidebar", "n_clicks"),
    Input("sidebar_toggler", "value"),
    Input("cls_sidebar", "n_clicks"),
    State("offcanvas", "is_open"),
)

app.clientside_callback(
    ClientsideFunction(
        namespace="dv_dashboard",
        function_name="theme_switcher",
    ),
    Output("void1", "children"),
    Input("themeToggle", "value"),
    State("themes", "data"),
)


@ app.callback(
    Output("spinner", "fullscreen_style"),
    Input("void1", "children"),
)
def load_output(_):
    sleep(1)
    return {'display': 'none'}


# app.clientside_callback(
#     ClientsideFunction(
#         namespace="dv_dashboard",
#         function_name="first_load_delay",
#     ),
#     Output("void2", "children"),
#     Input("themeToggle", "value"),
#     State("themes", "data"),
# )

# @app.callback(Output("loading", "style"), Input("void2", "children"))
# def void2(_):
#     sleep(3)
#     return {"display": "none"}

# app initialization
app.layout = dbc.Container([dcc.Location(id="url"), navbar, sidebar, content, stores, initial_load, voids],
                           fluid=True, className="dbc", style={"height": "100vh"}, id="main")

if __name__ == "__main__":
    app.run_server(port=5000,
                   debug=True,
                   threaded=True,
                   # host='0.0.0.0',
                   use_reloader=True)
