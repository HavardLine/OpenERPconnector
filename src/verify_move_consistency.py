# -*- coding: utf-8 -*-
"""Module for daily verification

Example:
    none

Attributes:
    none
"""
from drivers import odoo_connector
import logging, pprint

#Establish connection
con = odoo_connector.Connection()

#Find all supplier invoices not in draft
moves = con.searchRead('account.move')


inconsistent_records = []
for move in moves:
    # Verify that account.move and account.move.line is consistent
    lines = con.read('account.move.line', move['line_id'])
    move_error = False
    for line in lines:
        if move['date'] != line['date']:
            move_error = True
        if move['period_id'] != line['period_id']:
            move_error = True
    if(move_error):
        inconsistent_records.append(move['id'])
        logging.warning(move['journal_id'][1] + ' id=' + str(move['id']) + ' ' + move['name'] + ' dated ' + move['date'] + ' has inconsistent data')

if inconsistent_records:
    print('inconsistent_records: ', inconsistent_records)
print(len(moves), 'moves analyzed')
