import os
import sys
import shutil
import glob
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta
from zipfile import ZipFile
#from tkinter import Tk, filedialog

BASE_PATH = 'D:\\BARATA'
BARATA_SHIP_PATH = f'{BASE_PATH}\\7.barata_ship\\output\\'

AISDATA_BASEPATH = f'{BASE_PATH}\\10.ais'

def get_ais_info(ship_path):
    # read ship data
    shipdf = pd.read_csv(ship_path)

    # filter ship data to show only transmitted ship
    shipfilterdf = shipdf.copy()
    shipfilterdf = shipfilterdf[~pd.isnull(shipfilterdf['Asosiasi (AIS/VMS)'])]

    ship_basepath = os.path.dirname(ship_path)

    # read AIS data in the data folder if available
    ais_paths = glob.glob(f'{ship_basepath}\\*ais.csv')

    # check if there is ship with AIS associated
    if (shipfilterdf['Asosiasi (AIS/VMS)'] == 'AIS').any():
        print('Terdapat asosiasi dengan AIS\n')
        aisdf = shipfilterdf.copy()
        aisdf = aisdf[aisdf['Asosiasi (AIS/VMS)'] == 'AIS']

        # define data datetime
        # shipdate = datetime.strptime(ship_basepath[-15:], '%Y%m%d_%H%M%S')
        # startdate = (shipdate - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
        # stopdate = (shipdate + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')

        #aisdata_list = glob.glob(f'{AISDATA_BASEPATH}\\{ship_basepath[-15:-11]}\\*{ship_basepath[-15:-7]}*_ais.csv')
        aisdata_list = glob.glob(f'{AISDATA_BASEPATH}\\{ship_basepath[-15:-11]}\\*{ship_basepath[-15:-7]}*.zip')

        if len(aisdata_list) > 0:
            aisdatazip_path = aisdata_list[0]
            aisdatacsv_path = f'{os.path.dirname(aisdatazip_path)}\\indo_{ship_basepath[-15:-7]}_ais.csv'

            # extract ais data csv in zip file
            if not os.path.exists(aisdatacsv_path):
                with ZipFile(aisdatazip_path) as theZip:
                    fileNames = theZip.namelist()
                    for fileName in fileNames:
                        if fileName.endswith('csv'):
                            with theZip.open(fileName) as f:
                                with open(aisdatacsv_path, 'wb') as outfile:
                                    shutil.copyfileobj(f, outfile)

            # read ais data csv
            aisdatadf = pd.read_csv(aisdatacsv_path)

            # filter ais data to data datetime
            # aisdatadf = aisdatadf.loc[(aisdatadf['time'] >= startdate) & (aisdatadf['time'] <= stopdate)]

            # get vessel name, ship type and country from ais data
            def get_value(mmsi, column):
                value = aisdatadf[aisdatadf['mmsi'] == int(mmsi)][column].values
                if len(value) != 0:
                    return value[0]
                else:
                    return None

            aisdf['Nama Kapal'] = [get_value(mmsi, 'vessel_name') for mmsi in aisdf['MMSI']]
            aisdf['Tipe'] = [get_value(mmsi, 'ship_type') for mmsi in aisdf['MMSI']]
            aisdf['Asal'] = [get_value(mmsi, 'country') for mmsi in aisdf['MMSI']]

            # merge AIS dataframe to ship data
            aisshipdf = pd.merge(aisdf, shipdf, how='right')
            aisshipdf = aisshipdf[aisshipdf['Asosiasi (AIS/VMS)'] == 'AIS']

            # filter only some columns to appear
            shipaisdf = aisshipdf[['No.', 'Nama Kapal', 'Tipe', 'Asal', 'Longitude', 'Latitude', 'Heading (deg)']]
            shipaisdf = shipaisdf.round(6)
            shipaisdf['Heading (deg)'] = shipaisdf['Heading (deg)'].astype(int)

            print('Informasi kapal AIS:')
            for i, row in shipaisdf[['Nama Kapal', 'Tipe', 'Asal']].iterrows():
                print(f"{i+1}.\tNama\t: {row['Nama Kapal']}\n\tTipe\t: {row['Tipe']}\n\tAsal\t: {row['Asal']}\n")

            shipaisdf.set_index('No.', inplace=True)
            shipaisdf = shipaisdf.sort_index()
            shipaisdf.to_csv(ship_path[:-9] + '_ais.csv')

            print('Tabel AIS telah dibuat\n')

            return shipaisdf

        else:
            print(f'Data AIS pada periode {ship_basepath[-15:-7]} tidak tersedia')
            print('Tabel AIS tidak dapat dibuat\n')

    else:
        print('Tidak ada asosiasi dengan AIS\n')


def get_vms_info(ship_path):
    # read ship data
    shipdf = pd.read_csv(ship_path)
    shipgdf = gpd.GeoDataFrame(shipdf, geometry=gpd.points_from_xy(shipdf['Longitude'], shipdf['Latitude']))

    # filter ship data to show only transmitted ship
    shipfilterdf = shipdf.copy()
    shipfilterdf = shipfilterdf[~pd.isnull(shipfilterdf['Asosiasi (AIS/VMS)'])]

    # read VMS data in the data folder if available
    vms_paths = glob.glob(f'{os.path.dirname(ship_path)}\\*_vms.csv')

    # check if there is ship with VMS associated
    if (shipfilterdf['Asosiasi (AIS/VMS)'] == 'VMS').any():
        print('Terdapat asosiasi dengan VMS\n')

        # read output of VMS correlation analysis
        vms_ff = os.path.dirname(ship_path)[-15:].replace('_', '')[:-4]
        vms_list = glob.glob(f'{BARATA_SHIP_PATH}\\{vms_ff}*\\*.csv')

        if len(vms_list) > 0:

            # create dataframe from list of the output
            vmsdf = pd.concat([pd.read_csv(vms_path) for vms_path in vms_list], ignore_index=True)

            # filter by VMS associated only
            vmsdf = vmsdf[~vmsdf['status'].isin(['no_ais_vms', 'ais'])]
            vmsgdf = gpd.GeoDataFrame(vmsdf, geometry=gpd.points_from_xy(vmsdf['longitude'], vmsdf['latitude']))

            # merge VMS dataframe to ship data
            vmsbuffergdf = vmsgdf.copy()
            vmsbuffergdf.geometry = vmsbuffergdf.geometry.buffer(0.000001)
            shipbuffergdf = shipgdf.copy()
            shipbuffergdf.geometry = shipbuffergdf.geometry.buffer(0.000001)

            vmsshipgdf = gpd.sjoin(vmsbuffergdf, shipbuffergdf, how='inner', op='intersects').drop(columns=['longitude', 'latitude'])
            vmsshipdf = pd.DataFrame(vmsshipgdf.drop(columns='geometry'))

            # rename 'status' column to 'Nama Kapal' column
            vmsshipdf['status'] = [status.split('_')[1] for status in vmsshipgdf['status']]
            vmsshipdf = vmsshipdf.rename(columns={'status': 'Nama Kapal'})

            # filter only some columns to appear
            shipvmsdf = vmsshipdf[['No.', 'Nama Kapal', 'Longitude', 'Latitude', 'Panjang (m)', 'Heading (deg)']]
            shipvmsdf = shipvmsdf.round(6)
            shipvmsdf['Heading (deg)'] = shipvmsdf['Heading (deg)'].astype(int)

            print('Informasi nama kapal VMS:')
            for j, vms_name in enumerate(shipvmsdf['Nama Kapal']):
                print(f'{j+1}. {vms_name}')

            shipvmsdf.set_index('No.', inplace=True)
            shipvmsdf = shipvmsdf.sort_index()
            shipvmsdf.to_csv(f'{ship_path[:-9]}_vms.csv')

            print('\nTabel VMS telah dibuat\n')

            return shipvmsdf

        else:
            print(f'Tidak terdapat data korelasi VMS di folder {vms_ff}\n')

            # #alternative correlated VMS directory
            # correlated_path = os.path.dirname(ship_path).replace('2.seonse_outputs','12.correlated_ship')
            # vms_list = glob.glob(f'{correlated_path}\\*CORRELATED.shp')
            # if len(vms_list) > 0:
            #     vmsdata_list = glob.glob(f'{correlated_path}\\*vms.csv')

            #     vmsgdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(vms_path) for vms_path in vms_list], ignore_index=True))
            #     vmsgdf = vmsgdf[vmsgdf['STATUS'].isin(['VMS'])]

            #     vmsdatadf = pd.concat([pd.read_csv(vmsdata) for vmsdata in vmsdata_list], ignore_index=True)

            #     vmsgdf['Nama Kapal'] = [vmsdatadf[vmsdatadf['Beacon ID'] == int(beacon)]['Mobile name'].array[0] for beacon in vmsgdf['NEAREST_BE']]

            #     #merge VMS dataframe to ship data
            #     vmsbuffergdf = vmsgdf.copy()
            #     vmsbuffergdf.geometry = vmsbuffergdf.geometry.buffer(0.000001)
            #     shipbuffergdf = shipgdf.copy()
            #     shipbuffergdf.geometry = shipbuffergdf.geometry.buffer(0.000001)

            #     vmsshipgdf = gpd.sjoin(vmsbuffergdf, shipbuffergdf, how='inner', op='intersects')

            #     shipvmsdf = vmsshipgdf[['No.','Nama Kapal','Longitude','Latitude','Panjang (m)','Heading (deg)']]
            #     shipvmsdf = shipvmsdf.round(6)
            #     shipvmsdf['Heading (deg)'] = shipvmsdf['Heading (deg)'].astype(int)

            #     print ('Informasi nama kapal VMS:')
            #     for j, vms_name in enumerate(shipvmsdf['Nama Kapal']):
            #         print (f'{j+1}. {vms_name}')

            #     shipvmsdf.set_index('No.', inplace=True)
            #     shipvmsdf = shipvmsdf.sort_index()
            #     shipvmsdf.to_csv(f'{ship_path[:-9]}_vms.csv')

            #     print ('\nTabel VMS telah dibuat\n')

            #     return shipvmsdf

            # else:
            #     print (f'Tidak terdapat data korelasi VMS di folder {correlated_path}\n')

    else:
        print('Tidak ada asosiasi dengan VMS\n')


"""
Tk().withdraw()
data_paths = glob.glob(filedialog.askdirectory(initialdir = BASE_PATH, title = "Choose data ship directory")[:-4] + "*")
#data_paths = filedialog.askopenfilename(initialdir = basePath, title = "Choose data ship file", filetypes = (("CSV files","*.csv"),("all files","*.*")))
#data_paths = QFileDialog.getOpenFileName(None, "Choose data ship file", basePath, 'CSV Files (*.csv)')[0]
for data_path in data_paths:
    ship_paths = glob.glob(f'{data_path}\\*ship.csv')
    if len(ship_paths) > 0:
        for ship_path in ship_paths:
            print (os.path.basename(ship_path)[:-4])
            ais_info = get_ais_info(ship_path)
            vms_info = get_vms_info(ship_path)  

#input('Tekan ENTER untuk membuka folder!')
#os.startfile(os.path.dirname(ship_path))
print ('Selesai')
input('Tekan ENTER untuk keluar!')
"""
