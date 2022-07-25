# Live Weather
## To run the system: Execute the following commands in the given order for each socket.
###To run Websocket:
- python3 websocket_server.py
- python3 websocket_RPi_client.py
- python3 dashboard.py
  - then open the link shown in the terminal to see the dashboard on the web
###To run MQTT:
- python3 mqtt_publisher.py
- python3 mqtt_subscriber_server.py
- python3 dashboard.py
  - then open the link shown in the terminal to see the dashboard on the web
