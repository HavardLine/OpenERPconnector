import Rest

con = Rest.Connection()

#Asking for id number 1 in the products.products object.
#print con.get('product.product', [1])
print con.search('product.product')
#print con.search('project.project')
#print con.get('project.project', [1])
#print con.get('project.task', [1])[0]
#print con.get('project.task.work', [1])