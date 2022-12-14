from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import json


# returns JSON object as
# a dictionary

app_version = 1.30
with open('weather.json', 'r') as file:
    json_data = json.load(file)

token = "whcBdFBOMnUYN4cg7awyH-k8xGNmpxFgiFop6eX4OT68RTgcmd-Vt-B5L3XgNf2S58-I93DH7pFeoKPYCqZjCQ=="
org = "Aakash.shrestha@ui.city"
bucket = "weather"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org, default_tags={'appversion': str(app_version)}, debug=False) as client:
    def flatten_interval(interval):
        values = interval['values']
        values['startTime'] = interval['startTime']
        return values


    # get timelines
    timelines = json_data['data']['timelines']
    # get intervals
    intervals = list(map(lambda timeline: timeline['intervals'], timelines))
    # flatten intervals
    intervals = [flatten_interval(interval) for sublist in intervals for interval in sublist]
    for i in intervals:
        if i.get('temperature') == int(i.get('temperature')):
            i['temperature']= float(i.get('temperature'))
        if i.get('humidity') == int(i.get('humidity')):
            i['humidity'] = float(i.get('humidity'))
        if i.get('windSpeed') == int(i.get('windSpeed')):
            i['windSpeed'] = float(i.get('windSpeed'))
        #print (intervals)
        # temperature = i.get('temperature')
        # if temperature == int(temperature):
        #     temperature = float(temperature)
        # humidity = i.get('humidity')
        # if humidity == int(humidity):
        #     humidity = float(humidity)
        # windSpeed = i.get('windSpeed')
        # if windSpeed == int(windSpeed):
        #     windSpeed = float(windSpeed)
        # print(i)
            
    # write data
    client.write_api(write_options=SYNCHRONOUS).write(bucket=bucket,
                                                      record=intervals,
                                                      record_measurement_name="weather",
                                                      record_time_key="startTime",
                                                      record_field_keys=["humidity", "temperature", "windSpeed"])