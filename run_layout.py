import sys, os
from qgis.core import QgsApplication

#set QGIS application path and initialize it
QgsApplication.setPrefixPath(r'C:\OSGeo4W64\apps\qgis', True)
qgs = QgsApplication([], False)
qgs.initQgis()

#source paths
base_path = "D:\\BARATA"
basemap_path = f'{base_path}\\1.basemaps'
template_path = f'{base_path}\\14.templates'
rdrvms_path = f'{base_path}\\11.radar&vms_outputs'
script_path = f'{base_path}\\9.barata_layout'

#sys.path.append(script_path)
from barata_layout import *
import read_kml

#define project type and remove previous layer
option = input("\nPilih tipe project (ship/oils): ")
if option == "ship":
    project_path = f'{base_path}\\layout_ship.qgz'
else:
    project_path = f'{base_path}\\layout_oils.qgz'
    

project_layout = Project(project_path)
project_layout.removeLayerPanel()
project_layout.removeLayerHistory()
project_type = project_layout.getProjectType()

print (f'\nTipe project: {project_type}')

#define group
basemap_group = project_layout.getBasemapGroup()
data_group = project_layout.getDataGroup()

#input directory path based on defined method
data_folder = QFileDialog.getExistingDirectory(None, 'Select Data Directory', f'{base_path}\\2.seonse_outputs')[:-4] + '*'

print ('\nSumber data:')
print (data_folder)

#define list of data based on data folder
data_list = DataList(data_folder)
raster_list = data_list.getRasterList()
wind_list = data_list.getWindList()

output_folder = os.path.dirname(raster_list[-1])

print ('\nKetersediaan data:')
#load raster layer and get raster info
if len(raster_list) > 0:
    print ('- Ada data raster')
    rasterlayer_list = RasterLayer(raster_list).getRasterLayer()
    rasterbasename_list = RasterLayer(raster_list).getRasterBasename()
    raster_extent = RasterLayer(raster_list).getRasterExtent()

    radar_info_list = []
    for rasterlayer in rasterlayer_list:
        LoadRasterLayer(rasterlayer, basemap_group)

    #get radar info from raster filename
    wil = os.path.basename(output_folder)[:-16]
    for rasterbasename in rasterbasename_list:
        radar_info = RadarInfo(rasterbasename)
        radar_info_list.append(radar_info)

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
    
    #define metode layout berdasarkan jumlah data
    if len(raster_list) == 1:
        method = 'satu'
    else:
        method = 'gabungan'
else:
    print ('- Tidak ada data raster')

#load wind data and get wind range and direction
if len(wind_list) > 0:
    print ('- Ada data angin')
    wind_data = WindData(wind_list)
    wind_range = wind_data.windrange
    wind_direction = wind_data.dire
    windgdf = wind_data.getWindGeoDataFrame()
else:
    print ('- Tidak ada data angin')
    wind_range=wind_direction= 'n/a'

#load wpp data and get WPP area which is overlaid within raster
wpp_path = f'{basemap_path}\\wpp_juni_2011_fix.shp'
wpp_layer = WPPLayer(wpp_path, raster_extent)
wpp_area = wpp_layer.wpp_area

#define layer name
if method == 'satu':
    layer_name = f'{wil}_{local}_{project_type}'
else:
    layer_name = f'{wil}_{local[:-2]}_{project_type}'

#load data layer based on project type and setup the layout            
if project_type == 'ship':
    ship_list = data_list.getShipList()
    if len(ship_list) > 0:
        print ('- Ada data kapal')

        #define transmitted layer name and ship csv path
        trmlayer_name = f'{layer_name[:-4]}_AIS/VMS'
        shipdf_path = f'{output_folder}\\{layer_name}.csv'
        
        #define path of ship template
        ship_template = f'{template_path}\\template_ship_size_color_layer_2.qml'
        trm_template = f'{template_path}\\template_ais_vms_layer_2.qml'
        
        for ship_path in ship_list:
            #get AIS_MMSI information on KML file
            read_kml.AIS(os.path.dirname(ship_path))
        
        #define correlated VMS availability
        vms_list = []
        for raster_path in raster_list:
            vms_ff = os.path.dirname(raster_path)[-15:].replace('_','')
            vms_path = glob.glob(f'{rdrvms_path}\\{vms_ff}*\\*.shp')
            if len(vms_path) > 0:
                vms_list.append(vms_path[0])
            else:
                corshipPath = os.path.dirname(raster_path).replace('2.seonse_outputs','13.correlated_ship')
                vms_path = glob.glob(f'{corshipPath}\\*CORRELATED.shp')
                if len(vms_path) > 0:
                    vms_list.append(vms_path[0])

        #get list of features and attributes and feature extent    
        shipfeat_list = DataLayer(ship_list).getFeatList()
        shipattr_list = DataLayer(ship_list).getAttrList()
        ship_extent = DataLayer(ship_list).getFeatExtent()
            
        #get aggregation and transmitted layer of ship data
        agg_shiplayer = AggregationLayer(shipfeat_list, shipattr_list, layer_name).getAggLayer()
        trmlayer = TransmittedLayer(shipfeat_list, shipattr_list, vms_list, trmlayer_name).getTrmLayer()

        #export layer to csv
        ExportLayer(trmlayer, shipdf_path).to_csv()
        
        #get ship elements and feature number
        ship_elements = DataElements(project_type, shipdf_path).getShipElements()
        feat_number = len(shipfeat_list)
        
        #get delimited layer of ship data
        ship_layer = DelimitedLayer(shipdf_path, layer_name).getDelimitedLayer()
        ship2_layer = DelimitedLayer(shipdf_path, trmlayer_name).getDelimitedLayer()
        
        #load two ship layers to project
        LoadVectorLayer(ship_layer, data_group, ship_template)
        LoadVectorLayer(ship2_layer, data_group, trm_template)
        
        #overlay wpp layer and ship extent
        wpp_layer = WPPLayer(wpp_path, ship_extent)
    
    else:
        print ('- Tidak ada data kapal')

        feat_number = 0
        shipdf_path = None
        ship_elements = DataElements(project_type, shipdf_path).getShipElements()
        
    #define layout manager
    layout_manager = Layout(project_type, method, feat_number, wil, radar_info_list, wpp_layer, wind_data)

    #insert ship elements to layout
    layout_manager.insertShipElements(ship_elements)
  
else:
    oil_list = data_list.getOilList()
    if len(oil_list) > 0:
        print ('- Ada data tumpahan minyak')

        #define name and path
        oilgdf_path = f'{output_folder}\\{layer_name}.shp'

        #define path of oil template
        oil_template = f'{template_path}\\template_level_oils_layer.qml'
        
        #get list of features and attributes, geodataframe and feature extent
        oilfeat_list = DataLayer(oil_list).getFeatList()
        oilattr_list = DataLayer(oil_list).getAttrList()
        oilgdf = DataLayer(oil_list).getGeoDataFrame()
        oil_extent = DataLayer(oil_list).getFeatExtent()
        
        #get aggregation and transmitted layer of oil data    
        agg_oillayer = AggregationLayer(oilfeat_list, oilattr_list, layer_name).getAggLayer()
        wind_oillayer = WindOilLayer(oilgdf, windgdf, agg_oillayer).getWindOilLayer()
        
        #export layer to shapefile
        ExportLayer(wind_oillayer, oilgdf_path).to_shp()
        
        #get oil elements and feature number
        oil_elements = DataElements(project_type, oilgdf_path).getOilElements()
        feat_number = len(oilfeat_list)
        
        #get oil layer of oil data
        oil_layer = DataLayer([oilgdf_path]).getLayerList()[0]
        
        #load oil layer to project
        LoadVectorLayer(oil_layer, data_group, oil_template)
        
        #overlay wpp layer and oil extent
        wpp_layer = WPPLayer(wpp_path, oil_extent)
        
        #get value of oil area
        area = sum([i for i in oilgdf['AREA_KM']])
        area_txt = f'{str(round(area, 2))} km\u00B2'
            
    else:
        print ('- Tidak ada data tumpahan minyak')
        feat_number = 0
        
        oildf_path = None
        oil_elements = DataElements(project_type, oildf_path).getOilElements()
	
    #define layout manager
    layout_manager = Layout(project_type, method, feat_number, wil, radar_info_list, wpp_layer, wind_data)
    
    #get layout list
    layout_list = layout_manager.getLayoutList()
    
    #set atlas and oil area text to specific layout
    for layout in layout_list:
        if layout[0] == 1 or layout[0] == 3:
            layout_manager.setAtlas(oil_layer)
        elif layout[0] == 2:
            layout_manager.setOilAreaText(area_txt)
        else:
            pass

#set and insert attribute to layout   
layout_manager.setMap(raster_extent)
layout_manager.insertTitle()
layout_manager.insertWindText()
layout_manager.insertSourceText()
layout_manager.setLayoutName(layer_name) 

#save project
outputproj_path = f'{output_folder}\\{layer_name}.qgz'
project_layout.saveProject(outputproj_path)
    
print ('\nLayout telah dibuat')
print ('\nSelesai')

#exit QGIS application
qgs.exitQgis()

#set raster extent
xmin = raster_extent.xMinimum()
xmax = raster_extent.xMaximum()
ymin = raster_extent.yMinimum()
ymax = raster_extent.yMaximum()

#define open layout script path
openlayout_script = f'{script_path}\\open_layout.py'

#open current project using command line
os.system(f'qgis --projectfile {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {openlayout_script}')

print ('\nMembuka project layout...')
