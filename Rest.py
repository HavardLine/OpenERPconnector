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

  def getPDF(self, ids=[0]):
    printsock = xmlrpclib.ServerProxy(self._uri + '/xmlrpc/report')
    model = 'account.invoice'
    id_report = printsock.report(self._db, self._uid, self._pwd, model, ids, {'model': model, 'id': ids[0], 'report_type':'pdf'})
    time.sleep(5)
    state = False
    attempt = 0
    while not state:
      report = printsock.report_get(self._db, self._uid, self._pwd, id_report)
      state = report['state']
      if not state:
        time.sleep(1)
        attempt += 1
      if attempt>30:
        print 'Printing aborted, too long delay !'

    string_pdf = base64.decodestring(report['result'])
    file_pdf = open('/tmp/file.pdf','w')
    file_pdf.write(string_pdf)
    file_pdf.close()
    return True

#Test-code for module
if __name__ == '__main__':
  con = Connection()
  print con.get('product.pricelist', [1])
  #print con.getPDF() 

