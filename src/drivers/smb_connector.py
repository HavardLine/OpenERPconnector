from smb.SMBConnection import SMBConnection
import os, json

class Connection:
	def __init__(self):
		#self.con is a object of the type SMBConnection

		if os.name == 'nt':
			config_path = os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"/config/smb.json"
		else:
			config_path = os.environ['HOMEPATH']+"/config/smb.json"

		with open(config_path, "r") as f: 
			file_buffer = f.read()
		f.close()

		params = json.loads(file_buffer)
		self.con = SMBConnection(params['user'], params['pwd'], params['client'], params['host'], use_ntlm_v2 = True)
		self.con.connect(params['host_ip'], 139)

if __name__ == '__main__':
	nfs = Connection()
	
	filelist = nfs.con.listPath('data', '/accounting') 
	for instance in filelist:
		print('')
		print(instance.filename)
		print(instance.last_attr_change_time)
		print(instance.last_write_time)
