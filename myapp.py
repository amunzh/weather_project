from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.data as pldata
import pandas as pd
import sqlite3

conn = sqlite3.connect("weather.db")
cursor = conn.cursor()

# Order of each city
cities = {
        "New York": "new_york",
        "Los Angeles": "los_angeles",
        "Houston": "houston",
        "Miami": "miami",
        "Seattle": "seattle",
    }

# Creating a combined dataset to easier access the data
df_all = []
for name, table in cities.items():
    df_ext = pd.read_sql_query(f'SELECT * FROM "{table}"', conn)
    df_ext["city"] = name
    df_all.append(df_ext)
df = pd.concat(df_all, ignore_index=True)
conn.close()



app = Dash(__name__)

climate_weather= [x for x in df.columns if x not in ("city", "month")]
app.layout = html.Div([
    html.H2("INTERACTIVE DASHBOARDS", style = {"text-align": "center","font-weight": "bold"}),
    
    #First graph
    html.Div(children=[  
        html.H3("Heatmap for each Month by City",style = {"text-align": "center","font-weight": "bold"}),
        html.Div(style={"display": "flex","gap": "12px","justify-content": "center"}, children=[ 
        dcc.Dropdown(
                id="climate_dropdown2",
                options=[{"label": symbol.replace("_", " ").title(), "value": symbol} for symbol in climate_weather],
                value="avg_temp_f",
                clearable=False
            )]),
        dcc.Graph(id="heatmap-climat")
    ]),

    #Second graph
    html.Div(children=[  
        html.H3("Precipitation for each city",style = {"text-align": "center","font-weight": "bold"}),
        html.Div(style={"width": "60%","margin": "0 auto", "gap": "20px"}, children=[ 
        dcc.Slider(
                id="month_slide",
                min = 0,
                max = 11,
                step = 1,
                value = 0,
                marks= {i: x.title() for i, x in enumerate(df['month'].unique())}
            )]),
        dcc.Graph(id="precipitation-graph")
    ]),

    #Third graph
    html.Div(children=[     
        html.H3("Monthly Climate by City",style = {"text-align": "center","font-weight": "bold"}),
        html.Div(style={"display": "flex","gap": "12px","justify-content": "center"}, children=[ 
            dcc.Dropdown(
                id="climate_dropdown",
                options=[{"label": symbol.replace("_", " ").title(), "value": symbol} for symbol in climate_weather],
                value="avg_temp_f",
                clearable=False
            ),
            dcc.Dropdown(
                id="city_dropdown",
                options=[{"label": symbol, "value": symbol} for symbol in df["city"].unique()],
                value=df["city"].unique(),
                multi=True
            ),]),
        dcc.Graph(id="city-climat")
    ])
])

#First graph
@app.callback(
    Output("heatmap-climat", "figure"),
    [Input("climate_dropdown2", "value"),]
)
def update_graph1(symbol):
    table = df.pivot_table(index="city",columns="month",values=symbol,sort=False)
    fig = px.imshow(table,labels=dict(x="Month", y="City", color=symbol), aspect="auto")
    return fig

#Second Graph
@app.callback(
    Output("precipitation-graph", "figure"),
    [Input("month_slide", "value"),]
)
def update_graph2(month):
    df_new = df[df['month'] == df["month"].unique()[month]]
    fig = px.bar( df_new, x="city", y="precipitation_inch", title=f"Precipitation in {df["month"].unique()[month]}" )
    return fig

#Third Graph
@app.callback(
    Output("city-climat", "figure"),
    [Input("climate_dropdown", "value"),
     Input("city_dropdown", "value"),]
)

def update_graph3(symbol,city):
    dff_new = df[df["city"].isin(city)]
    fig = px.line(dff_new, x="month", y=symbol, title=f"{symbol.replace("_", " ").title()} by Month",color="city")
    fig.update_layout(xaxis_title="Month", yaxis_title=symbol,legend_title="City",
    )
    return fig

if __name__ == "__main__": 
    app.run(debug=True) 