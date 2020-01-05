import neopixel
from machine import Pin

pix = neopixel.NeoPixel(machine.Pin(5), 256)
color = {'red':'0', 'green':'0', 'blue':'0'}

def paint(r,g,b):
    for k in range(0,256):
        pix[k] = (r, g ,b)
        if k % 16 == 0:
            pix.write()
    pix.write()



#paint(int(color['red']), int(color['green']), int(color['blue']))
