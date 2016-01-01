from os.path import expanduser
import xmlrpclib
import csv
import time
import base64

class Connection:
  def __init__(self, user='admin', pwd='a', db='test', uri='http://localhost:8069'):
    sock_common = xmlrpclib.ServerProxy(uri + '/xmlrpc/common')
    self._uid = sock_common.login(db, user, pwd)
    self._uri = uri
    self._sock = xmlrpclib.ServerProxy(uri + '/xmlrpc/object')
    self._db = db
    self._pwd = pwd

  def search(self, obj):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'search', [[]])
    
  def searchDate(self, obj, myDate='2015-12%'):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'search', [[['date', 'like', myDate]]])

  def get(self, obj, ids):
    return self._sock.execute_kw(self._db, self._uid, self._pwd, obj, 'read', ids)

  def getPDF(self, ids):
    report = xmlrpclib.ServerProxy('{}/xmlrpc/2/report'.format(self._uri))
    result = report.render_report(self._db, self._uid, self._pwd, 'account.report_invoice', ids)
    report_data = result['result'].decode('base64')


    file_pdf = open(expanduser("~")+'/server/accounting/invoices_out/invoices.pdf','w')
    file_pdf.write(report_data)
    file_pdf.close()
    return True

#Test-code for module
if __name__ == '__main__':
  #saving all invoices
  con = Connection()
  ids = con.search('account.invoice')
  print con.getPDF(ids) 

