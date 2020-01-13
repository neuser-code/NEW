#!/usr/bin/python3
import requests
import re
from sys import argv
import json

ip_addr = argv[1]

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


def kyo_model_via_http(ip_addr):
    headers = {'Referer': f'http://{ip_addr}'}
    url = f'http://{ip_addr}/js/jssrc/model/startwlm/Start_Wlm.model.htm' #3050dn, 2040dn, 2135
    resp = requests.get(url, headers=headers)
    if '404' in resp.text:
        url = f'http://{ip_addr}/startwlm/Start_Wlm.htm' #2035dn
        resp = requests.get(url, headers=headers)
    elif 'DeepSleep' in resp.text:
        headers = {'Referer': f'http://{ip_addr}/DeepSleep.htm'}
        url = f'http://{ip_addr}/DeepSleep.js' #sleeping
        resp = requests.get(url, headers=headers)
        wakeup_url = f'http://{ip_addr}/esu/set.cgi'
        requests.post(wakeup_url, 'submit001=%D0%9F%D1%83%D1%81%D0%BA&okhtmfile=DeepSleepApply.htm&func=wakeup')
    model = 'UNKNOWN'
    Prnt_count = 0
    if 'ECOSYS P3050dn' in resp.text:
        model = "P3050dn"; Prnt_count = prnt_counter_P3050dn(ip_addr)
    elif 'ECOSYS M2040dn' in resp.text:
        model = 'M2040dn'; Prnt_count = prnt_counter_M2040dn(ip_addr)
    elif 'ECOSYS M2135dn' in resp.text:
        model = 'M2135dn'; Prnt_count = prnt_counter_M2040dn(ip_addr)
    elif 'ECOSYS M2035dn' in resp.text:
        model = 'M2035dn'; Prnt_count = prnt_counter_M2035dn(ip_addr)
    return {"model": model, "pages": Prnt_count}


print(json.dumps(kyo_model_via_http(ip_addr)))
