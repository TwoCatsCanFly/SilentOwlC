from configparser import ConfigParser

parser = ConfigParser()

parser.read('dev.ini')

print(parser.sections())
print(parser.get('settings','secret_key'))
print(parser.options('settings'))
print(parser.getint('files','port'))
print(parser.getint('files','non-existent-param',fallback='if-param-dont-exist-this-insted'))
print(parser.getboolean('files','use_cdn'))