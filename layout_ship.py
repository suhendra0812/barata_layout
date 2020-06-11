import sys
import os
from barata_layout import *
import read_kml
from radar_info import RadarInfo
import vessel_info

# set QGIS application path and initialize it
qgs_path = 'C:\\OSGeo4W64\\apps\\qgis'
qgs_app = QgsApp(qgs_path)
qgs_app.start()

# source paths
BASE_PATH = "D:\\BARATA"
BASEMAP_PATH = f'{BASE_PATH}\\1.basemaps'
BARATA_SHIP_PATH = f'{BASE_PATH}\\7.barata_ship\\output'
TEMPLATE_PATH = 'templates'

# define project type and remove previous layer
project_path = f'{TEMPLATE_PATH}\\project\\layout_ship.qgz'

project_layout = Project(project_path)
project_layout.removeLayerPanel()
project_layout.removeLayerHistory()
project_type = project_layout.getProjectType()

print(f'\nTipe project: {project_type}')

# define group
basemap_group = project_layout.getBasemapGroup()
data_group = project_layout.getDataGroup()

# input directory path
data_folder = FileDialog(BASE_PATH).open()

print('\nSumber data:')
print(data_folder)

# define list of data based on data folder
data_list = DataList(data_folder)
raster_list = data_list.getRasterList()
wind_list = data_list.getWindList()

OUTPUT_FOLDER = os.path.dirname(raster_list[-1])

print('\nKetersediaan data:')
# load raster layer and get raster info
if len(raster_list) > 0:
    print('- Ada data raster')
    rasterlayer_list = RasterLayer(raster_list).getRasterLayer()
    rasterbasename_list = RasterLayer(raster_list).getRasterBasename()
    raster_extent = LayerExtent(rasterlayer_list).getExtent()

    for rasterlayer in rasterlayer_list:
        LoadRasterLayer(rasterlayer, basemap_group)

    # get radar info from raster filename
    wil = os.path.basename(OUTPUT_FOLDER)[:-16]
    radar_info_list = []
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

    # define layout method based on data length
    if len(raster_list) == 1:
        method = 'satu'
    else:
        method = 'gabungan'
else:
    print('- Tidak ada data raster')

# load wind data and get wind range and direction
if len(wind_list) > 0:
    print('- Ada data angin')
    wind_data = WindData(wind_list)
    wind_range = wind_data.windrange
    wind_direction = wind_data.dire
    windgdf = wind_data.getWindGeoDataFrame()
else:
    print('- Tidak ada data angin')
    wind_data = None

# load wpp data and get WPP area which is overlaid within raster
wpp_path = f'{BASEMAP_PATH}\\WPP_Full_PermenKP182014.shp'
wpp_layer = WPPLayer(wpp_path, raster_extent)
wpp_area = wpp_layer.wpp_area

# define layer name
if method == 'satu':
    layer_name = f'{wil}_{local}_{project_type}'
else:
    layer_name = f'{wil}_{local[:-2]}_{project_type}'

# load data layer based on project type and setup the layout
ship_list = data_list.getShipList()
if len(ship_list) > 0:
    print('- Ada data kapal')

    # define transmitted layer name and ship csv path
    trmlayer_name = f'{layer_name[:-4]}AIS/VMS'
    shipdf_path = f'{OUTPUT_FOLDER}\\{layer_name}.csv'

    # define path of ship template
    ship_template = f'{TEMPLATE_PATH}\\layer\\ship_size_color_layer_template.qml'
    trm_template = f'{TEMPLATE_PATH}\\layer\\ais_vms_layer_template.qml'

    for ship_path in ship_list:
        # get AIS_MMSI information on KML file
        read_kml.AIS(os.path.dirname(ship_path))

    # define correlated VMS availability
    vms_list = []
    for raster_path in raster_list:
        vms_ff = os.path.dirname(raster_path)[-15:].replace('_', '')
        vms_path = glob.glob(f'{BARATA_SHIP_PATH}\\{vms_ff}*\\*.shp')
        if len(vms_path) > 0:
            vms_list.append(vms_path[0])
        # else:
        #     corshipPath = os.path.dirname(raster_path).replace('2.seonse_outputs','12.correlated_ship')
        #     vms_path = glob.glob(f'{corshipPath}\\*CORRELATED.shp')
        #     if len(vms_path) > 0:
        #         vms_list.append(vms_path[0])

    # get list of features and attributes and feature extent
    shipfeat_list = DataLayer(ship_list).getFeatList()
    shipattr_list = DataLayer(ship_list).getAttrList()
    ship_extent = DataLayer(ship_list).getFeatExtent()

    # get aggregation and transmitted layer of ship data
    
    # agg_shiplayer = AggregationLayer(shipfeat_list, shipattr_list, layer_name).getAggLayer()
    # agg_shiplayer = AggregationLayerV2(ship_list).getAggLayer(layer_name)
    # trmlayer = TransmittedLayer(shipfeat_list, shipattr_list, vms_list, trmlayer_name).getTrmLayer()
    trmlayer = TransmittedLayerV2(ship_list, vms_list).getTrmLayer(trmlayer_name)

    # export layer to csv
    ExportLayer(trmlayer, shipdf_path).to_csv()

    # get ship elements and feature number
    ship_elements = DataElements(project_type, shipdf_path).getShipElements()
    feat_number = len(shipfeat_list)

    # get delimited layer of ship data
    ship_layer = DelimitedLayer(shipdf_path, layer_name).getDelimitedLayer()
    ship2_layer = DelimitedLayer(shipdf_path, trmlayer_name).getDelimitedLayer()

    # load two ship layers to project
    LoadVectorLayer(ship_layer, data_group, ship_template)
    LoadVectorLayer(ship2_layer, data_group, trm_template)

    # overlay wpp layer and ship extent
    wpp_layer = WPPLayer(wpp_path, ship_extent)

else:
    print('- Tidak ada data kapal')

    feat_number = 0
    shipdf_path = None
    ship_elements = DataElements(project_type, shipdf_path).getShipElements()

# define layout manager
layout_manager = Layout(project_type, method, feat_number, wil, radar_info_list, wpp_layer, wind_data)

# insert ship elements to layout
layout_manager.insertShipElements(ship_elements)

# set and insert attributes to layout
layout_manager.setMap(raster_extent)
layout_manager.insertTitleText()
layout_manager.insertWindText()
layout_manager.insertSourceText()
layout_manager.setLayoutName(layer_name)

# save project
outputproj_path = f'{OUTPUT_FOLDER}\\{layer_name}.qgz'
project_layout.saveProject(outputproj_path)

print('\nLayout telah dibuat\n')

# get vessel info
print('======================================')
print('\nMendapatkan informasi vessel...\n')
ais_info = vessel_info.get_ais_info(shipdf_path)
vms_info = vessel_info.get_vms_info(shipdf_path)
print('======================================')

print('\nSelesai')

# exit QGIS application
qgs_app.quit()

# set raster extent
xmin = raster_extent.xMinimum()
xmax = raster_extent.xMaximum()
ymin = raster_extent.yMinimum()
ymax = raster_extent.yMaximum()

# define open layout script path
OPENLAYOUT_SCRIPT = 'open_layout.py'

# open current project using command line
os.system(f'qgis --projectfile {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {OPENLAYOUT_SCRIPT}')

print('\nMembuka project layout...')
