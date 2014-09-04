import Rest

con = Rest.Connection()

#Asking for id number 1 in the products.products object.
print con.get('product.product', [1])
