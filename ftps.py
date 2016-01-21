import yaml

with open("config.yml", "r") as f:
    params = yaml.load(f)
params = params['ftps_server']

def send(file):
  return True
