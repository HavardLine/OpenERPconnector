# -*- coding: utf-8 -*-
"""Module for daily verification

Example:
        $ python verify_move_periods.py

Attributes:
    none
"""
from drivers import odoo_connector
from os.path import split
from logging import getLogger, WARNING, Formatter
from datetime import timedelta, date, datetime
from drivers.aws_logger import MqttHandler

# Establish MQTT-logger
logger = getLogger('accounting/' + split(__file__)[-1])
logger.setLevel(WARNING)
formatter = Formatter("%(asctime)s:%(name)s:%(levelname)s:%(filename)s:%(message)s")
mqtt_handler = MqttHandler()
mqtt_handler.setFormatter(formatter)
logger.addHandler(mqtt_handler)

#Establish connection
con = odoo_connector.Connection()

#Find all supplier invoices not in draft
moves = con.searchRead('account.move')

for move in moves:
    # Verify period against date
    if (move['date'][:4] != move['period_id'][1][-4:]) or (move['date'][5:7] != move['period_id'][1][:2]):
        logger.warning(move['journal_id'][1] + ' ' + move['name'] + ' dated ' + move['date'] + ' has conflicting period and date')
logger.debug(str(len(moves)) + ' moves analyzed')

# Publish all warning to shadow
mqtt_handler.publish_to_shadow(logger.name)