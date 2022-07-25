# Live Weather
Live weather systems using 2 different protocols (WebSockets and MQTT).
The systems get temperature, humidity and pressure readings from sensors on a Raspberry Pi. From the Raspberry Pi sensors the data is then saved into an embedded database. Using WebSockets or MQTT the data is continuously transported to the dashboard(s).
## MQTT
### Architecture
![MQTT](https://github.com/TakudzwaMzembegwa/LiveWeather/blob/master/assets/images/MQTT.JPG)
### To run MQTT:
1. python3 mqtt_publisher.py
2. python3 mqtt_subscriber_server.py
3. python3 dashboard.py
4. **Then** open the link shown in the terminal to see the dashboard on the web

## Websocket
### Architecture
![WebSocket](https://github.com/TakudzwaMzembegwa/LiveWeather/blob/master/assets/images/websocket.JPG)
### To run Websocket:
1. python3 websocket_server.py
2. python3 websocket_RPi_client.py
3. python3 dashboard.py
4. **Then** open the link shown in the terminal to see the dashboard on the web

# Dashboard
## Web Dashboard
![Dashboard](https://github.com/TakudzwaMzembegwa/LiveWeather/blob/master/assets/images/dash.jpeg)
## Desktop Dashboard
![PLT](https://github.com/TakudzwaMzembegwa/LiveWeather/blob/master/assets/images/plt.jpeg)

