from drivers import odoo_connector
import tempfile, os
from pprint import pprint

con = odoo_connector.Connection()

#odoo_dataset = con.execute('account.invoice','search_read', [[('type','like','out_'), ('state','=','open')]], {'fields':['id','number']})
source = con.execute('account.move','search_read', [[('ref','=','Lønn 2017 07 Håvard.xlsx')]], {'fields':['id']})
#source[0]['id']=104

attachments = con.execute('ir.attachment','search_read', [[('res_model', '=', 'account.move'), ('res_id', '=', source[0]['id'])]], {'fields':['id', 'db_datas', 'res_model', 'datas_fname']})

# #Saving invoices to the archive
for attachment in attachments:
    import base64
    with open(attachment['datas_fname'], "wb") as fh:
        fh.write(base64.b64decode(attachment['db_datas']))

print(source[0]['id'])