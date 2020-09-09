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
    Project,
    FileDialog,
    DataList,
    RasterLayer,
    LayerExtent,
    WindData,
    WPPData,
    ShipData,
    LoadLayer,
    DataElements,
    Layout,
)
from utils import read_kml, vms_correlation
from info.radar_info import RadarInfo
from info import vessel_info

# set QGIS application path and initialize it
qgs_app = QgsApp(QGIS_PATH)
qgs_app.start()

# define project type and remove previous layer
project_layout = Project(PROJECT_PATH)
project_layout.removeLayerPanel()
project_layout.removeLayerHistory()
project_type = project_layout.getProjectType()

print(f'\nTipe project: {project_type}')

# input directory path
while True:
    option = input('Pilih metode layout (satu[1] atau gabungan[2]): ')
    if option == '1' or option.lower() == 'satu':
        method = 'satu'
        break
    elif option == '2' or option.lower() == 'gabungan':
        method = 'gabungan'
        break
    else:
        print('Metode layout yang Anda masukkan tidak sesuai')

print(f'Metode layout: {method}')

data_folder = FileDialog(BASE_PATH, method=method).open()

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
        load_raster = LoadLayer(project_layout, rasterlayer)
        load_raster.addRasterToMap()

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
    windgdf = wind_data.getGeoDataFrame()
else:
    print('- Tidak ada data angin')
    wind_data = None

# load wpp data and get WPP area which is overlaid within raster
wpp_data = WPPData(WPP_PATH, raster_extent)
wpp_area = wpp_data.wpp_area

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
    shipgdf_path = f'{OUTPUT_FOLDER}/{layer_name}.geojson'
    shipdf_path = f'{OUTPUT_FOLDER}/{layer_name}.csv'

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
        ship_data = ShipData(ship_list, vms_list)
    else:
        ship_data = ShipData(ship_list)
    ship_gdf = ship_data.getShipGeoDataFrame()
    ship_gdf.to_file(shipgdf_path, driver='GeoJSON')
    ship_df = ship_data.getShipDataFrame()
    ship_df.to_csv(shipdf_path)
    ship_layer = ship_data.getLayer(shipgdf_path, layer_name)
    ship2_layer = ship_data.getLayer(shipgdf_path, trmlayer_name)

    # get ship elements and feature number
    print("\nMenghitung jumlah kapal...\n")
    ship_elements = DataElements(ship_gdf).getShipElements()
    feat_number = len(ship_gdf)

    # load two ship layers to project
    load_ship = LoadLayer(project_layout, ship_layer, ship_template)
    load_ship2 = LoadLayer(project_layout, ship2_layer, trm_template)
    load_ship.addVectorToMap()
    load_ship2.addVectorToMap()

    # overlay wpp layer and ship extent
    ship_extent = ship_gdf.total_bounds
    wpp_data = WPPData(WPP_PATH, ship_extent)

else:
    print('- Tidak ada data kapal')

    feat_number = 0
    ship_gdf = None
    shipdf_path = None
    ship_elements = DataElements(ship_gdf).getShipElements()

# define layout manager
layout_manager = Layout(project_type, method, feat_number, wil, radar_info_list, wpp_data, wind_data)

# insert ship elements to layout
layout_manager.insertShipElements(ship_elements)

# set and insert attributes to layout
layout_manager.setMap(raster_extent)
layout_manager.insertTitleText()
layout_manager.insertWindText()
layout_manager.insertSourceText()
layout_manager.setLayoutName(layer_name)

# save project
outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
project_layout.saveProject(outputproj_path)

print('\nLayout telah dibuat\n')

if shipdf_path is not None:
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

# open current project using command line
os.chdir(SCRIPT_PATH)
os.system(f'{QGIS_BAT} --project {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {OPENLAYOUT_PATH}')

print('\nMembuka project layout...')
