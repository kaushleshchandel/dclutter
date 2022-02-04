
import argparse
import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
import sys

#topic = sys.argv[0]
topic = sys.argv[1]
value = sys.argv[2]

broker_address="10.0.2.201"
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
client.publish(topic ,value, qos=0,retain=True)
time.sleep(4) # wait
client.loop_stop() #stop the loop