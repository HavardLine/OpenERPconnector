# -*- coding: utf-8 -*-
"""Module for daily verification

Example:
    none   

Attributes:
    none
"""
from drivers import odoo_connector
from logging import error, warning, info
from pprint import pprint
from os import listdir, path
import pandas

#find file
src =path.join('L:\\','accounting', 'lønn')
files = listdir(src)


# using one file for now

for file_name in files:
    #Reading relevant lines from excel-file
    df = pandas.read_excel(open(path.join(src, file_name),'rb'), sheetname='Lønn', header=9, skip_footer=2, index_col=None).fillna(0.0).round(2)
    
    #Establish ODOO connection
    con = odoo_connector.Connection()

    #moves = con.searchRead('account.invoice', [[['number', 'like', 'SAJ/2017/'], ['state', '=','open']]])
    moves = con.searchRead('account.move', terms=[[['journal_id','=',5], ['ref','=',file_name]]]) #DIV

    if len(moves) == 1:
        info('Evaluating file "'+file_name+'"')
        #Reading relevant lines from odoo
        move_lines = con.execute('account.move.line', 'read', [moves[0]['line_id']])

        # Compares the number of items
        if df.shape[0] != len(move_lines):
            error('File "'+ file_name+'" has '+ str(df.shape[0])+ ' elements, journal has '+str(len(move_lines))+ ' elements')
            exit(1)

        # Looping journal lines
        for line_index, line_value in enumerate(move_lines):
            # Compares account number
            row = 0
            key='account_id'
            if(str(df.iloc[line_index,row]) != line_value[key][1][:6]):
                error('File "' + file_name + '" line index ' + str(line_index) + ', coulumn key: ' + key + ', ' + str(df.iloc[line_index,row]) + ' != ' + line_value[key][1][:6])
                exit(1)

            # Compares debit value
            row = 1
            key='debit'
            if df.iloc[line_index,row] != line_value[key]:
                warning('File "' + file_name + '" line index '+str(line_index) + ', coulumn key: ' + key + ', ' + str(df.iloc[line_index,row]) +' != '+ str(line_value[key]))    
                if con.execute('account.move.line', 'write', [[line_value['id']], {key: str(df.iloc[line_index,row])}]):
                    warning('File "' + file_name+ '", changed value at account.move.line, id:' + str(line_value['id']) + ', column key: ' + str(key))

             # Compares credit value
            row = 2
            key='credit'
            if df.iloc[line_index,row] != line_value[key]:
                warning('File "' + file_name + '" line index: '+str(line_index) + ', coulumn key: ' + key + ', ' + str(df.iloc[line_index,row]) +' != '+ str(line_value[key]))
                if con.execute('account.move.line', 'write', [[line_value['id']], {key: str(df.iloc[line_index,row])}]):
                    warning('File "' + file_name+ '", changed value at account.move.line, id:' + str(line_value['id']) + ', column key: ' + str(key))

    elif len(moves) > 1:
        error('Multiple records exist for "'+file_name+'". Delete records and try new import.')
        exit(1)
    else:
        error('No record exist for "'+file_name+'". Create record and try new import.')
