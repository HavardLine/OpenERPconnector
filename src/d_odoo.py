import xmlrpclib
import base64
import d_odoo_conf
from os.path import expanduser

params = d_odoo_conf.Group().value

class Connection:
  def __init__(self, params=params):
    sock_common = xmlrpclib.ServerProxy(params['uri'] + '/xmlrpc/common')
    self._uid = sock_common.login(params['db'], params['user'], params['pwd'])
    self._sock = xmlrpclib.ServerProxy(params['uri'] + '/xmlrpc/object')

  def execute(self, odoo_object, keyword, terms, options={}):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], odoo_object, keyword, terms, options)

  def search(self, obj, terms=[[]], opts = {}):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], obj, 'search', terms, opts)
	
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

  def returnPDF(self, ids=[]):
    report = xmlrpclib.ServerProxy('{}/xmlrpc/2/report'.format(params['uri']))
    result = report.render_report(params['db'], self._uid, params['pwd'], 'account.report_invoice', ids)
    return result['result'].decode('base64')
    
  def setProduct(self, product):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], 'product.product', 'create', product)
	
  def setProductTemplate(self, product_template):
    return self._sock.execute_kw(params['db'], self._uid, params['pwd'], 'product.template', 'create', product_template)
	
  def deleteProduct(self, default_code):
    p_ids = self.searchProduct(default_code)
    t_ids = self.searchProductTemplate(default_code)
    return p_ids, t_ids

#Test-code for module
if __name__ == '__main__':
  con = Connection()
  #print con.getPDF(myDate) 

