import dash
from dash import dash_table
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
df["id"] = df.index

app.layout = html.Div(
    dash_table.DataTable(
        id="table",
        row_selectable="multi",
        columns=[{"name": i, "id": i} for i in df.columns if i != "id"],
        data=df.to_dict("records"),
        page_size=4,
        filter_action="native",
    )
)

# print(df.to_dict("records"),)
print([
    {"if": {"filter_query": "{{id}} ={}".format(
        i)}, "backgroundColor": "yellow", }
    for i in df.index
])


@app.callback(
    Output("table", "style_data_conditional"),
    Input("table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
        print([
            {"if": {"filter_query": "{{id}} ={}".format(
                i)}, "backgroundColor": "yellow", }
            for i in selRows
        ])
    return [
        {"if": {"filter_query": "{{id}} ={}".format(
            i)}, "backgroundColor": "yellow", }
        for i in selRows
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
