import yaml, os

class Group:
  def __init__(self):  
    with open(os.environ['HOME']+"/config/odoo.yml", "r") as f:
      params = yaml.load(f)
    f.close()
    self.value = params

#Test-code for module
if __name__ == '__main__':
  print Group().value

