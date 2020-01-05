# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 14:55:16 2017 http://micropython.org/webrepl
Управление светодиодной матрицей по протоколу mqtt
@author: alexander
"""
#################
from umqtt.simple import MQTTClient
import ubinascii
import machine
import time
import ntptime
import neopixel
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
SERVER = "m12.cloudmqtt.com"
TOPIC_red = b"red1"
TOPIC_green = b"green1"
TOPIC_blue = b"blue1"
TOPIC_cmd = b"newsub1"
TOPIC3 = b"public31"
pix = neopixel.NeoPixel(machine.Pin(5), 256)
red = 0; green = 0; blue = 0
pixel = [red, green, blue]

m = [[x for x in range(0,16)] for k in range(0, 16)]
k = 0
for i in range(0, 16):
        for d in range(0,16):
                m[i][d] = [k, (0,0,0)]
                k += 1

for t in range(0, 16):
        if t % 2 != 0:
                m[t].reverse()


def sub_cb(topic, msg):
    global tm_1
    print((topic, msg))
    tm = time.localtime()
    tm_1 = time.localtime(time.mktime((tm[0], tm[1], tm[2], tm[3]+3, tm[4], tm[5], tm[6], tm[7])))
    d = (topic, msg)
    if d[0] == b'red1':
        pixel[0] = int(msg.decode())
    elif d[0] == b'green1':
        pixel[1] = int(msg.decode())
    elif d[0] == b'blue1':
        pixel[2] = int(msg.decode())
    elif d[0] == b'newsub1':
        if str(msg.decode()) == "paint":
            paint()
        elif str(msg.decode()) == "smile":
            pict()

def paint():
    for i in range(0,256):
        pix[i] = (pixel[0], pixel[1], pixel[2])
    pix.write()

def pict():
    for k in range(0,16):
        for i in range(0,16):
            pix[m[k][i][0]] = m[k][i][1]
    pix.write()


def tst2(server=SERVER):
    n = 0
    m = 0
    ntptime.settime()
    global tm_1
    tm = time.localtime()
    tm_1 = time.localtime(time.mktime((tm[0], tm[1], tm[2], tm[3]+3, tm[4], tm[5], tm[6], tm[7])))
    fail = False
    c = MQTTClient(CLIENT_ID, SERVER, user="ondainjc", password="PzGOg0B7lF8I", port=18634)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC_red)
    time.sleep_ms(100)
    c.subscribe(TOPIC_green)
    time.sleep_ms(100)
    c.subscribe(TOPIC_blue)
    c.subscribe(TOPIC_cmd)
    print("Connected")
    while 1:
        time.sleep_ms(200)
        try:
            c.check_msg()
            fail = False
        except OSError:
            fail = True
        n+=1
        m+=1
        if n > 80:
            minute = tm_1[4]
            if len(str(minute)) == 1:
                minute = '0'+str(minute)
            mess = str(tm_1[2])+' '+str(tm_1[1])+' '+str(tm_1[3])+':'+str(minute)
            try:
                c.publish(TOPIC3, mess)
                n = 0
                fail = False
            except OSError:
                fail = True
        if m > 38000:
            try:
                ntptime.settime()
                m = 0
                fail = False
            except OSError:
                fail = True
        if fail:
            print('Reconnecting...')
            try:
                c.connect()
                time.sleep_ms(100)
                c.subscribe(TOPIC_red)
                time.sleep_ms(100)
                c.subscribe(TOPIC_green)
                time.sleep_ms(100)
                c.subscribe(TOPIC_blue)
                time.sleep_ms(100)
                c.subscribe(TOPIC_cmd)
                fail = False
            except OSError:
                print('Reconnect fail')
                fail = True

