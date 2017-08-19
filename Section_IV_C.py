from data_folder import *
import glob
import os
from utc2locale import *
from load_session_qoe import *
import numpy as np
import matplotlib.pyplot as plt
import pprint

styles = ['k-', 'b.-', 'r--', 'm:', 'ys-', 'go-', 'c^-',
          'k.-', 'b--', 'r:', 'ms-','yo-', 'g^-', 'c-',
          'k--', 'b:', 'rs-', 'mo-', 'y^-', 'g-', 'c.-',
          'k:', 'bs-', 'ro-', 'm^-', 'y-', 'g.-', 'c--',
          'ks-', 'bo-', 'r^-', 'm-', 'y.-', 'g--', 'c-',
          'ko-', 'b^-', 'r-', 'm.-', 'y--', 'g-', 'cs-']

colors = ['red', 'green', 'blue', 'black']
markers = ['o', 's', '*', '<', '>']

def comare_clouds_qoes_daily(user):
    ## Google QoE from user in 24 hours
    google_qoe_folder = stability_data_folder + "google/dataQoE/"
    google_daily_qoes = load_session_qoes_daily(google_qoe_folder, user)
    sorted_google_ts = sorted(google_daily_qoes.keys())
    google_qoes = [google_daily_qoes[ts] for ts in sorted_google_ts]

    ## Azure QoE from user in 24 hours
    azure_qoe_folder = stability_data_folder + "azure/dataQoE/"
    azure_daily_qoes = load_session_qoes_daily(azure_qoe_folder, user)
    sorted_azure_ts = sorted(azure_daily_qoes.keys())
    azure_qoes = [azure_daily_qoes[ts] for ts in sorted_azure_ts]

    amazon_qoe_folder = stability_data_folder + "amazon/dataQoE/"
    amazon_daily_qoes = load_session_qoes_daily(amazon_qoe_folder, user)
    sorted_amazon_ts = sorted(amazon_daily_qoes.keys())
    amazon_qoes = [amazon_daily_qoes[ts] for ts in sorted_amazon_ts]

    fig, ax = plt.subplots()
    plt.plot(sorted_google_ts, google_qoes, styles[0], label="Google Cloud CDN", linewidth=2.0)
    plt.plot(sorted_azure_ts, azure_qoes, styles[1], label="Azure CDN", linewidth=2.0)
    plt.plot(sorted_amazon_ts, amazon_qoes, styles[2], label="Amazon CloudFront", linewidth=2.0)

    num_intvs = 25
    ts_labels = [x * 60 for x in range(num_intvs)]
    str_ts = [str(x) for x in range(num_intvs)]
    plt.xticks(ts_labels, str_ts, fontsize=10)

    ax.legend(loc=4)
    ax.set_xlabel("Hours (Local time)", fontsize=16)
    ax.set_ylabel("Session QoE", fontsize=16)
    ax.set_xlim([0,24*60])

    imgName = img_folder + user + "_cmpcloudcdns_dailyqoes"
    plt.savefig(imgName + ".jpg")
    plt.savefig(imgName + ".pdf")
    plt.savefig(imgName + ".png")
    plt.show()


def comare_clouds_latencies_daily(user):
    ## Google QoE from user in 24 hours
    google_ping_folder = stability_data_folder + "google/pingData/"
    google_daily_rtts = load_ping_daily(google_ping_folder, user)
    sorted_google_ts = sorted(google_daily_rtts.keys())
    google_lats = [google_daily_rtts[ts] for ts in sorted_google_ts]

    ## Azure QoE from user in 24 hours
    azure_ping_folder = stability_data_folder + "azure/pingData/"
    azure_daily_lats = load_ping_daily(azure_ping_folder, user)
    sorted_azure_ts = sorted(azure_daily_lats.keys())
    azure_lats = [azure_daily_lats[ts] for ts in sorted_azure_ts]

    amazon_qoe_folder = stability_data_folder + "amazon/pingData/"
    amazon_daily_lats = load_ping_daily(amazon_qoe_folder, user)
    sorted_amazon_ts = sorted(amazon_daily_lats.keys())
    amazon_lats = [amazon_daily_lats[ts] for ts in sorted_amazon_ts]

    fig, ax = plt.subplots()
    plt.plot(sorted_google_ts, google_lats, styles[0], label="Google Cloud CDN", linewidth=2.0)
    plt.plot(sorted_azure_ts, azure_lats, styles[1], label="Azure CDN", linewidth=2.0)
    plt.plot(sorted_amazon_ts, amazon_lats, styles[2], label="Amazon CloudFront", linewidth=2.0)

    num_intvs = 25
    ts_labels = [x * 60 for x in range(num_intvs)]
    str_ts = [str(x) for x in range(num_intvs)]
    plt.xticks(ts_labels, str_ts, fontsize=10)

    ax.legend(loc=0)
    ax.set_xlabel("Hours (Local time)", fontsize=16)
    ax.set_ylabel("Probed latencies (ms)", fontsize=16)
    ax.set_xlim([0,24*60])

    imgName = img_folder + user + "_cmpcloudcdns_dailyrtts"
    plt.savefig(imgName + ".jpg")
    plt.savefig(imgName + ".pdf")
    plt.savefig(imgName + ".png")
    plt.show()

def cmp_cloudcdns_qoe_stability_per_tz(provider, tz, styleID=0):
    hours = range(24)

    fig, ax = plt.subplots()

    ## load google qoe mean and std per hour for specified time zone
    qoe_folder = stability_data_folder + provider + "/dataQoE/"
    qoes_per_tz_hour = load_session_qoes_per_tz_hour(qoe_folder)
    qoes_per_hour = qoes_per_tz_hour[tz]
    qoe_hourly_mn = [np.mean(qoes_per_hour[h]) for h in hours]
    qoe_hourly_std = [np.std(qoes_per_hour[h]) for h in hours]
    plt.errorbar(hours, qoe_hourly_mn, qoe_hourly_std, marker=markers[styleID], mfc=colors[styleID], label=provider)

    ax.legend(loc=0)
    plt.title(tz)
    ax.set_xlabel("Hours (Local time)", fontsize=16)
    ax.set_ylabel("Mean and STD of Session QoEs (0-5)", fontsize=16)
    ax.set_xlim([0,24])
    ax.set_ylim([0,7])

    tz_str = tz.replace("/", "_")
    imgName = img_folder + provider + "_" + tz_str + "_cmpcloudcdns_hourly_qoe_errorbars"
    plt.savefig(imgName + ".jpg")
    plt.savefig(imgName + ".pdf")
    plt.savefig(imgName + ".png")
    plt.show()



def load_session_qoes_daily(qoe_folder, user):
    all_user_files = glob.glob(qoe_folder + user + "*")
    daily_qoes = {}
    for cur_user_file in all_user_files:
        cur_user_basefile = os.path.basename(cur_user_file)
        cur_user_basefile_strlist = cur_user_basefile.split("_")
        cur_username = cur_user_basefile_strlist[0]
        cur_timestr = cur_user_basefile_strlist[1]
        cur_mins = utc2locale_mins(cur_username, cur_timestr)
        cur_qoe = load_session_qoe(cur_user_file)
        daily_qoes[cur_mins] = cur_qoe
    return daily_qoes

def load_session_qoes_per_tz_hour(qoe_folder):
    all_session_qoe_files = glob.glob(qoe_folder + "*")
    qoes_per_tz_hour = {}
    for qoe_file in all_session_qoe_files:
        qoe_basefile = os.path.basename(qoe_file)
        qoe_basefile_strs = qoe_basefile.split("_")
        cur_node_name = qoe_basefile_strs[0]
        cur_ts_str = qoe_basefile_strs[1]
        cur_tz, cur_local_hour = get_local_hour(cur_node_name, cur_ts_str)

        if cur_tz not in qoes_per_tz_hour.keys():
            qoes_per_tz_hour[cur_tz] = {}

        if cur_local_hour not in qoes_per_tz_hour[cur_tz].keys():
            qoes_per_tz_hour[cur_tz][cur_local_hour] = []

        cur_qoe = load_session_qoe(qoe_file)
        qoes_per_tz_hour[cur_tz][cur_local_hour].append(cur_qoe)
    return qoes_per_tz_hour


def load_ping_daily(ping_folder, user):
    all_user_files = glob.glob(ping_folder + user + "*")
    daily_pings = {}
    for cur_user_file in all_user_files:
        cur_user_basefile = os.path.basename(cur_user_file)
        cur_user_basefile_strlist = cur_user_basefile.split("_")
        cur_username = cur_user_basefile_strlist[0].split("-")[0]
        cur_timestr = cur_user_basefile_strlist[1]
        cur_mins = utc2locale_mins(cur_username, cur_timestr)
        cur_pings = loadJson(cur_user_file)
        mn_rtt = np.mean(cur_pings["rttList"])
        daily_pings[cur_mins] = mn_rtt
    return daily_pings


if __name__ == '__main__':
    '''
    ## Section IV B, figure 9 to 12
    user = "earth.cs.brown.edu"
    # user = "pl1.rcc.uottawa.ca"
    # user = "planetlab01.cs.washington.edu"
    # user = "planetlab2.koganei.itrc.net"
    user_timezone = get_host_timezone(user)
    print("Compare Cloud CDN for user in %s."%user_timezone["timezoneId"])
    comare_clouds_qoes_daily(user)
    comare_clouds_latencies_daily(user)
    '''


    ## Draw QoE hourly error bars
    tz_to_draw = ['America/New_York', 'America/Los_Angeles', 'America/Denver', 'Europe/Prague']
    providers = ['google', 'amazon', 'azure']
    for tz in tz_to_draw:
        pid = 0
        for provider in providers:
            cmp_cloudcdns_qoe_stability_per_tz(provider, tz, pid)
            pid += 1

    ## Count mean and STD for all session QoEs in different time zones in 24 hours
    providers = ['google', 'amazon', 'azure']
    for provider in providers:
        qoe_folder = stability_data_folder + provider + "/dataQoE/"
        qoes_per_tz_hour = load_session_qoes_per_tz_hour(qoe_folder)








