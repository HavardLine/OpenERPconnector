# -*- coding: utf-8 -*-
"""Module for daily verification

This module checks if it is time to lock into payments.

Example:
        $ python verify_payments.py

Attributes:
    none
"""


from drivers import odoo_connector
from datetime import timedelta, date, datetime
import logging


#Establish connection
con = odoo_connector.Connection()

#Find all supplier invoices not in draft
selection_invoices = con.searchRead('account.invoice', [[['journal_id','=', 2], ['state', '=', 'open']]], {'fields':['date_due', 'journal_id', 'number']}) #EXJ
#Compare due date and current date
for invoice in selection_invoices:
    limit = datetime.strptime(invoice['date_due'], '%Y-%m-%d').date() - timedelta(days=2)
    if limit <= date.today():
        logging.warning(invoice['journal_id'][1] + ' ' + invoice['number'] + ' has due date ' + invoice['date_due'])

#Find all customer invoices marked as open
selection_invoices = con.searchRead('account.invoice', [[['journal_id','=', 1], ['state', '=', 'open']]], {'fields':['date_due', 'journal_id', 'number']}) #SAJ
#Compare due date and current date
for invoice in selection_invoices:
    limit = datetime.strptime(invoice['date_due'], '%Y-%m-%d').date() + timedelta(days=14)
    if limit <= date.today():
        logging.warning(invoice['journal_id'][1] + ' ' + invoice['number'] + ' had due date ' + invoice['date_due'])
