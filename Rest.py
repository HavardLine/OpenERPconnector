from os.path import expanduser
import xmlrpclib
import yaml
import time
import base64

with open("config.yml", "r") as f:
    params = yaml.load(f)
params = params['odoo']

class Connection:
  def __init__(self, user=params['user'], pwd=params['pwd'], db=params['db'], uri=params['uri']):
    sock_common = xmlrpclib.ServerProxy(uri + '/xmlrpc/common')
    self._uid = sock_common.login(db, user, pwd)
    self._uri = uri
    self._sock = xmlrpclib.ServerProxy(uri + '/xmlrpc/object')
    self._db = db
    self._pwd = pwd

  def search(self, obj, terms=[], opts = {}):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'search_read', [[terms]], opts)
	
  def searchRead(self, obj, terms=[], opts = {}):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'search_read', [[terms]], opts)
  
  #def set(self, obj, ids, opts):
  #  return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'write', [ids, opts])

  def searchProductTemplate(self, default_code):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.template', 'search', [[['default_code', 'like', default_code]]])
    
  def searchProduct(self, default_code):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.product', 'search', [[['active', '=', True], ['default_code', '=', default_code]]])
    
  def searchDate(self, obj, myDate='2015-12%'):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'search', [[['date', 'like', myDate]]])

  def get(self, obj, ids):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'read', ids)

  def getProduct(self, product_name):
    #return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.product', 'search_read', [[]], {})
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.product', 'read', [11471])
	
  def getProductTemplate(self, product_name):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.template', 'read', [8072])
	
  def getPDF(self, myDate):
    report = xmlrpclib.ServerProxy('{}/xmlrpc/2/report'.format(self._uri))
    ids = self._sock.execute_kw(self._db, self._uid, self._pwd,
      'account.invoice', 'search',
      [[('date_invoice', 'like', myDate)]])
    result = report.render_report(self._db, self._uid, self._pwd,
      'account.report_invoice', ids)
    report_data = result['result'].decode('base64')
    
    file_pdf = open(expanduser("~")+'/invoices_out/'+str(myDate)+' invoices.pdf','w')
    file_pdf.write(report_data)
    file_pdf.close()
    
    if len(ids)>0:
      logMsg = 'PDF ids '+str(ids)+' found'
      print logMsg
      return True
    else:
      print ids
      logMsg = 'No invoices found using parameter: '+ myDate
      print logMsg
      return False
	
  def setProduct(self, product):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.product', 'create', [product])
	
  def setProductTemplate(self, product_template):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.template', 'create', [product_template])
	
  def deleteProduct(self, ids):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.product', 'unlink', [ids])
	
  def deleteProductTemplate(self, ids):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, 'product.template', 'unlink', [ids])

#Test-code for module
if __name__ == '__main__':
  import sys, getopt
  myDate = ''
 
  opts, args = getopt.getopt(sys.argv[1:],"d:")
  if len(opts)!=1:
    print 'default options: -d <date>'
  else:
    #saving all invoices
    myDate = opts[0][1]
 
  con = Connection()
  print con.getPDF(myDate) 

