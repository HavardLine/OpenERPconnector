import os, json

class Group:
	def __init__(self):  
		with open(os.environ['HOME']+"/config/smb.json", "r") as f: 
			params = f.read()
		f.close()
		self.value = json.loads(params, object_hook=self.ascii_encode_dict)

	def ascii_encode_dict(self, data):
	#Code for encoding ascii
	#http://stackoverflow.com/questions/9590382/forcing-python-json-module-to-work-with-ascii
		ascii_encode = lambda x: x.encode('ascii')
		return dict(map(ascii_encode, pair) for pair in data.items())

#Test-code for module
if __name__ == '__main__':
  print Group().value

