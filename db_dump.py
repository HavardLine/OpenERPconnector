import base64, erppeek, config

def main():
#    """Main program."""
    conf = config.Group('odoo').value
    odoo = erppeek.Client(conf['uri'])
    b64data = odoo.db.dump(conf['pwd'], conf['db'])
    data = base64.b64decode(b64data)
    f = open('outfile.dump', 'w')
    f.write(data)
    f.close
    return True

#print 'OK'
print main()
