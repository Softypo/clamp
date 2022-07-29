import dash
import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.graph_objects as go
from .utils.pil_utilities import loader_pil_multiprocess, loader_pil
from dash import dcc, html, dash_table, Input, Output, State, callback, clientside_callback
from dash.dependencies import ClientsideFunction
#from dash_iconify import DashIconify

dash.register_page(__name__, title="DV Dashboard - ClampsVision")

COLUMN_STYLE = {
    "paddingTop": '8px',
    # "padding": "0.5rem",
    "height": "fill",
    "minHeight": "60vh",
    "maxHeight": "calc(100vh - 3rem)",
    # "display": "flex",
    # "flexFlow": "column",
}

# data

# clamps = pd.read_hdf("data/446/446cd.h5", "cd446")
clamps = pd.read_pickle("data/452/452cd.pkl")
clamp_types = clamps['type'].unique()
clamp_types = clamp_types[clamp_types != 'PERFS']
clamp_imgs = loader_pil('data/446/tubeviews/all')


# functions

def clampsoverview_fig(clamp_types, clamps, fiver=True):
    fig = go.Figure()
    cc = clamps.copy()
    fiber = cc[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                'fiberTOH']].loc[cc['type'].isin(clamp_types)]

    # add delta
    nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))]) + \
        ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(
            fiber[['fiber_plot_angle', 'depth']].values, range(fiber[['fiber_plot_angle', 'depth']].shape[0]))][::-1])

    fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
                      fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

    # Add traces
    for type in cc['type'].unique():
        fig.add_trace(go.Scatter(x=cc.loc[cc['type'] == type, 'plot_angle'], y=cc.loc[cc['type'] == type, 'depth'],
                                 mode='markers', name=type, customdata=cc.loc[cc['type'] == type, ['hadware_name', 'clampsTOH']].round(0)))
    if fiver:
        fig.add_trace(go.Scatter(x=fiber['fiber_plot_angle'], y=fiber['depth'], mode='lines+markers',
                                 name='Fiber Wire', marker_color='crimson', customdata=fiber[['type', 'fiberTOH']].round(0)))

    fig.update_traces(
        hovertemplate='%{customdata[0]}<br>%{customdata[1]} deg (TOH)')
    fig.update_layout(hovermode="y unified", legend_title="Type", legend_orientation="h", yaxis_title="Depth (m)",
                      showlegend=False,
                      xaxis_title='AngleFromHighSideClockwiseDegrees', autosize=True, margin=dict(l=0, r=10, b=0, t=0, pad=4),
                      # title="Fiber cable orientation overview",
                      # title_x=0.5,
                      )
    fig.update_yaxes(autorange="reversed", ticksuffix=" m")
    fig.layout.modebar = {'orientation': 'v'}
    return fig


def clampview_fig(clamp_img, fiver=True):

    # Create figure
    fig = go.Figure()

    # Constants
    img_width = clamp_img.size[0]
    img_height = clamp_img.size[1]
    scale_factor = 1

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        # autorange=False,
        # range=[0, img_width * scale_factor],
        scaleanchor="y"
    )

    fig.update_yaxes(
        visible=False,
        # autorange=False,
        # range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        # scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="contain",
            source=clamp_img)
    )

    # Configure other layout
    fig.update_layout(
        # autosize=False,
        dragmode='pan',
        hovermode=False,
        # width=img_width * scale_factor,
        # height=img_height * scale_factor,
        margin=dict(l=0, r=0, b=0, t=0),
    )
    # fig.layout.transition = {'duration': 500, 'easing': 'cubic-in-out'}
    return fig


def clampspolar_fig(clamp_types, clamps, fiver=True):
    fig = go.Figure()
    fiber = clamps[['type', 'fiber_plot_angle', 'depth', 'hadware_name',
                    'fiberTOH']].loc[clamps['type'].isin(clamp_types)]

    # add delta
    # nogozone_polar = pd.DataFrame([[angle+10, angle-10, depth]
    #                                for angle, depth in fiber[['fiber_plot_angle', 'depth']].values])

    # fig.update_layout(shapes=[dict(type="path", path=nogozone_svg,
    #                                fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

    # Add traces
    for type in clamps['type'].unique():
        fig.add_trace(go.Scatterpolar(theta=clamps.loc[clamps['type'] == type, 'plot_angle'], r=clamps.loc[clamps['type'] == type, 'depth'],
                                      mode='markers', name=type, customdata=clamps.loc[clamps['type'] == type, ['type', 'depth', 'clampsTOH']].round(0)))

    # Add traces
    # fig.add_trace(go.Scatterpolar(r=nogozone_polar['depth'], theta=nogozone_polar['fiber_plot_angle'], mode='lines+markers',
    #                               name='Fiber Wire', marker_color='crimson', customdata=fiber[['hadware_name', 'fiber_angle_rounded']]))
    if fiver:
        fig.add_trace(go.Scatterpolar(r=fiber['depth'], theta=fiber['fiber_plot_angle'], mode='lines+markers',
                      name='Fiber Wire', marker_color='crimson', customdata=fiber[['type', 'depth', 'fiberTOH']].round(0)))

    fig.update_traces(
        hovertemplate='%{customdata[1]} m<br>%{customdata[2]} deg (TOH)')
    fig.update_layout(title="Fiber cable orientation polarplot",
                      dragmode='turntable',
                      title_x=0.5,
                      legend_title="Type",
                      legend_orientation="h",
                      autosize=True,
                      margin=dict(t=40, b=40, l=40, r=40))
    fig.update_polars(
        hole=0.05,
        radialaxis=dict(
            range=[max(clamps['depth'])+100, min(clamps['depth'])-100]),
        angularaxis=dict(
            dtick=15,
            rotation=90,  # start position of angular axis
            direction="clockwise",
        ))
    # fig.layout.transition = {'duration': 1000, 'easing': 'circle-in-out'}
    return fig


# body

layout = [
    dcc.Store(id="ctbl", storage_type="memory",
              data=clamps.iloc[:, [0, 1, 4, 5, 6, 9]].to_dict('records')),
    dcc.Store(id="cover", storage_type="memory",
              data=clampsoverview_fig(clamp_types, clamps)),
    dcc.Store(id="cview", storage_type="memory"),
    dcc.Store(id="cpolar", storage_type="memory",
              data=clampspolar_fig(clamp_types, clamps)),
    dbc.Row([
            dbc.Col([
                dbc.Card([
                    dmc.Select(
                        data=["DVT1", "DVT2", "DVT3", "DVT4"],
                        searchable=True,
                        allowDeselect=True,
                        nothingFound="No logging found",
                        placeholder="Select a logging run",
                        style={"width": '100%'},
                    ),
                    dbc.CardHeader(
                        dbc.Tabs(
                            [
                                dbc.Tab(label="Overview",
                                        tab_id="overview",
                                        activeTabClassName="fst-italic",
                                        key="overview"),
                                dbc.Tab(label="Tubeview",
                                        tab_id="tubeview",
                                        activeTabClassName="fst-italic",
                                        key="tubeview"),
                                dbc.Tab(label="Resume",
                                        tab_id="resume",
                                        activeTabClassName="fst-italic",
                                        key="resume"),
                            ],
                            id="card-tabs",
                            active_tab="overview",
                            persistence=True,
                            persistence_type="memory",
                        )
                    ),
                    dbc.CardBody(
                        children=[
                            dcc.Loading(id="cd_loading", type="default", children=[
                                dbc.Fade(id="cd_overview_fade", is_in=True, exit=True, timeout=100, children=[
                                    dbc.Card([
                                        dbc.Row([
                                            dbc.Col([
                                                html.P("Interval: ",
                                                       className="d-inline",
                                                       ),
                                                html.P("00000.000 - 00000.000",
                                                       className="d-inline-block",
                                                       id="cd_interval",
                                                       ),
                                            ],
                                                xxl=6, xl=6, lg=6, md=6, sm=12, xs=12),
                                            dbc.Col([
                                                html.P("Mean: ",
                                                       className="d-inline",
                                                       ),
                                                html.P("000.000",
                                                    className="d-inline-block",
                                                    id="cd_mean",
                                                       ),
                                            ],
                                                xxl=3, xl=3, lg=3, md=3, sm=6, xs=6),
                                            dbc.Col([
                                                html.P("StDev: ",
                                                       className="d-inline",
                                                       ),
                                                html.P("000.000",
                                                    className="d-inline-block",
                                                    id="cd_stdev",
                                                       ),
                                            ],
                                                xxl=3, xl=3, lg=3, md=3, sm=6, xs=6),
                                        ],
                                            className="text-center",
                                            style={"font-size": "0.9rem",
                                                   "margin-top": "0.5rem"},
                                        ),
                                        dcc.Graph(id="cd_overview",
                                                  animate=False,
                                                  responsive=True,
                                                  config={'displaylogo': False,
                                                          'modeBarButtonsToRemove': ['zoom', 'pan2d', 'boxZoom', 'lasso2d', 'select2d', 'resetScale2d'],
                                                          'toImageButtonOptions': {'format': 'png', 'filename': 'Overview', 'height': 1080, 'width': 600, 'scale': 3}},
                                                  style={
                                                      'height': '100%'}
                                                  )], style={'height': '100%'}),
                                ], style={'height': '100%', 'display': 'block'}),
                                dbc.Fade(id="cd_view_fade", is_in=False, exit=True, timeout=100, children=[
                                    dcc.Graph(id="cd_view",
                                              animate=False,
                                              responsive=True,
                                              config={'displaylogo': False,
                                                      'scrollZoom': True,
                                                      'responsive': True,
                                                      'modeBarButtonsToRemove': ['zoom', 'boxZoom', 'lasso2d', 'select2d', 'resetScale2d'],
                                                      'toImageButtonOptions': {'format': 'png', 'filename': 'Overview', 'height': 1080, 'width': 600, 'scale': 3}},
                                              style={
                                                  'height': '100%'}
                                              )], style={'height': '100%', 'display': 'none'}),
                                dbc.Fade(id="cd_resume_fade", is_in=False, exit=True, timeout=100, children=[
                                    html.P("Phillips's Unit B3 was scanned by Darkvision Technologies on April 6, 2022, for clamp detection analysis. Darkvision's findings can be summarized as follows:\nAll 27 Cable Detection Clamps were identified, and its orientation measured. All analyses provided in this report or affiliated with this survey are provided on a commercially reasonable efforts basis. It remains the sole responsibility of the operator utilizing the report and information contained to undertake actions to ensure well and personnel safety, and draw their own conclusions regarding the well. All analyses provided by DarkVision Technologies Inc. are based on experience and judgment, but are always within the limitations of the technology deployed and downhole operating environment. Since all analysis and interpretations are opinions based on inferences from ultrasound measurements, the accuracy or completeness of any analysis or interpretation is not and cannot be guaranteed.",
                                           style={'textAlign': 'justify',
                                                  'textJustify': 'inter-word'},
                                           ),
                                ], style={'height': '100%', 'display': 'none'}),
                            ], color='#e95420', parent_style={'height': '100%'}),
                        ],
                        id="card-content",
                        className="card-text",
                        style={'height': '100%'}),
                ], style={'height': '100%'}),
            ],
                xxl=7, xl=6, lg=6, md=12, sm=12, xs=12,
                style=COLUMN_STYLE,
                className="pe-lg-0",
            ),
            dbc.Col(
                dbc.Card([
                    dbc.Row(
                        dcc.Graph(id="cd_polar",
                                  animate=False,
                                  responsive=True,
                                  config={'displaylogo': False,
                                          'doubleClick': 'reset',
                                          'responsive': True,
                                          'modeBarButtonsToRemove': ['zoom', 'select2d'],
                                          'toImageButtonOptions': {'format': 'png', 'filename': 'Overview', 'height': 600, 'width': 600, 'scale': 3}},
                                  style={
                                      'height': '25vh', 'minHeight': '20rem'},
                                  ),
                    ),
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                clamp_types,
                                clamp_types[1:],
                                multi=True,
                                searchable=False,
                                persistence=True,
                                persistence_type='memory',
                                id="dropdown_cd",
                                style={"width": "100%", "fontSize": "0.8rem"},
                            ), width=11,),
                        dbc.Col([
                            dcc.Clipboard(
                                id="table_copy",
                                style={
                                    "fontSize": 15,
                                    "position": "relative",
                                    "top": "0.5rem",
                                    "right": "1rem",
                                },
                                title="Copy to clipboard",
                            ),
                            # dbc.Tooltip(
                            #     "Copy table to clipboard",
                            #     delay={'show': 500,
                            #            'hide': 500},
                            #     target="table_copy",
                            # ),
                        ], width=1,
                        ), ], style={'height': 'auto', 'paddingTop': '0.5rem', 'paddingLeft': '0.5rem'}, justify='around'),
                    dbc.Row(
                        dash_table.DataTable(id='cd_table',
                                             cell_selectable=False,
                                             row_selectable='single',
                                             page_action='native',
                                             sort_action='native',
                                             style_as_list_view=True,
                                             fixed_rows={
                                                 'headers': True, 'data': 0},
                                             style_table={
                                                 'minHeight': '10%', 'height': '100%', 'maxHeight': '100%', 'padding': '5px'},
                                             style_header={
                                                 'text-align': 'left', 'fontSize': '0.8em', 'font-style': 'italic'},
                                             style_cell={
                                                 'text-align': 'left', 'fontSize': '1em'},
                                             ),
                        className="flex-grow-1 flex-shrink-1",
                    ),
                ], style={'height': '100%'}),
                xxl=5, xl=6, lg=6, md=12, sm=12, xs=12,
                style=COLUMN_STYLE,
            ),
            ],
            style={'position': 'relative', 'bottom': '5px',
                   'height': 'calc(100vh - 3rem)'},
            ),
]


@ callback(
    Output("cd_view", "figure"),
    Input("cd_table", "derived_virtual_selected_row_ids"),
    Input("themeToggle", "value"),
    State("themes", "data"),
)
def clampsview_listener(fig_id, themeToggle, themes):
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    # Create empty figure
    empty_fig = go.Figure()
    # Configure axes
    empty_fig.update_yaxes(
        visible=False,
        range=[0, 1]
    )
    empty_fig.update_xaxes(
        visible=False,
        range=[0, 1]
    )
    empty_fig.update_layout(
        dragmode='pan',
        hovermode=False,
        # width=img_width * scale_factor,
        # height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )
    if fig_id is None:
        fig = go.Figure(empty_fig)
    elif len(fig_id) < 1:
        fig = go.Figure(empty_fig)
    else:
        try:
            fig = go.Figure(clampview_fig(clamp_imgs[fig_id[0]], fiver=True))
        except:
            fig = go.Figure(empty_fig)
    if themeToggle:
        fig.layout.template = requests.get(
            url=themes['_light']['json']).json()
        fig.layout.modebar = {
            'orientation': 'v',
            'bgcolor': 'salmon',
            'color': 'white',
            'activecolor': '#9ED3CD'}
    else:
        fig.layout.template = requests.get(
            url=themes['_dark']['json']).json()
        fig.update_polars(bgcolor='rgb(58, 63, 68)')
        fig.layout.modebar = {
            'orientation': 'v',
            'bgcolor': 'rgb(39, 43, 48)',
            'color': 'white',
            'activecolor': 'grey'}
    return fig


clientside_callback(
    ClientsideFunction(
        namespace="clamps_viewer",
        function_name="tab_content"
    ),
    Output("cd_overview_fade", "style"),
    Output("cd_overview_fade", "is_in"),
    Output("cd_view_fade", "style"),
    Output("cd_view_fade", "is_in"),
    Output("cd_resume_fade", "style"),
    Output("cd_resume_fade", "is_in"),
    Output("card-tabs", "active_tab"),
    Input("card-tabs", "active_tab"),
    Input("cd_table", "derived_virtual_selected_row_ids"),
)

clientside_callback(
    ClientsideFunction(
        namespace="clamps_viewer",
        function_name="clampstable_rowselect"
    ),
    Output("cd_table", "style_data_conditional"),
    Input("cd_table", "derived_virtual_selected_row_ids"),
)

clientside_callback(
    ClientsideFunction(
        namespace="clamps_viewer",
        function_name="clampstable_listener"
    ),
    Output("cd_table", "data"),
    Output("cd_table", "columns"),
    Output("cd_table", "selected_rows"),
    Input("dropdown_cd", "value"),
    Input("ctbl", "data"),
    State("cd_table", "selected_rows"),
)

clientside_callback(
    ClientsideFunction(
        namespace="clamps_viewer",
        function_name="clampstable_tocsv"
    ),
    Output("table_copy", "content"),
    Input("table_copy", "n_clicks"),
    State("cd_table", "data"),
)


clientside_callback(
    ClientsideFunction(
        namespace="clamps_viewer",
        function_name="clampsoverview_listener"
    ),
    Output("cd_overview", "figure"),
    Input("dropdown_cd", "value"),
    Input('cd_overview', 'relayoutData'),
    Input("cover", "data"),
    State('cd_overview', 'figure'),
)

clientside_callback(
    ClientsideFunction(
        namespace="clamps_viewer",
        function_name="clampspolar_listener"
    ),
    Output("cd_interval", "children"),
    Output("cd_mean", "children"),
    Output("cd_stdev", "children"),
    Output("cd_polar", "figure"),
    Input("dropdown_cd", "value"),
    Input('cd_overview', 'relayoutData'),
    Input("cpolar", "data"),
    State('cd_polar', 'figure'),
    State('unitsToggle', 'value'),
)


clientside_callback(
    ClientsideFunction(
        namespace="clamps_viewer",
        function_name="cstore_switcher",
    ),
    Output("ctbl", "data"),
    Output("cover", "data"),
    Output("cpolar", "data"),
    Input("themeToggle", "value"),
    Input("unitsToggle", "value"),
    State("ctbl", "data"),
    State("cover", "data"),
    State("cpolar", "data"),
    State("themes", "data"),
)
