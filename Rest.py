import xmlrpclib
import csv

class Connection:
    def __init__(self, user='admin', pwd='a', db='test', uri='http://localhost:8069'):
        sock_common = xmlrpclib.ServerProxy(uri + '/xmlrpc/common')
        self._uid = sock_common.login(db, user, pwd)
        self._sock = xmlrpclib.ServerProxy(uri + '/xmlrpc/object')
        self._db = db
        self._pwd = pwd

    def get(self, obj, ids):
        return self._sock.execute(self._db, self._uid, self._pwd, obj, 'read', ids)


#Test-code for mudule
if __name__ == '__main__':
    con = Connection()
    print con.get('product.pricelist', [1])

