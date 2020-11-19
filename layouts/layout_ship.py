import sys, os, glob

# source paths
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)
BASEMAP_PATH = f'{BASE_PATH}/1.basemaps'
BARATA_SHIP_PATH = f'{BASE_PATH}/7.barata_ship/output'
TEMPLATE_PATH = f'{SCRIPT_PATH}/templates'
QGIS_PATH = 'C:/OSGeo4W64/apps/qgis'
PROJECT_PATH = f'{TEMPLATE_PATH}/project/layout_ship.qgz'
WPP_PATH = f'{BASEMAP_PATH}/WPP_Full_PermenKP182014.shp'
OPENLAYOUT_PATH = f'{SCRIPT_PATH}/utils/open_layout.py'
QGIS_BAT = 'C:/OSGeo4W64/bin/qgis.bat'

sys.path.append(SCRIPT_PATH)

from barata.barata_layout import (
    QgsApp,
    QgsProc,
    Project,
    FileDialog,
    DataList,
    RasterLayer,
    LayerExtent,
    WindLayer,
    WPPLayer,
    ShipLayer,
    LoadLayer,
    DataNumbers,
    Layout,
)
from utils import read_kml, vms_correlation
from info.radar_info import RadarInfo
from info import vessel_info

# set QGIS application path and initialize it
qgs_app = QgsApp().initialize()
qgs_app.initQgis()

# QgsProc().initialize_processing()

# define project type and remove previous layer
project_layout = Project(PROJECT_PATH)
project_layout.remove_layer_panel()
project_layout.remove_layer_history()
project_type = project_layout.get_project_type()

# define method
method = sys.argv[-1]

# input directory path
print()
data_folder = FileDialog(BASE_PATH, method=method).open()

print('\nSumber data:')
print(data_folder)

# define list of data based on data folder
data_list = DataList(data_folder)
raster_list = data_list.get_raster_list()
wind_list = data_list.get_wind_list()
ship_list = data_list.get_ship_list()

OUTPUT_FOLDER = os.path.dirname(raster_list[-1])

print('\nKetersediaan data:')
if len(raster_list) > 0:
    print('- Ada data raster')
else:
    print('- Tidak ada data raster')
if len(wind_list) > 0:
    print('- Ada data angin')
else:
    print('- Tidak ada data angin')
if len(ship_list) > 0:
    print('- Ada data kapal')
else:
    print('- Tidak ada data kapal')

print('\n')

# load raster layer and get raster info
if len(raster_list) > 0:
    rasterlayer_list = RasterLayer(raster_list).get_raster_layer()
    rasterbasename_list = RasterLayer(raster_list).get_raster_basename()
    raster_extent = LayerExtent(rasterlayer_list).get_extent()

    for rasterlayer in rasterlayer_list:
        load_raster = LoadLayer(project_layout, rasterlayer)
        load_raster.add_raster_to_map()

    # get radar info from raster filename
    wil = os.path.basename(OUTPUT_FOLDER)[:-16]
    radar_info_list = []
    for rasterbasename in rasterbasename_list:
        radar_info = RadarInfo(rasterbasename)
        radar_info_list.append(radar_info)
    
    local = radar_info.local

    # define layout method based on data length
    if len(raster_list) == 1:
        method = 'satu'
    else:
        method = 'gabungan'

# set raster extent
xmin = raster_extent.xMinimum()
xmax = raster_extent.xMaximum()
ymin = raster_extent.yMinimum()
ymax = raster_extent.yMaximum()

# load wind data and get wind range and direction
if len(wind_list) > 0:
    wind_layer = WindLayer(wind_list)
    wind_range = wind_layer.get_wind_range()
    wind_direction = wind_layer.get_wind_direction()

# load wpp data and get WPP area which is overlaid within raster
wpp_extent = f'{xmin}, {xmax}, {ymin}, {ymax}'
wpp_layer = WPPLayer(WPP_PATH, wpp_extent, output_dir=OUTPUT_FOLDER)
wpp_area = wpp_layer.wpp_area

# define layer name
if method == 'satu':
    layer_name = f'{wil}_{local}_{project_type}'
else:
    layer_name = f'{wil}_{local[:-2]}_{project_type}'

# load data layer based on project type and setup the layout
if len(ship_list) > 0:
    # define transmitted layer name and ship csv path
    trmlayer_name = f'{layer_name[:-4]}AIS/VMS'
    ship_geo_path = f'{OUTPUT_FOLDER}/{layer_name}.geojson'
    ship_csv_path = f'{OUTPUT_FOLDER}/{layer_name}.csv'

    # define path of ship template
    ship_template = f'{TEMPLATE_PATH}/layer/ship_size_color_layer_template.qml'
    trm_template = f'{TEMPLATE_PATH}/layer/ais_vms_layer_template.qml'

    print('\nMendapatkan informasi asosiasi dengan AIS dan VMS...\n')
    for ship_path in ship_list:
        # get AIS_MMSI information on KML file
        read_kml.AIS(os.path.dirname(ship_path))

        # execute VMS correlation
        vms_correlation.correlation(os.path.dirname(ship_path))

    # define correlated VMS availability
    vms_list = []
    for raster_path in raster_list:
        vms_ff = os.path.dirname(raster_path)[-15:].replace('_', '')
        vms_path = glob.glob(f'{BARATA_SHIP_PATH}/{vms_ff}*/*.shp')
        if len(vms_path) > 0:
            vms_list.append(vms_path[0])

    # get transmitted layer of ship data
    if len(vms_list) > 0:
        ship = ShipLayer(ship_list, vms_list)
    else:
        ship = ShipLayer(ship_list)
    
    ship.export_ship_to_csv(ship_csv_path)
    ship.export_ship_to_geojson(ship_geo_path)
    ship_layer = ship.get_ship_layer(ship_geo_path, layer_name)
    ship2_layer = ship.get_ship_layer(ship_geo_path, trmlayer_name)

    # get ship elements and feature number
    print("\nMenghitung jumlah kapal...\n")
    data_numbers = DataNumbers(ship_csv_path)
    ship_numbers = data_numbers.get_ship_numbers()
    feat_numbers = data_numbers.get_feature_count()

    # load two ship layers to project
    load_ship = LoadLayer(project_layout, ship_layer, ship_template)
    load_ship2 = LoadLayer(project_layout, ship2_layer, trm_template)
    load_ship.add_vector_to_map()
    load_ship2.add_vector_to_map()

    # overlay wpp layer and ship extent
    ship_rect = ship_layer.extent()
    ship_xmin = ship_rect.xMinimum()
    ship_xmax = ship_rect.xMaximum()
    ship_ymin = ship_rect.yMinimum()
    ship_ymax = ship_rect.yMaximum()
    ship_extent = f'{ship_xmin}, {ship_xmax}, {ship_ymin}, {ship_ymax}'
    wpp_layer = WPPLayer(
        WPP_PATH,
        ship_extent,
        layer_name='wppship_layer.gpkg',
        output_dir=OUTPUT_FOLDER
    )

else:
    feat_numbers = 0
    ship_csv_path = None
    ship_numbers = DataNumbers(ship_csv_path).getShipElements()

# define layout manager
layout_manager = Layout(project_type, method, feat_numbers, wil, radar_info_list, wpp_layer, wind_layer)

# insert ship elements to layout
layout_manager.insertShipElements(ship_numbers)

# set and insert attributes to layout
layout_manager.setMap(raster_extent)
layout_manager.insertTitleText()
layout_manager.insertWindText()
layout_manager.insertSourceText()
layout_manager.setLayoutName(layer_name)

# save project
outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
project_layout.save_project(outputproj_path)

print('\nLayout telah dibuat\n')

if ship_csv_path is not None:
    # get vessel info
    print('-----------------------------------------')
    print('\nMendapatkan informasi vessel...\n')
    ais_info = vessel_info.get_ais_info(ship_csv_path)
    vms_info = vessel_info.get_vms_info(ship_csv_path)
    print('-----------------------------------------')

print('\nSelesai')

# exit QGIS application
qgs_app.exitQgis()

# remove 'temp' directory
os.chdir(OUTPUT_FOLDER)
if os.path.exists('temp'):
    os.system('rmdir /s /q temp')

# open current project using command line
os.chdir(SCRIPT_PATH)
os.system(f'{QGIS_BAT} --project {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {OPENLAYOUT_PATH}')

print('\nMembuka project layout...')