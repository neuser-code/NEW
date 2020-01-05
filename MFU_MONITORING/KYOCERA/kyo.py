#!/usr/bin/python3


# Опрос модели МФУ по SNMP и счетчика распечатанных листов.
# Модели P3050dn, M2035, M2040, M2135

import requests
import re
from sys import argv
from os import popen

ip_addr = argv[1]
kyo_model = popen(f'snmpget -v 2c -c public {ip_addr} iso.3.6.1.2.1.43.5.1.1.16.1').read().split(' ')[4].strip('\n, "')

def prnt_counter_P3050dn(ip_addr):
    prnt_count_url = f'http://{ip_addr}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
    headers = {'Referer': f'http://{ip_addr}/'}
    resp = requests.get(prnt_count_url, headers=headers)
    return int(re.findall('pp.printertotal\s=\s\W+(\d+)', resp.text)[0])

def prnt_counter_M2035dn(ip_addr):
    prnt_count_url = f'http://{ip_addr}/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.htm'
    headers = {'Referer': f'http://{ip_addr}/'}
    wakeup_url = f'http://{ip_addr}/esu/set.cgi'
    resp = requests.get(prnt_count_url, headers=headers)
    if not 'DeepSleep' in resp.text:
        counter0_copy = int(re.findall('counterBlackWhite\[0\]\s*\=\s*(\d+)', resp.text)[0])
        counter1_print = int(re.findall('counterBlackWhite\[1\]\s*\=\s*(\d+)', resp.text)[0])
        counter_total = counter0_copy + counter1_print
        return counter_total
    else:
        requests.post(wakeup_url, 'submit001=%D0%9F%D1%83%D1%81%D0%BA&okhtmfile=DeepSleepApply.htm&func=wakeup')
        
def prnt_counter_M2040dn(ip_addr):
    prnt_count_url = f'http://{ip_addr}/js/jssrc/model/dvcinfo/dvccounter/DvcInfo_Counter_PrnCounter.model.htm'
    headers = {'Referer': f'http://{ip_addr}/'}
    resp = requests.get(prnt_count_url, headers=headers)
    counter0_copy = int(re.findall('pp.copytotal\s=\s\W+(\d+)', resp.text)[0])
    counter1_print = int(re.findall('pp.printertotal\s=\s\W+(\d+)', resp.text)[0])
    counter_total = counter0_copy + counter1_print
    return counter_total

if 'P3050' in kyo_model:
    result = prnt_counter_P3050dn(ip_addr);print(result)
elif 'M2035' in kyo_model:
    result = prnt_counter_M2035dn(ip_addr);print(result)
elif 'M2040' or 'M2135' in kyo_model:
    result = prnt_counter_M2040dn(ip_addr);print(result)
else:
    print('Non known model')
