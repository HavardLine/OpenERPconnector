import odoo

con = odoo.Connection()
#obj = 'res.partner'
#obj = 'project.task'
obj = 'product.product'
#obj = 'product.template'
#obj = 'product.variant'
#obj = 'project.task.work'
#obj = 'account.invoice'

#Asking for id number 1 in the products.products object.
ids = con.search(obj)
print ids
element = con.get(obj, [10191])

print "\nListing keys in element:"
keys= element.keys()
#for key in keys:
#  print key

#listing keys and values in element
for item in element:
  print item, " = ", element[item]
