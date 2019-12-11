#!/usr/env/python3

# При подключении по SSTP к zyxel keenetic необходимо вручную прописать маршрут для vpn.
# Для примера с Биляром
import os
tun_ip = os.popen('ip addr show ppp0').read().split("inet ")[1].split("/")[0].split(" ")[0]
command = f'sudo route add -net 192.168.1.0/24 gw {tun_ip}'
