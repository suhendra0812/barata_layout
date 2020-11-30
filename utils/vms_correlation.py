from datetime import datetime, timedelta
import os, glob, shutil
import pandas as pd
import subprocess

SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)

VMS_PATH = f"{BASE_PATH}\\9.vms"
SRC_VMS_PATH = f"{BASE_PATH}\\7.barata_ship\\src"
TEMP_VMS_PATH = f"{BASE_PATH}\\7.barata_ship\\temp"
OUTPUT_VMS_PATH = f"{BASE_PATH}\\7.barata_ship\\output"

def correlation(data_path):
    outputvms_list = glob.glob(f"{OUTPUT_VMS_PATH}\\{data_path[-15:].replace('_','')}*\\*csv")
                
    date = data_path[-15:-7]
    date_time = datetime.strptime(data_path[-15:-2], '%Y%m%d_%H%M')
    starttime = (date_time - timedelta(minutes=30)).strftime('%m/%d/%Y %H:%M:%S')
    endtime = (date_time + timedelta(minutes=30)).strftime('%m/%d/%Y %H:%M:%S')
    
    vmsdata_path = f"{VMS_PATH}\\{date[:4]}\\indo_{date}_vms.csv"
    if not os.path.exists(vmsdata_path):
        print(f'Data VMS pada periode {date} tidak tersedia\n')

        # download VMS data from UMV Portal
        vms_downloader = glob.glob(f'{VMS_PATH}/*/vms_downloader.py')[0]
        cmd = f'python {vms_downloader} {date}'
        subprocess.call(cmd)

    vms_df = pd.read_csv(vmsdata_path)
    vmsfilter_df = vms_df.copy()
    vmsfilter_df = vmsfilter_df.loc[(vmsfilter_df['Location date'] >= starttime) & (vmsfilter_df['Location date'] <= endtime)]

    vmsfilter_df.to_csv(f"{TEMP_VMS_PATH}\\dataUMV.csv", index=False)

    if len(outputvms_list) == 0:   
        types = ('*SHIPKML.zip','*SHIP.shp','*SHIP.dbf','*SHIP.prj','*SHIP.shx')
        ship_list = []
        for files in types:
            file_list = glob.glob(f"{data_path}\\{files}")
            if len(file_list) > 0:
                file_type = file_list[0]
                ship_list.append(file_type)
                
        if len(ship_list) == 5:
            for ship in ship_list:
                shutil.copy(ship, TEMP_VMS_PATH)
            
            os.chdir(SRC_VMS_PATH)
            
            sat_name = os.path.basename(ship)[:2]
            if sat_name == 'CS':
                subprocess.call('bash -c ./run_cosmo.R')
            elif sat_name == 'S1':
                subprocess.call('bash -c ./run_sentinel.R')
            else:
                subprocess.call('bash -c ./run_radarsat.R')

            temp_list = glob.glob(f"{TEMP_VMS_PATH}\\*")        
            if len(temp_list) > 0:
                #remove files
                for temp in temp_list:
                    if temp == f"{TEMP_VMS_PATH}\\dataUMV.csv":
                        pass
                    else:
                        os.remove(temp)

