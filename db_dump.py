import base64, erppeek, config

def main():
    """Exports backup of ODOO database and files
    Parameters used:
    odoo.uri
    odoo_backup.pwd
    odoo_backup.dbs
    odoo_backup.folder
    
    """
    uri = config.Group('odoo').value['uri']
    params = config.Group('odoo_backup').value

    odoo = erppeek.Client(uri)
    
    for db in params['dbs']:
      b64data = odoo.db.dump(params['pwd'], db)
      data = base64.b64decode(b64data)
      f = open('../'+db+'.zip', 'w')
      f.write(data)
      f.close
      print 'DB '+db+' exported'
    return True

print main()
