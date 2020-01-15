import os, sys, glob
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta
#from tkinter import Tk, filedialog

base_path = 'D:\\BARATA'
rdrvms_path = f'{base_path}\\7.barata_ship\\output\\'

aisdata_basepath = f'{base_path}\\10.ais'
ais_info_path = f'{aisdata_basepath}\\ais_info.csv'
ais_infodf = pd.read_csv(ais_info_path)

def get_ais_info(ship_path):
    #read ship data
    shipdf = pd.read_csv(ship_path)

    #filter ship data to show only transmitted ship
    shipfilterdf = shipdf.copy()
    shipfilterdf = shipfilterdf[~pd.isnull(shipfilterdf['Asosiasi (VMS/AIS)'])]

    ship_basepath = os.path.dirname(ship_path)
    
    #read AIS data in the data folder if available
    ais_paths = glob.glob(f'{ship_basepath}\\*ais.csv')
    if len(ais_paths) == 0:
        #check if there is ship with AIS associated
        if (shipfilterdf['Asosiasi (VMS/AIS)'] == 'AIS').any():
            print ('Terdapat asosiasi dengan AIS\n')
            aisdf = shipfilterdf.copy()
            aisdf = aisdf[aisdf['Asosiasi (VMS/AIS)'] == 'AIS']

            #define data datetime
            shipdate = datetime.strptime(ship_basepath[-15:], '%Y%m%d_%H%M%S')
            startdate = (shipdate - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
            stopdate = (shipdate + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')

            aisdata_list = glob.glob(f'{aisdata_basepath}\\{ship_basepath[-15:-11]}\\*{ship_basepath[-15:-7]}*_ais.csv')
            if len(aisdata_list) > 0:
                aisdata_path = aisdata_list[0]

                aisdatadf = pd.read_csv(aisdata_path)

                #filter ais data to data datetime
                aisdatadf = aisdatadf.loc[(aisdatadf['time'] >= startdate) & (aisdatadf['time'] <= stopdate)]

                #get vessel name, ship type and country from ais data
                aisdf['Nama Kapal'] = [aisdatadf[aisdatadf['mmsi'] == int(mmsi)]['vessel_name'].array[0] for mmsi in aisdf['MMSI']]
                aisdf['Tipe'] = [aisdatadf[aisdatadf['mmsi'] == int(mmsi)]['ship_type'].array[0] for mmsi in aisdf['MMSI']]
                aisdf['Asal'] = [aisdatadf[aisdatadf['mmsi'] == int(mmsi)]['country'].array[0] for mmsi in aisdf['MMSI']]

                #merge AIS dataframe to ship data
                aisshipdf = pd.merge(aisdf, shipdf, how='right')
                aisshipdf = aisshipdf[aisshipdf['Asosiasi (VMS/AIS)'] == 'AIS']

                #filter only some columns to appear
                shipaisdf = aisshipdf[['No.','Nama Kapal','Tipe','Asal','Longitude','Latitude','Heading (deg)']]
                shipaisdf = shipaisdf.round(6)
                shipaisdf['Heading (deg)'] = shipaisdf['Heading (deg)'].astype(int)

                print ('Informasi kapal AIS:')
                for i, row in shipaisdf[['Nama Kapal', 'Tipe', 'Asal']].iterrows():
                    print (f"{i+1}.\tNama\t: {row['Nama Kapal']}\n\tTipe\t: {row['Tipe']}\n\tAsal\t: {row['Asal']}\n")
                
                shipaisdf.set_index('No.', inplace=True)
                shipaisdf = shipaisdf.sort_index()
                shipaisdf.to_csv(ship_path[:-9] + '_ais.csv')
                
                print ('Tabel AIS telah dibuat\n')

                return shipaisdf

            else:
                print (f'Data AIS pada periode {ship_basepath[-15:-7]} tidak tersedia\n')

        else:
            print ('Tidak ada asosiasi dengan AIS\n')
    else:
        print ('Tabel AIS telah dibuat\n')

def get_vms_info(ship_path):
    #read ship data
    shipdf = pd.read_csv(ship_path)
    shipgdf = gpd.GeoDataFrame(shipdf, geometry=gpd.points_from_xy(shipdf['Longitude'],shipdf['Latitude']))

    #filter ship data to show only transmitted ship
    shipfilterdf = shipdf.copy()
    shipfilterdf = shipfilterdf[~pd.isnull(shipfilterdf['Asosiasi (VMS/AIS)'])]

    #read VMS data in the data folder if available
    vms_paths = glob.glob(f'{os.path.dirname(ship_path)}\\*_vms.csv')
    if len(vms_paths) == 0:
        #check if there is ship with VMS associated
        if (shipfilterdf['Asosiasi (VMS/AIS)'] == 'VMS').any():
            print ('Terdapat asosiasi dengan VMS\n')

            #read output of VMS correlation analysis
            vms_ff = os.path.dirname(ship_path)[-15:].replace('_','')[:-4]
            vms_list = glob.glob(f'{rdrvms_path}\\{vms_ff}*\\*.csv')

            if len(vms_list) > 0:

                #create dataframe from list of the output
                vmsdf = pd.concat([pd.read_csv(vms_path) for vms_path in vms_list], ignore_index=True)

                #filter by VMS associated only
                vmsdf = vmsdf[~vmsdf['status'].isin(['no_ais_vms','ais'])]
                vmsgdf = gpd.GeoDataFrame(vmsdf, geometry=gpd.points_from_xy(vmsdf['longitude'],vmsdf['latitude']))

                #merge VMS dataframe to ship data
                vmsbuffergdf = vmsgdf.copy()
                vmsbuffergdf.geometry = vmsbuffergdf.geometry.buffer(0.000001)
                shipbuffergdf = shipgdf.copy()
                shipbuffergdf.geometry = shipbuffergdf.geometry.buffer(0.000001)

                vmsshipgdf = gpd.sjoin(vmsbuffergdf, shipbuffergdf, how='inner', op='intersects').drop(columns=['longitude','latitude'])
                vmsshipdf = pd.DataFrame(vmsshipgdf.drop(columns='geometry'))

                #rename 'status' column to 'Nama Kapal' column
                vmsshipdf['status'] = [status.split('_')[1] for status in vmsshipgdf['status']]
                vmsshipdf = vmsshipdf.rename(columns={'status':'Nama Kapal'})

                #filter only some columns to appear
                shipvmsdf = vmsshipdf[['No.','Nama Kapal','Longitude','Latitude','Panjang (m)','Heading (deg)']]
                shipvmsdf = shipvmsdf.round(6)
                shipvmsdf['Heading (deg)'] = shipvmsdf['Heading (deg)'].astype(int)

                print ('Informasi nama kapal VMS:')
                for j, vms_name in enumerate(shipvmsdf['Nama Kapal']):
                    print (f'{j+1}. {vms_name}')

                shipvmsdf.set_index('No.', inplace=True)
                shipvmsdf = shipvmsdf.sort_index()
                shipvmsdf.to_csv(f'{ship_path[:-9]}_vms.csv')

                print ('\nTabel VMS telah dibuat\n')

                return shipvmsdf

            else:
                print (f'Tidak terdapat data korelasi VMS di folder {vms_ff}\n')

                #alternative correlated VMS directory
                correlated_path = os.path.dirname(ship_path).replace('2.seonse_outputs','12.correlated_ship')
                vms_list = glob.glob(f'{correlated_path}\\*CORRELATED.shp')
                if len(vms_list) > 0:
                    vmsdata_list = glob.glob(f'{correlated_path}\\*vms.csv')
                
                    vmsgdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(vms_path) for vms_path in vms_list], ignore_index=True))
                    vmsgdf = vmsgdf[vmsgdf['STATUS'].isin(['VMS'])]

                    vmsdatadf = pd.concat([pd.read_csv(vmsdata) for vmsdata in vmsdata_list], ignore_index=True)

                    vmsgdf['Nama Kapal'] = [vmsdatadf[vmsdatadf['Beacon ID'] == int(beacon)]['Mobile name'].array[0] for beacon in vmsgdf['NEAREST_BE']]

                    #merge VMS dataframe to ship data
                    vmsbuffergdf = vmsgdf.copy()
                    vmsbuffergdf.geometry = vmsbuffergdf.geometry.buffer(0.000001)
                    shipbuffergdf = shipgdf.copy()
                    shipbuffergdf.geometry = shipbuffergdf.geometry.buffer(0.000001)

                    vmsshipgdf = gpd.sjoin(vmsbuffergdf, shipbuffergdf, how='inner', op='intersects')
                    
                    shipvmsdf = vmsshipgdf[['No.','Nama Kapal','Longitude','Latitude','Panjang (m)','Heading (deg)']]
                    shipvmsdf = shipvmsdf.round(6)
                    shipvmsdf['Heading (deg)'] = shipvmsdf['Heading (deg)'].astype(int)

                    print ('Informasi nama kapal VMS:')
                    for j, vms_name in enumerate(shipvmsdf['Nama Kapal']):
                        print (f'{j+1}. {vms_name}')

                    shipvmsdf.set_index('No.', inplace=True)
                    shipvmsdf = shipvmsdf.sort_index()
                    shipvmsdf.to_csv(f'{ship_path[:-9]}_vms.csv')

                    print ('\nTabel VMS telah dibuat\n')

                    return shipvmsdf

                else:
                    print (f'Tidak terdapat data korelasi VMS di folder {correlated_path}\n')

        else:
            print ('Tidak ada asosiasi dengan VMS\n')
    else:
        print ('Tabel VMS telah dibuat\n')
        
"""
Tk().withdraw()
data_paths = glob.glob(filedialog.askdirectory(initialdir = base_path, title = "Choose data ship directory")[:-4] + "*")
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
    


    
