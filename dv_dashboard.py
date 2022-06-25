from time import sleep
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback, clientside_callback
# import dash_daq as daq
import dash_labs as dl
import dash_bootstrap_components as dbc
# from dash_bootstrap_templates import load_figure_template, ThemeSwitchAIO
from dash.dependencies import ClientsideFunction
import dash_mantine_components as dmc
from dash_iconify import DashIconify


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
    "padding": "0rem",
    # "height": "93vh",
    # "minHeight": "20em",
    # "display": "flex",
    # "flexFlow": "column",
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
                                DashIconify(icon="el:globe-alt",
                                            width=15,
                                            inline=True,
                                            style={"marginRight": "0.5rem"}
                                            ),
                                dbc.Switch(value=False, id="unitsToggle",
                                           className="d-inline-block",
                                           persistence=True, persistence_type='local'),
                                DashIconify(icon="cib:gov-uk",
                                            width=15,
                                            inline=True,
                                            # style={"marginRight": "auto"}
                                            ),
                            ],
                        ),
                    ],
                    # justify="end",
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
                [dbc.NavItem(dbc.NavLink(page['module'].split('.')[1], href=page["path"], active="exact"))
                 for page in dash.page_registry.values() if page["module"] not in ["pages.not_found_404", "pages.index"]]
                +
                [
                    html.Hr(),
                    dbc.NavItem(
                        # dmc.MantineProvider(
                        dmc.Select(
                            data=["React", "Angular", "Svelte", "Vue"],
                            searchable=True,
                            allowDeselect=True,
                            nothingFound="No well found",
                            placeholder="Select a framework",
                            style={"width": '15rem'},
                        ),
                        #   theme={"colorScheme": "light"},
                        #   styles={"Select": {
                        #       "input": {"&:focus": {'borderColor': '#e95420 !important'}}}},
                        #   withNormalizeCSS=True,
                        # ),
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
                    dbc.Col(dbc.NavbarBrand(
                        "   Dashboard",
                        href="/",
                        class_name="my-auto fa fa-chart-line",
                        style={"fontSize": "0.9rem"})),
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
    style={"padding": "0.4rem", "zIndex": "10"},
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
                                      "bottom": "0", "zIndex": "9999", "backgroundColor": "rgba(0,0,0,0.97)"}
                    ),
    ]
)
voids = html.Div([html.Div(id='void1'), html.Div(id='void2')],
                 id="voids", style={"display": "none"})


# callbacks

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
    Output("theme_provider", "theme"),
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


# app initialization
app.layout = dmc.MantineProvider(children=dmc.Container([dcc.Location(id="url"), initial_load, sidebar, navbar, content, stores, voids], class_name='dbc', fluid=True),
                                 theme={"colorScheme": "dark"},
                                 styles={"Select": {
                                     "input": {"&:focus": {'borderColor': '#e95420 !important'}}}},
                                 withNormalizeCSS=True,
                                 id='theme_provider',
                                 )
#    fluid=True,
#    className="dbc",
#    # style={"height": "100vh"},
#    id="main")

if __name__ == "__main__":
    app.run_server(port=5000,
                   debug=True,
                   threaded=True,
                   # host='0.0.0.0',
                   use_reloader=True)
