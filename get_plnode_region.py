import urllib, json, os
import time
from ipinfo.ipinfo import *
from data_folder import *
import glob

GET_NODE_URL_PATH = 'http://manage.cmu-agens.com/nodeinfo/get_node'
MAP_TIMEZONE_API = 'https://maps.googleapis.com/maps/api/timezone/json?location='

def get_plnode_region(pl_hostname):
    ip = host2ip(pl_hostname)

    url = GET_NODE_URL_PATH + '?ip=' + ip
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    location = data['latitude'] + "," + data['longitude']
    map_url = MAP_TIMEZONE_API + location + "&timestamp=" + str(time.time()) + "&sensor=false"

    response = urllib.urlopen(map_url)
    map_data = json.loads(response.read())
    if map_data['status'] == 'OK':
        timeZoneName = map_data['timeZoneName']


    if data['country'] != {}:
        if (data['country'] in ['US', 'CA', 'United States', 'Canada']):
            return "North America"

        if (data['country'] == 'BR'):
            return "South America"

        if (data['country'] in ['PT', 'Czech Republic', 'SW', 'PL', 'CZ', 'FR', 'FI',
                                'BE', 'IT', 'AR', 'NO', 'DE', 'ES', 'SE', 'CH']):
            return "Europe"

        if (data['country'] in ['AU', 'NZ']):
            return "Australia"

        if (data['country'] in ['CN', 'JP', 'SG', 'Japan', 'RU']):
            return "Asia"

        if (data['country'] not in ['US', 'CA', 'United States', 'BR', 'PT', 'Czech Republic',
                                    'SW', 'PL', 'CZ', 'AU', 'NZ', 'CN', 'JP', 'SG', 'Japan',
                                    'FR', 'FI', 'BE', 'Canada', 'IT', 'AR', 'NO', 'DE', 'ES',
                                    'SE', 'RU']):
            print pl_hostname, ip, data['country']
            return "Unknown"

if __name__ == '__main__':
    pl_node_data_folder = geographical_data_folder + "amazon/dataQoE/"

    all_pl_node_data_files = glob.glob(pl_node_data_folder + "*.json")
    for pl_node_data_file in all_pl_node_data_files:
        pl_node_data_file_basename = os.path.basename(pl_node_data_file)
        pl_node_name = pl_node_data_file_basename.split("_")[0]
        region = get_plnode_region(pl_node_name)
        print("The region for the planetlab node %s is %s!"%(pl_node_name, region))




