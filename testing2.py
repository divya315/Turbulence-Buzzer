#!/usr/bin/python
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import sqlite3
import datetime
import urllib.request
import socket

broker_url="188.42.97.81"
broker_port=1883

#GPIO SETUP
channel = 38
led=8
var=""
l_read=[]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
conn=sqlite3.connect('database.db')
c=conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS reading(ID INTEGER PRIMARY KEY AUTOINCREMENT,datetime text,sensordata text)''')
status="Not Connected"
def on_connect(client,userdata,flags,rc):
    print("CONNECTED WITH RESULT CODE {}".format(rc))
def on_publish(client,userdata,mid):
    print ("Message published with mid value as ...."+str(mid))
def disconnect(client,userdata,rc):
    print("DISCONNECTED")
def active(led):
    GPIO.output(led,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led,GPIO.LOW)
    time.sleep(0.5)
def data_entry():
        time_object=datetime.datetime.now()
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        c.execute("INSERT INTO reading(datetime,sensordata) VALUES(?,?);",(time_object,var))
        print("data entered")
        conn.commit()
        c.close()
        conn.close()
def stored_data():
        i=""
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        c.execute('SELECT * FROM reading ORDER BY datetime DESC')
        rows=c.fetchall()
        for row in rows:
                 l_read=row
                 print(l_read)
                 if var=="Vibration Detected":
                     ret1=client.publish(topic="vbox/test/user/vibration",payload=var,qos=1,retain=False)
                     print(ret1)
                     if ret1[0]==0:
                         i=str(row[0])
                         c.execute("DELETE FROM reading WHERE ID=?",i)
                         print("reading deleted")
                         conn.commit()
        c.close()
        conn.close()
def table_clear():
    conn=sqlite3.connect('database.db')
    c=conn.cursor()
    c.execute('DROP TABLE reading')
    conn.commit()
    c.close()
    conn.close()


def callback(channel):
    global var
    if GPIO.input(channel):
        print("Movement Detected!")
        var="Vibration Detected"
        active(led)
        try:
            socket.create_connection(("www.google.com", 80))
            status="Connected"
            print(status)
        except OSError:
            pass
            status="Not Connected"
            print(status)
        if status=="Connected":
            if var=="Vibration Detected":
                ret=client.publish(topic="vbox/test/user/vibration",payload=var,qos=1,retain=False)
                print(ret)
                if ret[0]!=0:
                    data_entry()
                else:
                    stored_data()
        else:
            data_entry()
                
client=mqtt.Client()
client.username_pw_set("",password="")
client.on_connect=on_connect
client.on_publish=on_publish
client.connect(broker_url,broker_port,keepalive=60)
GPIO.add_event_detect(channel, GPIO.RISING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
client.loop_forever()


try:
    while True:
        time.sleep(2)
  
except KeyboardInterrupt:
    table_clear()
    l_read.clear()
    GPIO.cleanup()