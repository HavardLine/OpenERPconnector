# -*- coding: utf-8 -*-
"""Module for importing payment

Example:
        $ python payment.py

Attributes:
    none
"""
import pprint, json
from os import path
#print(os.path.dirname(os.path.realpath(__file__)))

with open(path.dirname(path.realpath(__file__)) + '\\payment.yml', "r") as f: 
#	file_buffer = f.read()

    payment_table = json.load(f)#['payment_type']

#pprint.pprint(payment_table)

for entry in payment_table['payment_type']:
    print(entry['calc_feriepenger'])
    #print(entry['name'])

f.close()
