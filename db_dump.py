import base64, erppeek, config

def main():
    """Exports backup of ODOO database and files
    Parameters used:
    odoo.uri
    odoo_backup.pwd
    odoo_backup.dbs
    odoo_backup.folder
    
    """
    conf = config.Group('odoo').value
    odoo = erppeek.Client(conf['uri'])
    b64data = odoo.db.dump(conf['pwd'], conf['db'])
    data = base64.b64decode(b64data)
    f = open('outfile.dump', 'w')
    f.write(data)
    f.close
    return True

print main()
