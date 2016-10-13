import d_smb_conf
from smb.SMBConnection import SMBConnection


class Connection:
	def __init__(self):
		#self.con is a object of the type SMBConnection
		params = d_smb_conf.Group().value
		self.con = SMBConnection(params['user'], params['pwd'], params['client'], params['host'], use_ntlm_v2 = True)
		self.con.connect(params['host_ip'], 139)

if __name__ == '__main__':
	nfs = Connection()
	
	filelist = nfs.con.listPath('data', '/accounting') 
	for instance in filelist:
		print ''
		print instance.filename
		print instance.last_attr_change_time
		print instance.last_write_time
