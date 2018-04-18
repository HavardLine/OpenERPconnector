# -*- coding: utf-8 -*-
"""This module forces selected journals into draft state.

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
names = [
    'BNK2/2018/0076'
]

for name in names:
    moves = con.searchRead('account.move', [[['name', '=', name]]])
    if len(moves) == 1:
        move_id = moves[0]['id']
        if con.execute('account.move', 'write', [[move_id], {'state': "draft"}]):
            logging.warning(name + ', move id '+str(move_id)+' are now in draft state')
    else:
        logging.warning('failed to find record')