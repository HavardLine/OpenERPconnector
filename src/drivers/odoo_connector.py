import xmlrpc.client
import os, json


class Connection:
  def __init__(self):
    if os.name == 'nt':
      config_path = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"/config/odoo.json"
    else:
      config_path = os.environ['HOMEPATH']+"/config/odoo.json"

    with open(config_path, "r") as f:
      file_buffer = f.read()
      f.close()

    self.params = json.loads(file_buffer)

    sock_common = xmlrpc.client.ServerProxy(self.params['uri'] + '/xmlrpc/common')
    self._uid = sock_common.login(self.params['db'], self.params['user'], self.params['pwd'])
    self._sock = xmlrpc.client.ServerProxy(self.params['uri'] + '/xmlrpc/object', allow_none=True, use_builtin_types=True )

  def execute(self, obj, keyword, terms, options={}):
    return self._sock.execute_kw(self.params['db'], self._uid, self.params['pwd'], obj, keyword, terms, options)

  def search(self, obj, terms=[[]], opts = {}):
    return self._sock.execute_kw(self.params['db'], self._uid, self.params['pwd'], obj, 'search', terms, opts)
	
  def searchRead(self, obj, terms=[], opts = {}):
    return self._sock.execute_kw(self.params['db'], self._uid, self.params['pwd'], obj, 'search_read', terms, opts)

  def read(self, obj, ids):
    return self._sock.execute_kw(self.params['db'], self._uid, self.params['pwd'], obj, 'read', [ids])

  def returnPDF(self, ids=[]):
    sock_report = xmlrpc.client.ServerProxy('{}/xmlrpc/2/report'.format(self.params['uri']))
    result = sock_report.render_report(self.params['db'], self._uid, self.params['pwd'], 'account.report_invoice', ids)
    return result['result'].decode('base64')
    
  def setProduct(self, product):
    return self._sock.execute_kw(self.params['db'], self._uid, self.params['pwd'], 'product.product', 'create', product)
	
  def setProductTemplate(self, product_template):
    return self._sock.execute_kw(self.params['db'], self._uid, self.params['pwd'], 'product.template', 'create', product_template)
	
#Test-code for module
if __name__ == '__main__':
  con = Connection()

