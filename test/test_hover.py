from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import pandas as pd

# Small molcule drugbank dataset
# Source: https://raw.githubusercontent.com/plotly/dash-sample-apps/main/apps/dash-drug-discovery/data/small_molecule_drugbank.csv'
data_path = 'https://raw.githubusercontent.com/plotly/dash-sample-apps/main/apps/dash-drug-discovery/data/small_molecule_drugbank.csv'

df = pd.read_csv(data_path, header=0, index_col=0)

cc = pd.read_csv('data\Seidel Unit A3_features_QF.csv', usecols=[0, 1, 7])
cc.rename(columns={'perfAngleFromHighSideClockwiseDegrees':
          'AngleFromHighSideClockwiseDegrees'}, inplace=True)
cc['type'] = ['CrossCouple' if 'CC' in name else 'BlastProtector' if 'BP' in name else 'Centralizer' for name in cc['name']]
cc['NV'] = ['NV' if 'NV' in name else pd.NA for name in cc['name']]
cc.loc[cc['NV'] == 'NV', 'AngleFromHighSideClockwiseDegrees'] = pd.NA
cc['J'] = [name.split()[0] if 'J' in name.split()[0]
           else pd.NA for name in cc['name']]
cc['BP'] = [name.split()[1][:3] if 'BP' in name.split()[1]
            else pd.NA for name in cc['name']]
cc['CC'] = [name.split()[1][:-2] if 'CC' in name.split()[1]
            else pd.NA for name in cc['name']]
cc['C'] = [name.split()[1] if name.split()[1].startswith('C1')
           else pd.NA for name in cc['name']]


perfs = pd.read_csv('data\Seidel Unit A3_Perfs_BIASED.csv', usecols=[0, 1, 7])
perfs['type'] = 'PERFS'
perfs.rename(columns={
             'perfAngleFromHighSideClockwiseDegrees': 'AngleFromHighSideClockwiseDegrees'}, inplace=True)

features = pd.concat([cc[['depth', 'J', 'BP', 'AngleFromHighSideClockwiseDegrees']].groupby(['J', 'BP']).mean(
    numeric_only=False), cc[['depth', 'CC', 'AngleFromHighSideClockwiseDegrees']].groupby(['CC']).mean(numeric_only=False)])
features['name'] = features.index
features = features.sort_values(by=['depth'], ascending=False)
features.reset_index(drop=True, inplace=True)
features['type'] = ['BlastProtector' if 'BP' in name[1]
                    else 'CrossCoupling' if 'CC' in name else 'Centralizer' for name in features['name']]
features.loc[features['AngleFromHighSideClockwiseDegrees'].isna(
), 'type'] = features.loc[features['AngleFromHighSideClockwiseDegrees'].isna(), 'type']+' NV'
features.interpolate(method='pad', inplace=True)

features['fiberAngleFromHighSideClockwiseDegrees'] = [angle+180 if angle <
                                                      180 else angle-180 for angle in features['AngleFromHighSideClockwiseDegrees']]
features['fiber_plot_angle'] = [angle-360 if angle >
                                180 else angle for angle in features['fiberAngleFromHighSideClockwiseDegrees']]


combined = pd.concat([features, perfs])
combined['plot_angle'] = [angle-360 if angle >
                          180 else angle for angle in combined['AngleFromHighSideClockwiseDegrees']]
combined['angle_rounded'] = combined['AngleFromHighSideClockwiseDegrees'].round(
    0)
combined['fiber_angle_rounded'] = combined['fiberAngleFromHighSideClockwiseDegrees'].round(
    0)

fig = go.Figure()

# Add windows
gozone_svg = ''.join([f'M {xy[0][0]+30},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+30},{xy[0][1]} ' for xy in zip(combined.loc[combined['type'] != 'PERFS', ['plot_angle', 'depth']].values, range(combined.loc[combined['type'] != 'PERFS', ['plot_angle', 'depth']].shape[0]))]) + \
    ''.join([f' L{xy[0][0]-30},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-30},{xy[0][1]}' for xy in zip(combined.loc[combined['type'] !=
            'PERFS', ['plot_angle', 'depth']].values, range(combined.loc[combined['type'] != 'PERFS', ['plot_angle', 'depth']].shape[0]))][::-1])

nogozone_svg = ''.join([f'M {xy[0][0]+10},{xy[0][1]} ' if xy[1] == 0 else f'L{xy[0][0]+10},{xy[0][1]} ' for xy in zip(combined.loc[combined['type'] != 'PERFS', ['fiber_plot_angle', 'depth']].values, range(combined.loc[combined['type'] != 'PERFS', ['fiber_plot_angle', 'depth']].shape[0]))]) + \
    ''.join([f' L{xy[0][0]-10},{xy[0][1]} Z' if xy[1] == 0 else f' L{xy[0][0]-10},{xy[0][1]}' for xy in zip(combined.loc[combined['type'] != 'PERFS',
            ['fiber_plot_angle', 'depth']].values, range(combined.loc[combined['type'] != 'PERFS', ['fiber_plot_angle', 'depth']].shape[0]))][::-1])

fig.update_layout(shapes=[dict(type="path", path=gozone_svg, fillcolor='rgba(154,205,50,0.2)', line=dict(
    width=0), layer='below'), dict(type="path", path=nogozone_svg, fillcolor='rgba(255,69,0,0.2)', line=dict(width=0), layer='below')])

# Add traces
fig.add_trace(go.Scatter(x=combined.loc[combined['type'] == 'BlastProtector', 'plot_angle'], y=combined.loc[combined['type'] == 'BlastProtector', 'depth'],
              mode='markers', name='BlastProtector', marker_color='forestgreen', customdata=combined.loc[combined['type'] == 'BlastProtector', ['name', 'angle_rounded']]))

fig.add_trace(go.Scatter(x=combined.loc[combined['type'] == 'BlastProtector NV', 'plot_angle'], y=combined.loc[combined['type'] == 'BlastProtector NV', 'depth'],
              mode='markers', name='BlastProtector LowConf', marker_color='forestgreen', customdata=combined.loc[combined['type'] == 'BlastProtector NV', ['name', 'angle_rounded']]))

fig.add_trace(go.Scatter(x=combined.loc[combined['type'] == 'CrossCoupling', 'plot_angle'], y=combined.loc[combined['type'] == 'CrossCoupling', 'depth'],
              mode='markers', name='CrossCoupling', marker_color='darkolivegreen', customdata=combined.loc[combined['type'] == 'CrossCoupling', ['name', 'angle_rounded']]))

fig.add_trace(go.Scatter(x=combined.loc[combined['type'] == 'CrossCoupling NV', 'plot_angle'], y=combined.loc[combined['type'] == 'CrossCoupling NV', 'depth'],
              mode='markers', name='CrossCoupling LowConf', marker_color='darkolivegreen', customdata=combined.loc[combined['type'] == 'CrossCoupling NV', ['name', 'angle_rounded']]))

fig.add_trace(go.Scatter(x=combined.loc[combined['type'] == 'PERFS', 'plot_angle'], y=combined.loc[combined['type'] == 'PERFS', 'depth'],
              mode='markers', name='PERFS', marker_color='navy', customdata=combined.loc[combined['type'] == 'PERFS', ['name', 'angle_rounded']]))

fig.add_trace(go.Scatter(x=combined.loc[combined['type'] != 'PERFS', 'fiber_plot_angle'], y=combined.loc[combined['type'] != 'PERFS', 'depth'],
              mode='lines+markers', name='Fiber Wire', marker_color='crimson', customdata=combined.loc[combined['type'] != 'PERFS', ['name', 'fiber_angle_rounded']]))

fig.update_traces(hovertemplate='%{customdata[0]}<br>%{customdata[1]}')
fig.update_xaxes(range=[-185, 185])
fig.update_yaxes(autorange="reversed")
fig.update_layout(hovermode='y', title="Jewelry vs Perfs", legend_title="Type", legend_orientation="h",
                  template="plotly", yaxis_title="Depth", xaxis_title='AngleFromHighSideClockwiseDegrees')

# fig = go.Figure(data=[
#     go.Scatter(
#         x=df["LOGP"],
#         y=df["PKA"],
#         mode="markers",
#         marker=dict(
#             colorscale='viridis',
#             color=df["MW"],
#             size=df["MW"],
#             colorbar={"title": "Molecular<br>Weight"},
#             line={"color": "#444"},
#             reversescale=True,
#             sizeref=45,
#             sizemode="diameter",
#             opacity=0.8,
#         )
#     )
# ])

# # turn off native plotly.js hover effects - make sure to use
# # hoverinfo="none" rather than "skip" which also halts events.
fig.update_traces(hoverinfo="none", hovertemplate=None)

fig.update_layout(
    xaxis=dict(title='Log P'),
    yaxis=dict(title='pkA'),
    plot_bgcolor='rgba(255,255,255,0.1)'
)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph-basic-2", figure=fig, clear_on_unhover=True),
    dcc.Tooltip(id="graph-tooltip"),
])


@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("graph-basic-2", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = combined.iloc[num]
    img_src = "C:\\Users\\Softypo\\OneDrive\\Documentos\\_Burrito\\clamp\\data\\images\\J40 CC39 cross coupling.jpg"
    name = df_row['name']
    #form = df_row['type']
    #desc = df_row['DESC']
    # if len(desc) > 300:
    #    desc = desc[:100] + '...'

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{str(name)}", style={"color": "darkblue"}),
            # html.P(f"{form}"),
            # html.P(f"{desc}"),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]

    return True, bbox, children


if __name__ == "__main__":
    app.run_server(debug=True)
