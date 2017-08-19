from json_utils import *
import pandas as pd
from data_folder import *
import glob
import os
from get_plnode_region import *

def load_session_qoe(qoe_file):
    qoes = loadJson(qoe_file)
    qoes_list = []
    for chunk_id in qoes:
        qoes_list.append(qoes[chunk_id])

    df = pd.DataFrame(qoes_list)

    session_qoe = df["QoE2"].mean()

    return session_qoe

def load_all_session_qoes(qoe_file_folder):
    all_qoe_files = glob.glob(qoe_file_folder + "*")
    all_session_qoes = []
    for qoe_file in all_qoe_files:
        cur_qoe = load_session_qoe(qoe_file)
        all_session_qoes.append(cur_qoe)

    return all_session_qoes

def load_all_session_qoes_per_region(qoe_file_folder):
    regional_qoes = {}

    all_qoe_files = glob.glob(qoe_file_folder + "*")
    for qoe_file in all_qoe_files:
        cur_qoe_file_basename = os.path.basename(qoe_file)
        cur_node_name = cur_qoe_file_basename.split("_")[0]
        cur_qoe = load_session_qoe(qoe_file)
        cur_node_region = get_plnode_region(cur_node_name)
        if cur_node_region not in regional_qoes.keys():
            regional_qoes[cur_node_region] = []
        regional_qoes[cur_node_region].append(cur_qoe)

    return regional_qoes


if __name__ == '__main__':
    pl_node_data_folder = geographical_data_folder + "azure/dataQoE/"

    all_pl_node_data_files = glob.glob(pl_node_data_folder + "*.json")
    for pl_node_data_file in all_pl_node_data_files:
        pl_node_data_file_basename = os.path.basename(pl_node_data_file)
        pl_node_name = pl_node_data_file_basename.split("_")[0]
        session_qoe = load_session_qoe(pl_node_data_file)
        print("The session QoE for the planetlab QoE file %s is %.4f!"%(pl_node_data_file_basename, session_qoe))
