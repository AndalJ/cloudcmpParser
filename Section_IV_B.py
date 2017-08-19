from data_folder import *
from drawlibs.draw_cdf import *
from get_plnode_region import *
from load_session_qoe import *
import numpy as np

patterns = ['-', '+', 'x', '\\', '*', 'o', 'O', '.', '/']
colors = ['r', 'g', 'y', 'b', 'm', 'c']

def cmp_overall_qoe_cps():
    google_QoE_folder = geographical_data_folder + "google/dataQoE/"
    azure_QoE_folder = geographical_data_folder + "azure/dataQoE/"
    amazon_QoE_folder = geographical_data_folder + "amazon/dataQoE/"

    qoogle_session_qoes = load_all_session_qoes(google_QoE_folder)
    azure_session_qoes = load_all_session_qoes(azure_QoE_folder)
    amazon_session_qoes = load_all_session_qoes(amazon_QoE_folder)

    fig, ax = plt.subplots()

    draw_cdf(qoogle_session_qoes, styles[0], "Google Cloud CDN")
    draw_cdf(azure_session_qoes, styles[1], "Azure CDN (Verizon)")
    draw_cdf(amazon_session_qoes, styles[2], "Amazon CloudFront")

    ax.set_xlabel(r'Session QoE (0-5)', fontsize=18)
    ax.set_ylabel(r'Percentage of PlanetLab users', fontsize=18)
    plt.xlim([0, 5])
    plt.ylim([0, 1])
    plt.legend(loc=2)

    imgName = img_folder + "compare_cloud_cdns_QoE_overall"
    plt.savefig(imgName + ".jpg")
    plt.savefig(imgName + ".pdf")
    plt.savefig(imgName + ".png")
    plt.show()

def cmp_overall_qoe_per_region(regions, regionName):
    google_QoE_folder = geographical_data_folder + "google/dataQoE/"
    azure_QoE_folder = geographical_data_folder + "azure/dataQoE/"
    amazon_QoE_folder = geographical_data_folder + "amazon/dataQoE/"

    qoogle_regional_qoes = load_all_session_qoes_per_region(google_QoE_folder)
    azure_regional_qoes = load_all_session_qoes_per_region(azure_QoE_folder)
    amazon_regional_qoes = load_all_session_qoes_per_region(amazon_QoE_folder)

    google_to_draw = []
    azure_to_draw = []
    amazon_to_draw = []
    for r in regions:
        google_to_draw.extend(qoogle_regional_qoes[r])
        azure_to_draw.extend(azure_regional_qoes[r])
        amazon_to_draw.extend(amazon_regional_qoes[r])

    fig, ax = plt.subplots()

    draw_cdf(google_to_draw, styles[0], "Google Cloud CDN")
    draw_cdf(azure_to_draw, styles[1], "Azure CDN (Verizon)")
    draw_cdf(amazon_to_draw, styles[2], "Amazon CloudFront")

    ax.set_xlabel(r'Session QoE (0-5)', fontsize=18)
    ax.set_ylabel(r'Percentage of PlanetLab users', fontsize=18)
    plt.xlim([0, 5])
    plt.ylim([0, 1])
    plt.legend(loc=2)

    imgName = img_folder + "compare_cloud_cdns_QoE_region_" + regionName
    plt.savefig(imgName + ".jpg")
    plt.savefig(imgName + ".pdf")
    plt.savefig(imgName + ".png")
    plt.show()

def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.2f' % height,
                ha='center', va='bottom')


def cmp_qoe_stats_over_regions():
    google_QoE_folder = geographical_data_folder + "google/dataQoE/"
    azure_QoE_folder = geographical_data_folder + "azure/dataQoE/"
    amazon_QoE_folder = geographical_data_folder + "amazon/dataQoE/"

    google_regional_qoes = load_all_session_qoes_per_region(google_QoE_folder)
    azure_regional_qoes = load_all_session_qoes_per_region(azure_QoE_folder)
    amazon_regional_qoes = load_all_session_qoes_per_region(amazon_QoE_folder)

    regions = ["North America", "South America", "Europe", "Asia", "Australia"]

    ind = np.arange(len(regions))
    width = 0.3

    fig, ax = plt.subplots()

    google_qoe_mn = [np.mean(google_regional_qoes[r]) for r in regions]
    google_qoe_std = [np.std(google_regional_qoes[r]) for r in regions]
    google_rects = ax.bar(ind, google_qoe_mn, width, hatch=patterns[0], color=colors[0], yerr=google_qoe_std)

    azure_qoe_mn = [np.mean(azure_regional_qoes[r]) for r in regions]
    azure_qoe_std = [np.std(azure_regional_qoes[r]) for r in regions]
    azure_rects = ax.bar(ind + width, azure_qoe_mn, width, hatch=patterns[1], color=colors[1], yerr=azure_qoe_std)

    amazon_qoe_mn = [np.mean(amazon_regional_qoes[r]) for r in regions]
    amazon_qoe_std = [np.std(amazon_regional_qoes[r]) for r in regions]
    amazon_rects = ax.bar(ind + 2*width, amazon_qoe_mn, width, hatch=patterns[2], color=colors[2], yerr=amazon_qoe_std)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Mean and Std of Session QoEs')
    # ax.set_title('QoE across regions')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(["N. America", "S. America", "Europe", "Asia", "Australia"])

    ax.legend((google_rects[0], azure_rects[0], amazon_rects[0]),
              ('Google Cloud CDN', 'Azure CDN(Verizon)', "Amazon CloudFront"),
              loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)

    autolabel(ax, google_rects)
    autolabel(ax, azure_rects)
    autolabel(ax, amazon_rects)

    imgName = img_folder + "compare_cloud_cdns_QoE_across_regions"
    plt.savefig(imgName + ".jpg")
    plt.savefig(imgName + ".pdf")
    plt.savefig(imgName + ".png")

    plt.show()



if __name__ == '__main__':

    ## Figure 4 to show overall QoE comparison among 3 Cloud CDNs
    # cmp_overall_qoe_cps()

    ## Figure 5 to show the bar graphs of overall QoE among regions for 3 Cloud CDNs
    # cmp_qoe_stats_over_regions()

    ## Figure 6 to show overall QoE comparison among 3 Cloud CDNs in region North and South America
    cmp_overall_qoe_per_region(["North America", "South America"], "America")
    cmp_overall_qoe_per_region(["Asia", "Australia"], "Asia-Oceania")
    cmp_overall_qoe_per_region(["Europe"], "Europe")





