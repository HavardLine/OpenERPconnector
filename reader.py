import Rest

con = Rest.Connection(db='test', uri='http://localhost:8069')
#obj = 'res.partner'
#obj = 'product.product'
#obj = 'project.task'
#obj = 'project.task.work'
obj = 'account.invoice'

#Asking for id number 1 in the products.products object.
ids = con.search(obj)
print ids
element = con.get(obj, [1])

#listing keys in element
keys= element.keys()
for key in keys:
  print key

#listing keys and values in element
#for item in element:
#  print item, " = ", element[item]
