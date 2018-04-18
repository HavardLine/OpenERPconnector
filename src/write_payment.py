# -*- coding: utf-8 -*-
"""Module for importing journals from .xlsx files.
The code is written with norwegian payments in mind.

Example:
    none   

Attributes:
    none
"""
from pprint import pprint
from os import listdir
import pandas, logging, erppeek

def uppload_move_attachement(src, file_name, resource_id):
    # Delete attachment(s)
    attachments = client.read('ir.attachment', ['res_model = account.move', 'res_id = ' + str(resource_id)], 'id res_model datas_fname')
    if len(attachments) > 0:
        attachment_ids = []
        for attachment in attachments:
            attachment_ids.append(attachment['id'])
        client.unlink('ir.attachment', attachment_ids)
        logging.debug('Deleted attachments '+str(attachment_ids))

    # Upload new attachment
    from base64 import b64encode
    file_content = b64encode(open(src+'\\'+file_name, 'rb').read())
    uppload_content = {'db_datas': file_content, 'res_model': 'account.move', 'name': file_name, 'type': 'binary', 'res_id': resource_id}
    if client.create('ir.attachment', uppload_content):
        logging.debug('File "' + file_name+ '", uploaded')
    else:
        logging.critical('File "' + file_name+ '", failed to upload')
        exit(1)


if __name__ == '__main__':
    # General setup
    logging.basicConfig(level="DEBUG")
    client = erppeek.Client.from_config(environment='DEFAULT')
    src = 'L:\\accounting\\lønn'
    files = listdir(src)
    logging.debug('Found '+str(len(files))+' file(s)')
    
    # Loop all files
    for file_name in files:
        logging.debug('Reading '+file_name)
        domain = [
            'journal_id = 5',
            'ref = '+file_name
            ]

        # Count ODOO-journals that refer to the same file
        count = client.count('account.move', domain)
        logging.debug('Found '+str(count)+' match for '+file_name)
        
        # Continue only if one journal refers to the file
        if count > 1:
            logging.critical('Multiple journals exist for "'+file_name+'". Delete records and try new import.')
            exit(1)
        if count != 1:
            logging.critical('No journals exist for "'+file_name+'". Add journal and try new import.')
            exit(1)
            logging.debug('Evaluating '+file_name)
            
        # Read data from file
        df = pandas.read_excel(open(src +'\\'+ file_name,'rb'), sheetname='Lønn', header=10, skip_footer=3, index_col=None).fillna(0.0).round(2)
        # Remove lines where debit and credit is 0.0
        df = df.drop(df[(df.Debit == 0.0) & (df.Credit == 0.0)].index)
        # Read existing journal
        move_data = client.read('account.move', domain, 'id line_id date journal_id period_id')[0]
        move_id = move_data['id']
        lines_id = move_data['line_id']
        lines_new = False
        logging.debug('Changing account.move to draft state')
        client.write('account.move', move_id, {'state': "draft"})
        
        if len(lines_id) > 0:
            partner_id = client.read('account.move.line', lines_id[0], 'partner_id')[0]
        else:
            partner_id = False

        logging.debug('Reading existing partner_id: '+str(partner_id))
        
        if len(lines_id) != df.shape[0]:
            logging.debug(file_name+' has ' +str(df.shape[0])+ ' elements. Journal has ' + str(len(lines_id)) + '.')
            if lines_id != []:
                logging.info('Deleting account.move.line ids '+str(lines_id))
                client.unlink('account.move.line', move_data['line_id'])
            lines_new = True
        else:
            logging.debug('Matching number of journal line elements. Moving on.')

        i=0
        for index, row in df.iterrows():
            account_code = str(row['Konto'])
            account_ids = client.search('account.account', ['code = '+account_code])
            if len(account_ids) != 1:
                logging.critical('Unable to find unique record for account '+account_code)  
                exit(1)

            if lines_new:
                dataset = {
                'account_id': account_ids[0],
                'name': index,
                'debit': row['Debit'],
                'credit': row['Credit'],
                'date': move_data['date'],
                'journal_id': 5,
                'move_id': move_data['id'],
                'partner_id': partner_id,
                'period_id': move_data['period_id'][0],
                }
                lines_id.append(client.create('account.move.line', dataset))
                logging.debug('Appended account.move.line '+str(lines_id[-1]))
            else:
                dataset = {
                'name': index,
                'account_id': account_ids[0],
                'credit': row['Credit'],
                'debit': row['Debit'],
                'partner_id': partner_id,
                }
                client.write('account.move.line', lines_id[i], dataset)
                logging.debug('Replaced account.move.line '+str(lines_id[i]))
            i+=1
        logging.debug('Upploading '+file_name)
        uppload_move_attachement(src, file_name, move_id)
        logging.info(file_name+' OK')
