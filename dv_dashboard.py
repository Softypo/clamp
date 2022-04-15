import dash
from dash import dcc, html, dash_table, Input, Output, State, callback, clientside_callback
import dash_daq as daq
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO, ThemeChangerAIO, template_from_url, load_figure_template

# To use different themes,  change these links:
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.5/dbc.min.css"
themes = {'_dark': {'css': 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/_dark/bootstrap.css', 'fig': 'slate'},
          '_light': {'css': 'https://cdn.jsdelivr.net/gh/Softypo/clamp/themes/_light/bootstrap.min.css', 'fig': 'flatly'}}

# initial config
app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[themes['_dark']['css'], dbc.icons.FONT_AWESOME],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=2, minimum-scale=1"}], title='DV Dashboard', serve_locally=True)
load_figure_template(themes['_light']['fig'])
load_figure_template(themes['_dark']['fig'])

#app.scripts.config.serve_locally = True

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
    # "height": "100vh",
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
                                dbc.Switch(value=False, id="themeToggle",
                                           className="d-inline-block ml-2",
                                           persistence=True, persistence_type='local'),
                                html.Span(className="fa fa-sun",
                                          style={"marginRight": "auto"}),
                            ],
                        ),
                        # dbc.Col(
                        #     ThemeChangerAIO(
                        #         aio_id="themeio", radio_props={"value": dbc.themes.SLATE}
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
        dbc.Col(
            dbc.Nav(
                [dbc.NavItem(dbc.NavLink(page["name"], href=page["path"], active="exact"))
                 for page in dash.page_registry.values() if page["module"] != "pages.not_found_404"],
                pills=True,
                justified=True,
            ),
            width=5,
        ),
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.Checklist(
                options=[
                    {"label": "Settings", "value": 1},
                ],
                value=[1],
                id="sidebar-toggler",
                switch=True,
                style={"color": "grey", "marginLeft": "1rem"},
            ),
            width="auto",
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
                href="https://darkvisiontech.com/",
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

content = dl.plugins.page_container

sessions = html.Div([dcc.Store(id="themes", storage_type="local", data=themes)],
                    id="sessions")

voids = html.Div([html.Div(id='void1'), html.Div(id='void2')],
                 id="voids", style={"display": "none"})


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
    function(themeToggle, themes) {
        const stylesheet = document.querySelector('link[rel=stylesheet][href^="https://cdn.jsdelivr"]')
        var themeLink = themeToggle ? themes['_light']['css'] : themes['_dark']['css'];
        stylesheet.href = themeLink
    }
    """,
    Output("void1", "children"),
    Input("themeToggle", "value"),
    State("themes", "data"),
)


@ app.callback(Output("void2", "children"),
               Input("themeToggle", "value"),
               )
def fig_theme_session(data):
    load_figure_template(themes['_light']['fig']
                         if data else themes['_dark']['fig'])


# app initialization
app.layout = dbc.Container(
    [dcc.Location(id="url"), navbar, sidebar, content, sessions, voids], fluid=True, className="dbc", style=CONTENT_STYLE)

if __name__ == "__main__":
    app.run_server(port=8888,
                   debug=True,
                   threaded=True,
                   # host='0.0.0.0',
                   use_reloader=True)
