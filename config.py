import yaml, os

class Group:
  def __init__(self, group):  
    with open(os.environ['HOME']+"/server/config.yml", "r") as f:
      params = yaml.load(f)
    f.close()
    self.value = params[group]

#Test-code for module
if __name__ == '__main__':
  print Group('odoo').value

