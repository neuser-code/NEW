# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 20:42:03 2018

@author: alexander
"""

from umqtt.simple import MQTTClient
import ubinascii
import time
import socket
import ntptime
import machine
from machine import Pin
pinrelay = [machine.Pin(i, machine.Pin.OUT, value=1) for i in (4, 5, 12, 13)]
SERVER = "m12.cloudmqtt.com"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC1 = b"sub"
TOPIC2 = b"public"
offset=3

def sub_cb(topic, msg):
    print((topic, msg))
    global dt
    dt = eventtime()
    for i in range (1, int(len(pinrelay)+1)):
        if msg.decode() == "on"+str(i):
            pinrelay[i-1].value(0)
        elif msg.decode() == "off"+str(i):
            pinrelay[i-1].value(1)
            
def eventtime(offset=3):
    tm = time.localtime()
    tm_1 = time.localtime(time.mktime((tm[0], tm[1], tm[2], tm[3]+offset, tm[4], tm[5], tm[6], tm[7])))
    minute = tm_1[4]
    if len(str(minute)) == 1:
        minute = '0'+str(minute)
    t = str(tm_1[2])+' '+str(tm_1[1])+' '+str(tm_1[3])+':'+str(minute)
    return(t)
    
def relaystate():
    state = []
    for i in range (0, len(pinrelay)):
        if pinrelay[i].value() == 1:
            f = "R"+str(i+1)+"_OFF"
            state.append(f)
        elif pinrelay[i].value() == 0:
            f = "R"+str(i+1)+"_ON"
            state.append(f)
    return(state)
    
def test_broker(name, port):
    try:
        tst = socket.getaddrinfo(name, port)
        return(True)
    except OSError:
        return(False)    
    
def main(server=SERVER):
    global dt
    n = 0
    m = 0
    while m < 4:
        try:
            ntptime.settime()
            break
        except OSError:
            time.sleep(1)
            m += 1
    fail = False
    dt = eventtime()
    try:
        c = MQTTClient(CLIENT_ID, SERVER, user="ondainjc", password="PzGOg0B7lF8I", port=18634)
    except OSError:
        fail = True
    if not fail:
        try:
            c.set_callback(sub_cb)
            c.connect()
            c.subscribe(TOPIC1)
        except OSError:
            fail = True
    print("Connected to %s, subscribed to %s topic" % (server, TOPIC1))
    while 1:
        time.sleep_ms(200)
        if not fail:
            try:
                c.check_msg()
            except OSError:
                fail = True
        n += 1
        m += 1
        if n % 80 == 0:
            state = relaystate()
            mess = str(dt)+" "+str(state[0])+" "+str(state[1])+" "+str(state[2])+" "+str(state[3])
            if not fail:
                try:
                    c.publish(TOPIC2, mess)
                except OSError:
                    fail = True
        if n > 320:
            n = 0
            if test_broker(SERVER, 18634):
                print ("Broker UP")
                fail = False
            else:
                print("Broker DOWN")
                fail = True
        if m > 38000:
            m = 0
            if not fail:
                try:
                    ntptime.settime()
                except OSError:
                    pass
        if fail:
            if test_broker(SERVER, 18634):
                try:
                    c = MQTTClient(CLIENT_ID, SERVER, user="ondainjc", password="PzGOg0B7lF8I", port=18634)
                    c.set_callback(sub_cb)
                    c.connect()
                    print("Conected")
                    c.subscribe(TOPIC1)
                    print("Listen command")
                    fail = False
                except OSError:
                    time.sleep(2)
                    fail = True

