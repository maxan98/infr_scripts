import routeros_api
import os
import argparse
connection = routeros_api.RouterOsApiPool('192.168.88.1', username='admin', password=os.environ['MPWD'], use_ssl=False, ssl_verify=False, ssl_verify_hostname=False, ssl_context=None,)
api = connection.get_api()
nat_list =  api.get_resource('/ip/firewall/nat')
print(nat_list.get(id='*5'))
nat_list.set(chain='dstnat', action='netmap',to_addresses='192.168.88.11',to_ports='8888',protocol='tcp',in_interface='ether1',dst_port='8888')
connection.disconnect()
