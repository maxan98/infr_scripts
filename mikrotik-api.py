import routeros_api
import os
import argparse
connection = routeros_api.RouterOsApiPool('192.168.88.1', username='admin', password=os.environ['mikrotik-password'], use_ssl=False, ssl_verify=False, ssl_verify_hostname=False, ssl_context=None,)
api = connection.get_api()
nat_list =  api.get_resource('/ip/firewall/nat')
