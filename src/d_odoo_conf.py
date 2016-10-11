import os, json

class Group:
	def __init__(self):  
		with open(os.environ['HOME']+"/config/odoo.json", "r") as f: 
			params = f.read()
		f.close()
		self.value = json.loads(params)

#Test-code for module
if __name__ == '__main__':
  print Group().value

