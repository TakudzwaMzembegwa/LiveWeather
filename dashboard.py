# importing packages
import dash
from dash import dcc
from dash import html
import pandas as pd
from datetime import datetime
import sqlite3
import random
import dash_daq as daq
from dash.dependencies import Input, Output
last_time, cur_temperature, cur_pressure, cur_humidity = 0, 0, 0, 0
def read_all(last):    
    global last_time, cur_temperature, cur_pressure, cur_humidity
    conn = sqlite3.connect('SENSEHAT.db')
    print("Opened database successfully")
    cursor = conn.execute(f"SELECT id, temperature, pressure, humidity from SENSEHAT WHERE ID>{last}")
    data = []
    for row in cursor:
        last_time = row[0]
        data.append([datetime.fromtimestamp(int(row[0])).strftime("%H:%M:%S"), row[1], row[2], row[3]])#"%H:%M:%S-%d/%m"
    conn.close()
    cur_temperature, cur_pressure, cur_humidity = data[-1][1], data[-1][2], data[-1][3]
    return data
data = pd.DataFrame(read_all(0),
                  columns = ['Date', 'Temperature', 'Pressure', 'Humidity'])
count = 0
# initialisation and manipulation of data
#data = pd.read_csv("https://raw.githubusercontent.com/ThuwarakeshM/geting-started-with-plottly-dash/main/life_expectancy.csv")
#data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%d-%m-%Y')
app = dash.Dash(__name__)
 
# Initialising the application.
app.layout=html.Div(
    children=[
        html.H1(children="3805515 IoT project", style={'textAlign': 'center', 'color':'red', 'font-size':'60px'}),
        html.H1(children="Graphical Presentation", style={'textAlign': 'center'}),
        dcc.Interval(
            id='interval-component',
            interval=3*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Graph(id='graph', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='graph1', style={'width': '50%', 'display': 'inline-block'}),
        html.H1(children="Sensor readings", style={'textAlign': 'center'}),
        daq.Gauge(
            id='pressure',
            color={"gradient":True,"ranges":{"green":[260,650],"yellow":[650,1110],"red":[1110,1260]}},
            value=900,
            label='Pressure',
            max=1260,
            min=260,
            showCurrentValue=True,
            units="mbar",
            style={'width': '33%', 'display': 'inline-block'}),
        daq.Thermometer(
            id='thermo',
            color='red',
            value=27,
            height=250,
            width=10,
            max=100,
            min=0,
            label='Tempeture',
            showCurrentValue=True,
            units="C",
            style={'width': '33%', 'display': 'inline-block'}),
        daq.Gauge(            
            id='humidity',
            color={"gradient":True,"ranges":{"green":[0,33],"yellow":[33,66],"red":[66,100]}},
            value=26,
            label='Humidity',
            max=100,
            min=0,
            showCurrentValue=True,
            units="%",
            style={'width': '33%', 'display': 'inline-block'})
        
] )
@app.callback(
    Output('thermo', 'value'),
    [Input('interval-component', "n_intervals")]
)
def update_output(value):
    return cur_temperature

@app.callback(
    Output('humidity', 'value'),
    [Input('interval-component', "n_intervals")]
)
def update_output1(value):
    return  cur_humidity

@app.callback(
    Output('pressure', 'value'),
    [Input('interval-component', "n_intervals")]
)
def update_output2(value):
    return cur_pressure
    
# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig(value):

    global data, count
    df2 = pd.DataFrame(read_all(last_time), columns = ['Date', 'Temperature', 'Pressure', 'Humidity'])
    count =  count + 5
    data = data.append(df2)#.reset_index()
    figure={
                "data":[
                    {
                        "x":data["Date"],
                        "y":data["Temperature"],
                        "type":"lines",
                    },
                ],
                "layout":{"title":"Second-wise Temperature readings"},
                   }
    return(figure)
#Define callback to update graph
@app.callback(
    Output('graph1', 'figure'),
    [Input('interval-component', "n_intervals")]
)
def streamFig1(value):

    global data, count
    df2 = pd.DataFrame(read_all(last_time), columns = ['Date', 'Temperature', 'Pressure', 'Humidity'])
    count =  count + 5
    data = data.append(df2)#.reset_index()
    figure={
                "data":[
                    {
                        "x":data["Date"],
                        "y":data['Pressure'],
                        "type":"lines",
                    },
                ],
                "layout":{"title":"Second-wise Pressure readings"},
                   }
    return(figure)
# deploying server
if __name__ == "__main__":
    app.run_server(debug=True)    