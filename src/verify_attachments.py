from logging import error
from os.path import split
from drivers import odoo_connector
from pprint import pprint

def run():
    #Establish connection
    con = odoo_connector.Connection()

    #find all attachements in the account.move category
    attachment_account_invoice = con.searchRead('ir.attachment', [[['res_model','=','account.invoice'], ['db_datas','<>', None]]], {'fields': ['name', 'res_id', 'id']})
    attachment_res_ids = []
    for attachment in attachment_account_invoice:
        attachment_res_ids.append(attachment['res_id'])
    #Find all supplier invoices not in draft
    selection_invoices = con.searchRead('account.invoice', [[['journal_id','=', 2], ['state', '<>', 'draft']]]) #EXJ
    selection_invoices += con.searchRead('account.invoice', [[['journal_id','=', 4], ['state', '<>', 'draft']]]) #ECNJ
    #Verify that an attachment exists
    for move in selection_invoices:
        if move['id'] not in attachment_res_ids:
            if 'key1' in move:
                error(move['journal_id'][1] + ' ' + move['internal_number'] + ' dated ' + move['date'] + ' has no attachment!')
            else:
                error(move['journal_id'][1] + ' ' + move['internal_number'] + ' has no attachment!')

    #find all attachements in the account.move category
    attachment_account_move = con.searchRead('ir.attachment', [[['res_model','=','account.move'], ['db_datas','<>', None]]], {'fields': ['name', 'res_id', 'id']})
    attachment_res_ids = []
    for attachment in attachment_account_move:
        attachment_res_ids.append(attachment['res_id'])
    #Find all journals that needs attachement
    #selection_moves = con.searchRead('account.move', terms=[[['journal_id','=',5]]]) #DIV
    # Do not check for attachements in OPEJ-journals
    # selection_moves += con.searchRead('account.move', terms=[[['journal_id','=',6]]]) #OPEJ
    #selection_moves += con.searchRead('account.move', terms=[[['journal_id','=',7]]]) #BNK1
    # Check for attatchments only in draft state
    #selection_moves += con.searchRead('account.move', terms=[[['journal_id','=',8], ['state','=','draft']]]) #BNK2

    #Verify that an attachment exists
    #for move in selection_moves:
    #    if move['id'] not in attachment_res_ids:
    #        error(move['journal_id'][1] + ' ' + move['name'] + ' dated ' + move['date'] + ' has no attachment!')

if __name__ == '__main__':
    run()
