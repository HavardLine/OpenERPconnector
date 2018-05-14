# -*- coding: utf-8 -*-
"""Module for importing journals from .xlsx files.
The code is written with norwegian payments in mind.

Example:
    none   

Attributes:
    none
"""
from pprint import pprint
from os import listdir, makedirs
import erppeek, hashlib, logging, os.path, pandas
from base64 import b64decode

def save_base64_data(data, path):
    with open(path, "wb") as fh:
        fh.write(b64decode(data))

def download_attachements(attachment_ids, base_path, file_prefix=''):
    # Loop attachements for this move
    for attachment_id in attachment_ids:
        data = client.read('ir.attachment', attachment_id, 'db_datas name')
        file_name = file_prefix + data['name']
        path = base_path + '\\' + file_name
        path_new = base_path + '\\new\\' + file_name
        path_conflicting = base_path + '\\conflicting\\' + file_name

        # Verify that database has content
        if data['db_datas']:
            # Check if file exists
            if os.path.isfile(path):
                # File exists. Validate checksum
                logging.debug('File '+path+' exists. Validating checksum')
                checksum1 = hashlib.sha256(b64decode(data['db_datas'])).hexdigest()
                with open(path, "rb") as f1:
                    checksum2 = hashlib.sha256(f1.read()).hexdigest()

                if checksum1 != checksum2:
                    # File and database has conflicting checksums.
                    # Save in path_conflicting.
                    logging.warning('File '+path+' has conflicting checksum.')
                    logging.debug('Saving conflicting file at '+path_conflicting)
                    save_base64_data(data['db_datas'], path_conflicting)
                else:
                    # File and database has equal checksums.
                    # No need to save anything.
                    logging.debug('File '+path+' has equal checksum.')
            else:
                # File in database does not exist in filesystem.
                # Save new file in path_new
                logging.info('Saving new file at '+path_new)
                save_base64_data(data['db_datas'], path_new)
        else:
            logging.debug('No data at attachment_id ' + str(attachment_id)+' path ' +path)

def download_move_attachements(base_path, resource_model):
    move_ids = client.search(resource_model)
    moves = client.read(resource_model ,move_ids)
    
    # Looping account.move elements
    for move in moves:
        if resource_model == 'account.invoice':
            file_prefix = move['number'][:-10]+'-' + move['number'][-4:] + '-'
        else:
            file_prefix = move['name'][:-10]+'-' + move['name'][-4:] + '-'
        condition = ['res_id = '+ str(move['id']), 'res_model = '+resource_model]
        attachment_ids = client.search('ir.attachment', condition)
        download_attachements(attachment_ids, base_path, file_prefix)

if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    client = erppeek.Client.from_config(environment='DEFAULT')
    destination = 'L:\\accounting\\vedlegg'
    res_models = ['account.move', 'account.invoice']
    for res_model in res_models:
        download_move_attachements(destination, res_model)
    logging.info('Script read_attachments.py finished')
   