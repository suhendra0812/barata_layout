# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 14:51:02 2019

@author: WSBARATA01
"""

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os, glob
import pandas as pd
from datetime import datetime
from qgis.core import QgsApplication
from PyQt5.QtWidgets import QFileDialog

#set QGIS application path and initialize it
QgsApplication.setPrefixPath('C:\\OSGeo4W64\\apps\\qgis', True)
qgs = QgsApplication([], False)
qgs.initQgis()

#source paths
base_path = "D:\\BARATA"
tpl_path = f'{base_path}\\11.barata_layout\\tb_templates'
tboutput_path = f'{base_path}\\8.technical_brief'

import sys
sys.path.append(base_path)

from barata_layout import RadarInfo

#input directory path
#Tk().withdraw()
#data_folder = filedialog.askdirectory(initialdir=f'{base_path}\\2.seonse_output',title='Select Data Directory')[:-4] + '*'
data_folder = QFileDialog.getExistingDirectory(None, 'Select Data Directory', f'{base_path}\\2.seonse_outputs')[:-4] + '*'

print ('Sumber data:')
print (data_folder)

#define list of data based on data folder
raster_list = glob.glob(f'{data_folder}\\*.tif')

if len(raster_list) > 0:
    print ('- Ada data raster')
    raster_path = raster_list[-1]
    raster_basename = os.path.basename(raster_path)
    
    #get radar info from raster filename
    bulan_dict = {'01':'JANUARI','02':'FEBRUARI','03':'MARET','04':'APRIL','05':'MEI','06':'JUNI','07':'JULI','08':'AGUSTUS','09':'SEPTEMBER','10':'OKTOBER','11':'NOVEMBER','12':'DESEMBER'}
    
    wil = os.path.basename(os.path.dirname(raster_path))[:-16]
    radar_info = RadarInfo(raster_basename)
    rdr_name = radar_info.rdr_name
    local = radar_info.local
    tgl_local = radar_info.tgl_local    
    bln_local = radar_info.bln_local
    thn_local = radar_info.thn_local
    jam_local = radar_info.jam_local
    thn = radar_info.thn
    bln = radar_info.bln
    tgl = radar_info.tgl
    j = radar_info.j
    m = radar_info.m
    d = radar_info.d
    con = radar_info.con
    mode = radar_info.mode
    pola = radar_info.pola
    
else:
    print ('- Tidak ada data raster')

if len(raster_list) > 1:
    method = 'gabungan'
else:
    method = 'satu'

if method == 'gabungan':
    local_datetime = local[:-2]
    date_time = datetime.strptime(local_datetime, '%Y%m%d_%H%M')
    time = f'{jam_local}:{m}'
else:
    local_datetime = local
    date_time = datetime.strptime(local_datetime, '%Y%m%d_%H%M%S')
    time = f'{jam_local}:{m}:{d}'

location = wil.capitalize()
radar = rdr_name
date = f'{tgl_local} {(bulan_dict[bln_local]).capitalize()} {thn_local}'

#project_type = input('Pilih jenis project (ship/oils): ')
project_type = 'ship'

layout_basepath = os.path.dirname(data_folder).replace("2.seonse_outputs","3.layouts") + "\\" + local[:8]

if project_type == 'ship':
    output_tb = f'TB IUU_{local_datetime} {wil.upper()}.docx'
    
    ship_list = glob.glob(f'{data_folder}\\*ship.csv')
    layout_list = glob.glob(f'{layout_basepath}\\*{local_datetime}*ship.png')
    
    if len(ship_list) > 0:
        print ('- Ada data kapal')
        ship_path = ship_list[0]
        ship_df = pd.read_csv(ship_path)
        
        ship_df[['Longitude', 'Latitude']] = ship_df[['Longitude', 'Latitude']].applymap('{:,.6f}'.format)
        ship_df[['Heading (deg)','MMSI']] = ship_df[['Heading (deg)','MMSI']].astype('Int64')
        
        ship_columns = ship_df.columns.to_list()
        ship_rows = [{'label': row.to_list()[0], 'cols': row.fillna('-').to_list()[1:]} for i, row in ship_df.iterrows()]
        
        echo_len = len(ship_df)
        
        ais_len = len(ship_df[ship_df['Asosiasi (VMS/AIS)'] == 'AIS'])
        vms_len = len(ship_df[ship_df['Asosiasi (VMS/AIS)'] == 'VMS'])
        
        echo_text = str(echo_len)
        non_text = str(echo_len - (ais_len+vms_len))
        
        ais_list = glob.glob(f'{os.path.dirname(raster_path)}\\*ais.csv')
        vms_list = glob.glob(f'{os.path.dirname(raster_path)}\\*vms.csv')
    
        
        if len(ais_list) > 0:
            print ('- Ada data AIS')
            ais_path = ais_list[0]
            ais_df = pd.read_csv(ais_path)
            ais_df[['Longitude', 'Latitude']] = ais_df[['Longitude', 'Latitude']].applymap('{:,.6f}'.format)
            
            ais_columns = ais_df.columns.to_list()
            ais_rows = [{'label': row.to_list()[0], 'cols': row.fillna('-').to_list()[1:]} for i, row in ais_df.iterrows()]
            ais_text = f"{ais_len}"
            
        else:
            print ('- Tidak ada data AIS')
            ais_columns = []
            ais_rows = []
            ais_text = "0"
        
        if len(vms_list) > 0:
            print ('- Ada data VMS')
            vms_path = vms_list[0]
            vms_df = pd.read_csv(vms_path)
            vms_df[['Longitude', 'Latitude']] = vms_df[['Longitude', 'Latitude']].applymap('{:,.6f}'.format)
            vms_df['Heading (deg)'] = vms_df['Heading (deg)'].astype('Int64')
            
            vms_columns = vms_df.columns.to_list()
            vms_rows = [{'label': row.to_list()[0], 'cols': row.fillna('-').to_list()[1:]} for i, row in vms_df.iterrows()]
            vms_text = f"{vms_len}"
            
        else:
            print ('- Tidak data VMS')
            vms_columns = []
            vms_rows = []
            vms_text = "0"
                
        
        if ais_len > 0 and vms_len > 0:
            tpl_path = f'{tpl_path}\\TB IUU TEMPLATE (AIS and VMS).docx'
        elif ais_len > 0 or vms_len > 0:
            if ais_len > 0 and vms_len == 0:
                tpl_path = f'{tpl_path}\\TB IUU TEMPLATE (AIS).docx' 
            elif ais_len == 0 and vms_len > 0:
                tpl_path = f'{tpl_path}\\TB IUU TEMPLATE (VMS).docx'
        else:
            tpl_path = f'{tpl_path}\\TB IUU TEMPLATE (No AIS and VMS).docx'
        
    else:
        print ('- Tidak ada data kapal')

        echo_text = '0'
        ais_text = '0'
        vms_text = '0'
        non_text = '0'
        ais_columns = []
        ais_rows = []
        vms_columns = []
        vms_rows = []
        
        tpl_path = f'{tpl_path}\\TB IUU TEMPLATE (No Ship).docx'   
    
    tpl = DocxTemplate(tpl_path)

    if len(layout_list) > 0:
        print ('- Ada layout')
        image = InlineImage(tpl, layout_list[0], width=Mm(163.5), height=Mm(115.6))
    else:
        print ('- Tidak ada layout')
        image = 'Tidak ada layout peta'
    
    context = {'image': image,
               'location': location,
               'radar': radar,
               'date': date,
               'time': time,
               'echo': echo_text,
               'ais': ais_text,
               'vms': vms_text,
               'non': non_text,
               'ship_labels': ship_columns, 
               'ship_contents': ship_rows,
               'ais_labels': ais_columns,
               'ais_contents': ais_rows,
               'vms_labels': vms_columns,
               'vms_contents': vms_rows,}

else:
    output_tb = f"TB OILSPILL_{local_datetime} {wil.upper()}.docx"
    
    oil_list = glob.glob(f'{data_folder}\\*OIL.shp')
    layout_list = glob.glob(f'{layout_basepath}\*{local_datetime}*oils.png')

    if len(oil_list) > 0:
        print ('- Ada data tumpahan minyak')
    else:
        print ('- Tidak ada data tumpahan minyak')


tpl.render(context)
tpl.save(f'{tboutput_path}\\{output_tb}')

print ('TB telah dibuat')

#exit QGIS application
qgs.exitQgis()
