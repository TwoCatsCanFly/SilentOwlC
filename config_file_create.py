from configparser import ConfigParser

config = ConfigParser()

config['settings'] = {
    'debug':'true',
    's_key':'abc123',
    'log_path':'/something'
    }
config['files'] = {
    'use_cdn':'false',
    'port':'8889'
    }

with open('./dev.ini','w') as f:
    config.write(f)