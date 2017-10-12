# -*- coding: utf-8 -*-
"""Module for daily verification

Example:
    none   

Attributes:
    none
"""
from drivers import odoo_connector
from datetime import timedelta, date, datetime
import logging, pprint

#Establish connection
con = odoo_connector.Connection()

moves = con.searchRead('account.invoice', [[['number', 'like', 'SAJ/2016/'], ['state', '=','open']]])

for move in moves:
    print(con.execute('account.invoice', 'write', [[move['id']], {'state': "paid"}]))
    print(move['id'])
#moves = con.searchRead('account.move', [[['name', '=', 'DIV/2017/0019']]])
#pprint.pprint(moves)
#print(con.execute('account.move', 'write', [[166], {'state': "draft"}]))
