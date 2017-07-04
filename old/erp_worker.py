import odoo

#Export databases in odoo


#Export monthly invoices
con = odoo.Connection()
print con.getPDF('2015')



#manager = product.Manager()
#dataset = manager.readActive()
#print dataset
#print manager.createCatalog(dataset)

#print ftps.upload_catalog()
