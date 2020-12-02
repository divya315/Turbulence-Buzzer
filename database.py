#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import sqlite3
import datetime
import urllib.request

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
def data_entry():
        time_object=datetime.datetime.now()
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        c.execute('INSERT INTO reading(datetime,sensordata) VALUES(?,?)',(time_object,var))
        c.close()
        conn.close()
def stored_data():
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        c.execute('SELECT * FROM reading ORDER BY datetime DESC')
        rows=c.fetchall()
        for row in rows:
                 l_read=row
                 print(l_read)
                 c.execute("DELETE FROM reading WHERE ID=?",str(row[0]))
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



def active(led):
    GPIO.output(led,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led,GPIO.LOW)
    time.sleep(0.5)
def callback(channel):
    global var
    if GPIO.input(channel):
        print("Movement Detected!")
        var="Vibration Detected"
        active(led)
        try:
                x=urllib.request.urlopen('https://www.google.com/')
                status="Connected"
                print(status)
        except:
                status="Not Connected"
        if status=="Connected":
                data_entry()
                stored_data()
GPIO.add_event_detect(channel, GPIO.RISING, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
try:
    while True:
        time.sleep(0.5)
  
except KeyboardInterrupt:
        table_clear()
        l_read.clear()
        GPIO.cleanup()