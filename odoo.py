import xmlrpclib
import base64
import config

params = config.Group('odoo').value

class Connection:
  def __init__(self, params=params):
    sock_common = xmlrpclib.ServerProxy(params['uri'] + '/xmlrpc/common')
    self._uid = sock_common.login(params['db'], params['user'], params['pwd'])
    self._sock = xmlrpclib.ServerProxy(params['uri'] + '/xmlrpc/object')

  def search(self, obj, terms=[], opts = {}):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], obj, 'search', [terms], opts)
	
  def searchRead(self, obj, terms=[], opts = {}):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], obj, 'search_read', [terms], opts)
  
  #def set(self, obj, ids, opts):
  #  return self._sock.execute_kw(params['db'], params['user'], params['pwd'], obj, 'write', [ids, opts])

  def searchProductTemplate(self, default_code):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], 'product.template', 'search', [[['default_code', 'like', default_code]]])
    
  def searchProduct(self, default_code):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], 'product.product', 'search', [[['active', '=', True], ['default_code', '=', default_code]]])
    
  def searchDate(self, obj, myDate='2015-12%'):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], obj, 'search', [[['date', 'like', myDate]]])

  def get(self, obj, ids):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], obj, 'read', ids)

  def getProduct(self, product_name):
    #return self._sock.execute_kw(params['db'], params['user'], params['pwd'], 'product.product', 'search_read', [[]], {})
    return self._sock.execute_kw(params['db'], self._uid , params['pwd'], 'product.product', 'read', [11471])
	
  def getProductTemplate(self, product_name):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], 'product.template', 'read', [8072])
	
  def getPDF(self, myDate):
    report = xmlrpclib.ServerProxy('{}/xmlrpc/2/report'.format(self._uri))
    ids = self._sock.execute_kw(params['db'], self._uid, params['pwd'],
      'account.invoice', 'search',
      [[('date_invoice', 'like', myDate)]])
    result = report.render_report(params['db'], self._uid, params['pwd'],
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
    return self._sock.execute_kw(params['db'], params['user'], params['pwd'], 'product.product', 'create', [product])
	
  def setProductTemplate(self, product_template):
    return self._sock.execute_kw(params['db'], params['user'], params['pwd'], 'product.template', 'create', [product_template])
	
  def deleteProduct(self, ids):
    return self._sock.execute_kw(params['db'], params['user'], params['pwd'], 'product.product', 'unlink', [ids])
	
  def deleteProductTemplate(self, ids):
    return self._sock.execute_kw(params['db'], params['user'], params['pwd'], 'product.template', 'unlink', [ids])

#Test-code for module
if __name__ == '__main__':
  con = Connection()
  #print con.getPDF(myDate) 

