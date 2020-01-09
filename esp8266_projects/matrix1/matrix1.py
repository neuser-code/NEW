# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 14:55:16 2017 http://micropython.org/webrepl
Управление светодиодной матрицей по протоколу mqtt
@author: alexander
"""

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
<<<<<<< HEAD
global t
global tm_1
global red_level; red_level = 0
global green_level; green_level = 0
global blue_level; blue_level = 0

l1 = range(0, 17)
l2 = range(31, 15, -1)
l3 = range(32, 48)
l4 = range(63, 47, -1)
l5 = range(64, 80)
l6 = range(95, 79, -1)
l7 = range(96, 112)
l8 = range(127, 111, -1)
l9 = range(128, 144)
l10 = range(159, 143, -1)
l11 = range(160, 176)
l12 = range(191, 175, -1)
l13 = range(192, 208)
l14 = range(223, 207, -1)
l15 = range(224, 240)
l16 = range(255, 239, -1)

t = (l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16)

def sub_cb(topic, msg):
    global t
    global tm_1
    global red_level
    global green_level
    global blue_level
=======
red = 0; green = 0; blue = 0
pixel = [red, green, blue]

picture_list = ['sneg', 'cross', 'smile', 'elka', 'puzyirki']

def json_file_2_obj(file):
    import json
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

m = []

def sub_cb(topic, msg):
    global tm_1
>>>>>>> new
    print((topic, msg))
    tm = time.localtime()
    tm_1 = time.localtime(time.mktime((tm[0], tm[1], tm[2], tm[3]+3, tm[4], tm[5], tm[6], tm[7])))
    d = (topic, msg)
    if d[0] == b'red1':
<<<<<<< HEAD
        red_level = int(msg.decode())
    elif d[0] == b'green1':
        green_level = int(msg.decode())
    elif d[0] == b'blue1':
        blue_level = int(msg.decode())
    elif d[0] == b'newsub1':
        if str(msg.decode()) == "paint":
            paint()
        elif str(msg.decode()) == "smile":
            sm()

def paint():
    global red_level
    global green_level
    global blue_level
    for i in range(0,256):
        pix[i] = (red_level, green_level, blue_level)
    pix.write()
    

def sm():
    global t
    global red_level
    global green_level
    global blue_level
    r = red_level
    g = green_level
    b = blue_level
    for j in (2,3,12,13):
        pix[t[1][j]] = (r,g,b);pix[t[14][j]] = (r,g,b);pix[t[j][14]] = (r,g,b);pix[t[j][1]] = (r,g,b)
    for j in range(3, 13):
        pix[t[0][j]] = (r,g,b);pix[t[15][j]] = (r,g,b);pix[t[j][0]] = (r,g,b); pix[t[j][15]] = (r,g,b)
    for i in (4,5):
        for j in (4,5):
            pix[t[i][j]] = (r,g,b)
    for i in (10,11):
        for j in (4,5):
            pix[t[i][j]] = (r,g,b)
    for i in range(5,11):
        pix[t[i][12]] = (r,g,b)
    pix[t[4][11]] = (r,g,b);pix[t[11][11]] = (r,g,b)
=======
        pixel[0] = int(msg.decode())
    elif d[0] == b'green1':
        pixel[1] = int(msg.decode())
    elif d[0] == b'blue1':
        pixel[2] = int(msg.decode())
    elif d[0] == b'newsub1':
        if str(msg.decode()) == "paint":
            paint()
        elif str(msg.decode()) in picture_list:
            m = json_file_2_obj(msg.decode())
            pict(m)

def paint():
    for i in range(0,256):
        pix[i] = (pixel[0], pixel[1], pixel[2])
    pix.write()

def pict(m):
    for k in m:
        pix[k] = (pixel[0], pixel[1], pixel[2])
>>>>>>> new
    pix.write()


def tst2(server=SERVER):
    n = 0
    m = 0
    ntptime.settime()
<<<<<<< HEAD
    global t
=======
>>>>>>> new
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
<<<<<<< HEAD

=======
>>>>>>> new
