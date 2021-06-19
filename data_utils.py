"""
This module contains a set of functions that parse the training data set and
compute the centers for the data clusters.
Here you will also find dictionaries contatining Sentinel2 and Landsat7/8
bands, as well as distionaries containing the mean values for each class.
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


HCRF_FILE = os.path.join(os.getcwd(), 'TrainingData', 'TrainingData.csv')
SAVEFIG_PATH = os.getcwd()

HA = {}
LA = {}
CI = {}
CC = {}
WAT = {}
SN = {}

HA_L8 = {}
LA_L8 = {}
CI_L8 = {}
CC_L8 = {}
WAT_L8 = {}
SN_L8 = {}

HA_L7 = {}
LA_L7 = {}
CI_L7 = {}
CC_L7 = {}
WAT_L7 = {}
SN_L7 = {}

BANDS = {
    1: [433, 453],
    2: [457, 522],
    3: [542, 578],
    4: [650, 680],
    5: [697, 712],
    6: [732, 747],
    7: [776, 796],
    8: [855, 875],  # 8a
    9: [935, 955],
    10: [1365, 1385],
    11: [1565, 1655],
    12: [2100, 2280]
}

BANDS_LANDSAT_8 = {
    1: [430, 450],
    2: [450, 510],
    3: [530, 590],
    4: [640, 670],
    5: [850, 880],
    6: [1570, 1650],
    7: [2110, 2290],
    8: [500, 680],
    9: [1360, 1380]
}

BANDS_LANDSAT_7 = {
    1: [450, 520],
    2: [520, 600],
    3: [630, 690],
    4: [770, 900],
    5: [1550, 1750],
    7: [2064, 2354],
    8: [520, 900]
}

def plot_training_spectra(BANDS, HA, LA, CI, CC, WAT, SN, mission="Sentinel2"):
    ax = plt.subplot(1, 1, 1)
    xpoints = BANDS.keys()
    plt.plot(xpoints, HA.values(), 'o:g', label="High Algae")
    plt.plot(xpoints, LA.values(), 'o:y', label="Low Algae")
    plt.plot(xpoints, CI.values(), 'o:b', label="Clean Ice")
    plt.plot(xpoints, CC.values(), 'o:m', label="Cryoconite")
    plt.plot(xpoints, WAT.values(), 'o:k', label="Water")
    plt.plot(xpoints, SN.values(), 'o:c', label="Snow")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(labels)
    plt.grid()
    plt.xlabel("{} bands".format(mission))
    plt.ylabel("Albedo")
    plt.title("Spectra of training data")
    plt.savefig(os.path.join(SAVEFIG_PATH, 'TrainingSpectra{}.png'.format(mission)))
    plt.close()

def create_dataset(file=HCRF_FILE, savefig=True):
    hcrf_master = pd.read_csv(file)
    HA_hcrf = pd.DataFrame()
    LA_hcrf = pd.DataFrame()
    CI_hcrf = pd.DataFrame()
    CC_hcrf = pd.DataFrame()
    WAT_hcrf = pd.DataFrame()
    SN_hcrf = pd.DataFrame()

    # Group site names according to surface class

    HAsites = ['13_7_SB2', '13_7_SB4', '14_7_S5', '14_7_SB1', '14_7_SB5', '14_7_SB10',
               '15_7_SB3', '21_7_SB1', '21_7_SB7', '22_7_SB4', '22_7_SB5', '22_7_S3', '22_7_S5',
               '23_7_SB3', '23_7_SB5', '23_7_S3', '23_7_SB4', '24_7_SB2', 'HA_1', 'HA_2', 'HA_3',
               'HA_4', 'HA_5', 'HA_6', 'HA_7', 'HA_8', 'HA_10', 'HA_11', 'HA_12', 'HA_13', 'HA_14',
               'HA_15', 'HA_16', 'HA_17', 'HA_18', 'HA_19', 'HA_20', 'HA_21', 'HA_22', 'HA_24',
               'HA_25', 'HA_26', 'HA_27', 'HA_28', 'HA_29', 'HA_30', 'HA_31', '13_7_S2', '14_7_SB9',
               'MA_11', 'MA_14', 'MA_15', 'MA_17', '21_7_SB2', '22_7_SB1', 'MA_4', 'MA_7', 'MA_18',
               '27_7_16_SITE3_WMELON1', '27_7_16_SITE3_WMELON3', '27_7_16_SITE2_ALG1',
               '27_7_16_SITE2_ALG2', '27_7_16_SITE2_ALG3', '27_7_16_SITE2_ICE3', '27_7_16_SITE2_ICE5',
               '27_7_16_SITE3_ALG4', '5_8_16_site2_ice7', '5_8_16_site3_ice2', '5_8_16_site3_ice3',
               '5_8_16_site3_ice5', '5_8_16_site3_ice6', '5_8_16_site3_ice7', '5_8_16_site3_ice8',
               '5_8_16_site3_ice9']

    LAsites = ['14_7_S2', '14_7_S3', '14_7_SB2', '14_7_SB3', '14_7_SB7', '15_7_S2',
               '15_7_SB4', '20_7_SB1', '20_7_SB3', '21_7_S1', '21_7_S5', '21_7_SB4', '22_7_SB2',
               '22_7_SB3', '22_7_S1', '23_7_S1', '23_7_S2', '24_7_S2', 'MA_1', 'MA_2', 'MA_3',
               'MA_5', 'MA_6', 'MA_8', 'MA_9', 'MA_10', 'MA_12', 'MA_13', 'MA_16', 'MA_19',
               '13_7_S1', '13_7_S3', '14_7_S1', '15_7_S1', '15_7_SB2', '20_7_SB2', '21_7_SB5',
               '21_7_SB8', '25_7_S3', '5_8_16_site2_ice10', '5_8_16_site2_ice5',
               '5_8_16_site2_ice9', '27_7_16_SITE3_WHITE3']

    CIsites = ['21_7_S4', '13_7_SB3', '15_7_S4', '15_7_SB1', '15_7_SB5', '21_7_S2',
               '21_7_SB3', '22_7_S2', '22_7_S4', '23_7_SB1', '23_7_SB2', '23_7_S4',
               'WI_1', 'WI_2', 'WI_4', 'WI_5', 'WI_6', 'WI_7', 'WI_9', 'WI_10', 'WI_11',
               'WI_12', 'WI_13', '27_7_16_SITE3_WHITE1', '27_7_16_SITE3_WHITE2',
               '27_7_16_SITE2_ICE2', '27_7_16_SITE2_ICE4', '27_7_16_SITE2_ICE6',
               '5_8_16_site2_ice1', '5_8_16_site2_ice2', '5_8_16_site2_ice3',
               '5_8_16_site2_ice4', '5_8_16_site2_ice6', '5_8_16_site2_ice8',
               '5_8_16_site3_ice1', '5_8_16_site3_ice4']

    CCsites = ['DISP1', 'DISP2', 'DISP3', 'DISP4', 'DISP5', 'DISP6', 'DISP7', 'DISP8',
               'DISP9', 'DISP10', 'DISP11', 'DISP12', 'DISP13', 'DISP14', '27_7_16_SITE3_DISP1',
               '27_7_16_SITE3_DISP3']

    WATsites = ['21_7_SB5', '21_7_SB8', 'WAT_1', 'WAT_3', 'WAT_6']

    SNsites = ['14_7_S4', '14_7_SB6', '14_7_SB8', '17_7_SB2', 'SNICAR100', 'SNICAR200',
               'SNICAR300', 'SNICAR400', 'SNICAR500', 'SNICAR600', 'SNICAR700', 'SNICAR800',
               'SNICAR900', 'SNICAR1000', '27_7_16_KANU_', '27_7_16_SITE2_1',
               '5_8_16_site1_snow10', '5_8_16_site1_snow2', '5_8_16_site1_snow3',
               '5_8_16_site1_snow4', '5_8_16_site1_snow6', '5_8_16_site1_snow7',
               '5_8_16_site1_snow9']

    for i in HAsites:
        hcrf_HA = np.array(hcrf_master[i])
        HA_hcrf['{}'.format(i)] = hcrf_HA

    for ii in LAsites:
        hcrf_LA = np.array(hcrf_master[ii])
        LA_hcrf['{}'.format(ii)] = hcrf_LA

    for iii in CIsites:
        hcrf_CI = np.array(hcrf_master[iii])
        CI_hcrf['{}'.format(iii)] = hcrf_CI

    for iv in CCsites:
        hcrf_CC = np.array(hcrf_master[iv])
        CC_hcrf['{}'.format(iv)] = hcrf_CC

    for v in WATsites:
        hcrf_WAT = np.array(hcrf_master[v])
        WAT_hcrf['{}'.format(v)] = hcrf_WAT

    for vi in SNsites:
        hcrf_SN = np.array(hcrf_master[vi])
        SN_hcrf['{}'.format(vi)] = hcrf_SN

    for band in BANDS.keys():
        min_wl_index = BANDS[band][0] - 350
        max_wl_index = BANDS[band][1] - 350

        HA[band] = HA_hcrf[min_wl_index:max_wl_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        LA[band] = LA_hcrf[min_wl_index:max_wl_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        CI[band] = CI_hcrf[min_wl_index:max_wl_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        CC[band] = CC_hcrf[min_wl_index:max_wl_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        WAT[band] = WAT_hcrf[min_wl_index:max_wl_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        SN[band] = SN_hcrf[min_wl_index:max_wl_index].mean(axis='columns').mean(axis='index').astype(np.float64)

    for band in BANDS_LANDSAT_8.keys():
        min_l8_index = BANDS_LANDSAT_8[band][0] - 350
        max_l8_index = BANDS_LANDSAT_8[band][1] - 350

        HA_L8[band] = HA_hcrf[min_l8_index:max_l8_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        LA_L8[band] = LA_hcrf[min_l8_index:max_l8_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        CI_L8[band] = CI_hcrf[min_l8_index:max_l8_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        CC_L8[band] = CC_hcrf[min_l8_index:max_l8_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        WAT_L8[band] = WAT_hcrf[min_l8_index:max_l8_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        SN_L8[band] = SN_hcrf[min_l8_index:max_l8_index].mean(axis='columns').mean(axis='index').astype(np.float64)

    for band in BANDS_LANDSAT_7.keys():
        min_l7_index = BANDS_LANDSAT_7[band][0] - 350
        max_l7_index = BANDS_LANDSAT_7[band][1] - 350

        HA_L7[band] = HA_hcrf[min_l7_index:max_l7_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        LA_L7[band] = LA_hcrf[min_l7_index:max_l7_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        CI_L7[band] = CI_hcrf[min_l7_index:max_l7_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        CC_L7[band] = CC_hcrf[min_l7_index:max_l7_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        WAT_L7[band] = WAT_hcrf[min_l7_index:max_l7_index].mean(axis='columns').mean(axis='index').astype(np.float64)
        SN_L7[band] = SN_hcrf[min_l7_index:max_l7_index].mean(axis='columns').mean(axis='index').astype(np.float64)


    if savefig:
        plot_training_spectra(BANDS, HA, LA, CI, CC, WAT, SN, mission="Sentinel2")
        plot_training_spectra(BANDS_LANDSAT_8, HA_L8, LA_L8, CI_L8, CC_L8, WAT_L8, SN_L8, mission="Landsat8")
        plot_training_spectra(BANDS_LANDSAT_7, HA_L7, LA_L7, CI_L7, CC_L7, WAT_L7, SN_L7, mission="Landsat7")


COLORS = {
    1: [135, 206, 250], # BLUE - ICE
    2: [255, 255, 255], # WHITE - SNOW
    3: [60, 179, 113], # LIGHT GREEN - ALGAE_LOW
    4: [0, 100, 0], # DARK GREEN - ALGAE_HIGH
    #5: [65, 105, 225], # WATER
    5: [0, 0, 0], #CRYOCONITE
    6: [211, 211, 211] #OUTSIDE SNOW/ICE AREA
}
