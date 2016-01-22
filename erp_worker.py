import ftps, product

manager = product.Manager()
dataset = manager.readActive()
print dataset
#print manager.createCatalog(dataset)

#¤print ftps.upload_catalog()


