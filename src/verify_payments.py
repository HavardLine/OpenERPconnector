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

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(filename)s:%(message)s")

file_handler = logging.FileHandler('log.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#Establish connection
con = odoo_connector.Connection()

#Find all supplier invoices not in draft
selection_invoices = con.searchRead('account.invoice', [[['journal_id','=', 2], ['state', '=', 'open']]], {'fields':['date_due', 'journal_id', 'number']}) #EXJ
#Compare due date and current date
for invoice in selection_invoices:
    limit = datetime.strptime(invoice['date_due'], '%Y-%m-%d').date() - timedelta(days=2)
    if limit <= date.today():
        logger.warning(invoice['journal_id'][1] + ' ' + invoice['number'] + ' has due date ' + invoice['date_due'])

#Find all customer invoices marked as open
selection_invoices = con.searchRead('account.invoice', [[['journal_id','=', 1], ['state', '=', 'open']]], {'fields':['date_due', 'journal_id', 'number']}) #SAJ
#Compare due date and current date
for invoice in selection_invoices:
    due_date = datetime.strptime(invoice['date_due'], '%Y-%m-%d').date()
    if (due_date + timedelta(days=14)) <= date.today():
        logger.warning(invoice['journal_id'][1] + ' ' + invoice['number'] + ' had due date ' + str((date.today()-due_date).days) + ' days ago')
