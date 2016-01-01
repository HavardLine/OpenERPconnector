import Rest

con = Rest.Connection(db='LTS', uri='http://172.16.1.146:8070')
#obj = 'res.partner'
#obj = 'product.product'
#obj = 'project.task'
#obj = 'project.task.work'
obj = 'account.invoice'

#Asking for id number 1 in the products.products object.
ids = con.search(obj)
print ids
alpha = con.get(obj, [5])
beta = con.get(obj, [7])

#listing keys in element
keys= alpha.keys()
for key in keys:
  if alpha[key]!=beta[key]:
    print key, alpha[key], beta[key]
    print ""
