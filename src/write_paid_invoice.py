# -*- coding: utf-8 -*-
"""Some invoices will not go to the paid state from the user interface. This scrip helps doing that.

Example of use:
    - Change the names variable
    - Run the script
"""
from drivers import odoo_connector
from datetime import timedelta, date, datetime
import logging, pprint

#Establish connection
con = odoo_connector.Connection()
names = [
    'EXJ/2018/0058',
]

for name in names:
    moves = con.searchRead('account.invoice', [[['number', '=', name]]])
    if len(moves) == 1:
        move_id = moves[0]['id']
        if con.execute('account.invoice', 'write', [[move_id], {'state': "paid"}]):
            logging.warning(name + ', move id '+str(move_id)+' are now in paid state')
    else:
        logging.warning('failed to find record')