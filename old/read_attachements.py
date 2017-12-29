
from drivers import odoo_connector
from drivers import smb
import pprint, tempfile, os

con = odoo_connector.Connection()
smb = d_smb.Connection()

odoo_dataset = con.execute('account.invoice','search_read', [[('type','like','out_'), ('state','=','open')]], {'fields':['id','number']})
odoo_dataset += con.execute('account.invoice','search_read', [[('type','like','out_'), ('state','=','paid')]], {'fields':['id','number']})

smb_archive =  smb.con.listPath('data', '/accounting/archive')


#Extracts the name we want from the invoice number. Example: SAJ/2016/0001 > SAJ0001
for data in odoo_dataset:
	data['name'] = data['number'].split('/')[0] + data['number'].split('/')[2]

#Finding PDF files that need to be archived
smb_names = []
for data in smb_archive:
	if len(data.filename) > 4:
		if data.filename[-4:] == '.pdf':
			smb_names.append(data.filename[:-4].encode('ascii', 'ignore'))
	

#print odoo_dataset
#print smb_names

#Find new invoices to the archive
new_odoo_elements = []
for odoo_element in odoo_dataset:
	if odoo_element['name'] in smb_names:
		print(odoo_element['name'] + '.pdf exists in archive')
	else:
		new_odoo_elements.append(odoo_element)

#Saving invoices to the archive
for odoo_element in new_odoo_elements:
	pdf_data = tempfile.TemporaryFile()
	pdf_data.write(con.returnPDF([odoo_element['id']]))
	pdf_data.seek(0)
	filename= odoo_element['name'] + '.pdf'
	print('Writing bytes to '+filename+':')
	print(smb.con.storeFile('data', '/accounting/archive/' + filename  , pdf_data, timeout=30))
	pdf_data.close()
