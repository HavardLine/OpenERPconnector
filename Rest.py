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

  def getPDF(self, myDate):
    report = xmlrpclib.ServerProxy('{}/xmlrpc/2/report'.format(self._uri))
    ids = self._sock.execute_kw(self._db, self._uid, self._pwd,
      'account.invoice', 'search',
      [[['date_invoice', 'like', myDate], ['state', '!=', 'draft']]])
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

