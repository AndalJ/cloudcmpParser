import pytz
import urllib, json, os
import time
from ipinfo.ipinfo import *
from data_folder import *
import glob
from json_utils import *

def get_host_timezone(node_name):
    geodata_file = geodata_folder + "nodes_tz.json"
    node_tz = loadJson(geodata_file)

    if node_name in node_tz.keys():
        return node_tz[node_name]
    else:
        GET_NODE_URL_PATH = 'http://manage.cmu-agens.com/nodeinfo/get_node'

        ip = host2ip(node_name)

        url = GET_NODE_URL_PATH + '?ip=' + ip
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        geoname_url = "http://api.geonames.org/timezoneJSON?formatted=true&lat=%.4f&lng=%.4f&username=wangchen615" % (float(data['latitude']), float(data['longitude']))

        r = requests.get(geoname_url)  ## Make a request
        rsp = r.json()
        node_tz[node_name] = rsp
        dumpJson(node_tz, geodata_file)
        return node_tz[node_name] ## return the timezone

def utc2locale_mins(node_name, datetime_str):
    cur_timediff = get_host_timezone(node_name)["rawOffset"]
    cur_utc_hour = int(datetime_str[4:6])

    ## Get the local hour of the
    cur_locale_hour = cur_utc_hour + cur_timediff
    if cur_locale_hour < 0:
        cur_locale_hour += 24

    if cur_locale_hour >= 24:
        cur_locale_hour -= 24

    cur_local_min = int(datetime_str[6:8])

    cur_total_mins = cur_locale_hour * 60 + cur_local_min
    return cur_total_mins

def get_local_hour(node_name, datetime_str):
    cur_tz_dict = get_host_timezone(node_name)
    cur_tz = cur_tz_dict["timezoneId"]
    cur_timediff = cur_tz_dict["rawOffset"]
    cur_utc_hour = int(datetime_str[4:6])

    ## Get the local hour of the
    cur_locale_hour = cur_utc_hour + cur_timediff
    if cur_locale_hour < 0:
        cur_locale_hour += 24

    if cur_locale_hour >= 24:
        cur_locale_hour -= 24

    return cur_tz,cur_locale_hour


if __name__ == '__main__':
    # client_to_study = "earth.cs.brown.edu"

    pl_node_data_folder = geographical_data_folder + "azure/dataQoE/"
    geodata_file = geodata_folder + "nodes_tz.json"

    node_tz = loadJson(geodata_file)
    all_pl_node_data_files = glob.glob(pl_node_data_folder + "*.json")
    for pl_node_data_file in all_pl_node_data_files:
        pl_node_data_file_basename = os.path.basename(pl_node_data_file)
        pl_node_name = pl_node_data_file_basename.split("_")[0]
        if pl_node_name not in node_tz.keys():
            print("Requesting GEONAMES URL")
            time_zone_dict = get_host_timezone(pl_node_name)
            node_tz[pl_node_name] = time_zone_dict
        else:
            print("Already cached!")
            time_zone_dict = node_tz[pl_node_name]
        print("The time diff to the UTC for the planetlab node %s is %d!" % (pl_node_name, time_zone_dict["rawOffset"]))

    dumpJson(node_tz, geodata_file)