import commands, yaml

with open("config.yml", "r") as f:
    params = yaml.load(f)
f.close()
ftpsParams = params['ftps_webserver']

def upload_catalog(file_name = 'catalog.pdf'):
  """Uploading catalog to ftp server using TLS.
  All valid system certificates will be accepted.
  """
  cmd = 'curl --ssl-reqd --ftp-create-dirs -T '+file_name+\
        ' -u '+ftpsParams['user']+\
        ':'+ftpsParams['pwd']+\
        ' ftp://'+ftpsParams['url']+'/'+file_name
  return commands.getstatusoutput(cmd)[0]
