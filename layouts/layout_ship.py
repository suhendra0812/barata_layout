import sys, os, glob
import numpy as np
import pandas as pd
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, "id_ID")

from qgis.core import (
    edit,
    QgsApplication,
    QgsProcessingFeedback,
    QgsProcessing,
    QgsProject,
    QgsRasterLayer,
    QgsRectangle,
    QgsRasterRange,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransformContext,
    QgsField,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsLayerTreeLayer,
    QgsLayoutItemLabel,
    QgsLayoutItemMap,
    QgsLayoutItemMapOverview
)
from qgis.gui import QgsMapCanvas
from qgis.analysis import QgsNativeAlgorithms
from PyQt5.QtCore import QFileInfo, QVariant
from PyQt5.QtWidgets import QFileDialog
import sip

# source paths
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)
BASEMAP_PATH = os.path.join(BASE_PATH, '1.basemaps')
BARATA_SHIP_PATH = os.path.join(BASE_PATH, '7.barata_ship/output')
TEMPLATE_PATH = os.path.join(SCRIPT_PATH, 'templates')
QGIS_PATH = 'C:/OSGeo4W64/apps/qgis'
PLUGINS_PATH = os.path.join(QGIS_PATH, 'python', 'plugins')
PROJECT_PATH = os.path.join(TEMPLATE_PATH, 'project', 'layout_ship.qgz')
WPP_PATH = os.path.join(BASEMAP_PATH, 'WPP_Full_PermenKP182014.shp')
OPENLAYOUT_PATH = os.path.join(SCRIPT_PATH, 'utils', 'open_layout.py')
QGIS_BAT = 'C:/OSGeo4W64/bin/qgis.bat'

sys.path.append(SCRIPT_PATH)

from utils import read_kml, vms_correlation
from info.radar_info import RadarInfo
from info import vessel_info

# set QGIS application path and initialize it
QgsApplication.setPrefixPath(QGIS_PATH, True)
qgs = QgsApplication([], False)
qgs.initQgis()

# set QGIS Processing plugins and initialize it
sys.path.append(PLUGINS_PATH)
import processing
from processing.core.Processing import Processing
Processing.initialize()
qgs.processingRegistry().addProvider(QgsNativeAlgorithms())

def run_processing(algorithm, params):
    params = params
    feedback = QgsProcessingFeedback()
    output = processing.run(algorithm, params, feedback=feedback)
    
    if params['OUTPUT'] != QgsProcessing.TEMPORARY_OUTPUT:
        layer_path = output['OUTPUT']
        layer_name = QFileInfo(layer_path).baseName()
        layer = QgsVectorLayer(layer_path, layer_name)
    else:
        layer = output['OUTPUT']
    
    return layer

def merge_vector_layer(layer_list, epsg_code=4326, output_path=None):
    algorithm = 'native:mergevectorlayers'
    if output_path == None:
        output_path = QgsProcessing.TEMPORARY_OUTPUT
    params = {
        'LAYERS': layer_list,
        'CRS': QgsCoordinateReferenceSystem(f'EPSG:{epsg_code}'),
        'OUTPUT': output_path
    }
    output = run_processing(algorithm, params)
    return output

def extract_by_extent(input_layer, extent, output_path=None):
    algorithm = 'native:extractbyextent'
    if output_path == None:
        output_path = QgsProcessing.TEMPORARY_OUTPUT
    params = {
        'INPUT': input_layer,
        'EXTENT': extent,
        'OUTPUT': output_path
    }
    output = run_processing(algorithm, params)
    return output

def join_attributes_by_location(base_layer, join_layer, join_fields=None, output_path=None):
    algorithm = 'native:joinattributesbylocation'
    if output_path == None:
        output_path = QgsProcessing.TEMPORARY_OUTPUT
    params = {
        'INPUT': base_layer,
        'JOIN': join_layer,
        'JOIN_FIELDS': join_fields,
        'METHOD': 0,
        'OUTPUT': output_path
    }
    output = run_processing(algorithm, params)
    return output

def wind_angle(x, y):
    angle = np.arctan2(y, x)*(180/np.pi)+180
    return angle

def wind_direction(angle):
    # define mean wind direction
    if angle < 180:
        wind_ang = angle + 180
    elif angle > 180:
        wind_ang = angle - 180

    # define wind direction value to wind direction name
    if wind_ang > 22.5 and wind_ang <= 67.5:
        wind_dir = "Timur Laut"
    elif wind_ang > 67.5 and wind_ang <= 112.5:
        wind_dir = "Timur"
    elif wind_ang > 112.5 and wind_ang <= 157.5:
        wind_dir = "Tenggara"
    elif wind_ang > 157.5 and wind_ang <= 202.5:
        wind_dir = "Selatan"
    elif wind_ang > 202.5 and wind_ang <= 247.5:
        wind_dir = "Barat Daya"
    elif wind_ang > 247.5 and wind_ang <= 292.5:
        wind_dir = "Barat"
    elif wind_ang > 292.5 and wind_ang <= 337.5:
        wind_dir = "Barat Laut"
    else:
        wind_dir = "Utara"
    return wind_dir

def get_wind_range(wind_layer):
    wind_sp = [feat['speed'] for feat in wind_layer.getFeatures()]
    wsp_min = round(min(wind_sp), 2)
    wsp_max = round(max(wind_sp), 2)
    return wsp_min, wsp_max

def get_wind_direction(wind_layer):
    wind_ang = [feat['angle'] for feat in wind_layer.getFeatures()]
    ang_mean = np.mean(wind_ang)
    wind_dir = wind_direction(ang_mean)
    return wind_dir

def get_wpp_area(wpp_layer):
    wpp_list = [feat['WPP'][-3:] for feat in wpp_layer.getFeatures()]

    if len(wpp_list) == 1:
        wpp_area = f'WPP NRI {wpp_list[0]}'
    elif len(wpp_list) == 2:
        wpp_area = f'WPP NRI {wpp_list[0]} & {wpp_list[1]}'
    elif len(wpp_list) > 2:
        wpp_area = f'WPP NRI {wpp_list[0]}, {wpp_list[1]} & {wpp_list[2]}'
    else:
        wpp_area = 'LUAR INDONESIA'
    
    return wpp_area   

def export_vector_layer(vector_layer, output_path, driver='ESRI Shapefile', column_dict=None):
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = driver

    QgsVectorFileWriter.writeAsVectorFormatV2(
        vector_layer,
        output_path,
        QgsCoordinateTransformContext(),
        options
    )

    if driver == 'CSV':
        df = pd.read_csv(output_path)
        old_column_list = list(column_dict.keys())
        df = df[old_column_list]
        df.rename(
            columns=column_dict,
            inplace=True
        )

        df.index += 1
        df.index.name = 'No.'

        df.to_csv(output_path)

def get_ship_numbers(ship_csv_path=None):
    if ship_csv_path != None:
        ship_df = pd.read_csv(ship_csv_path)
        # get echo, AIS and VMS data
        vms = ship_df['Asosiasi (AIS/VMS)'] == 'VMS'
        ais = ship_df['Asosiasi (AIS/VMS)'] == 'AIS'

        fv = ship_df[vms]
        fa = ship_df[ais]
        fu = ship_df[~vms & ~ais]

        # ship data selection based on size
        se = ship_df['Panjang (m)']
        su = fu['Panjang (m)']
        sv = fv['Panjang (m)']
        sa = fa['Panjang (m)']

        # untransmitted ship selection by 50 size scale
        u1 = fu[(su <= 50)]  # kapal ikan
        u2 = fu[(su > 50)]  # bukan kapal ikan

        # AIS ship selection by 50 size scale
        a1 = fa[(sa <= 50)]  # kapal ikan
        a2 = fa[(sa > 50)]  # bukan kapal ikan

        # ship classification by 10 size scale
        e0 = ship_df[(se <= 10)]
        e10 = ship_df[(se > 10) & (se <= 20)]
        e20 = ship_df[(se > 20) & (se <= 30)]
        e30 = ship_df[(se > 30) & (se <= 40)]
        e40 = ship_df[(se > 40) & (se <= 50)]
        e50 = ship_df[(se > 50)]

        # define component of ship number
        k0 = str(len(e0))
        k1 = str(len(e10))
        k2 = str(len(e20))
        k3 = str(len(e30))
        k4 = str(len(e40))
        k5 = str(len(e50))

        # total of untransmitted ship
        k6 = str(len(fu))

        # VMS transmitted ship
        k11 = str(len(fv))

        # AIS transmitted ship for <=50 and >50
        k7 = str(len(a1))
        k8 = str(len(a2))

        # total of AIS transmitted ship
        k9 = str(len(fa))

        # total number of ship
        k10 = str(len(ship_df))

    else:
        k0 = k1 = k2 = k3 = k4 = k5 = k6 = k7 = k8 = k9 = k10 = k11 = '0'

    print(f"<10\tNon Transmitter\t\t\t= {k0}")
    print(f"20-30\tNon Transmitter\t\t\t= {k2}")
    print(f"30-40\tNon Transmitter\t\t\t= {k3}")
    print(f"10-20\tNon Transmitter\t\t\t= {k1}")
    print(f"40-50\tNon Transmitter\t\t\t= {k4}")
    print(f">50\tNon Transmitter\t\t\t= {k5}")
    print(f"\nKapal <=50 Bertransmitter AIS\t\t= {k7}")
    print(f"Kapal >50 Bertransmitter AIS\t\t= {k8}")
    print(f"\nJumlah Kapal Bertransmitter AIS\t\t= {k9}")
    print(f"Jumlah Kapal Bertransmitter VMS\t\t= {k11}")
    print(f"Jumlah Kapal Tidak Bertransmitter\t= {k6}")
    print(f"\nTotal jumlah kapal\t\t\t= {k10}")

    return [k0, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11]

def load_raster_layer(raster_layer, group):
    QgsProject.instance().addMapLayer(raster_layer, False)
    raster_layer.dataProvider().setNoDataValue(1, 0)
    raster_layer.dataProvider().setUserNoDataValue(1, [QgsRasterRange(0, 0)])
    group.insertChildNode(3, QgsLayerTreeLayer(raster_layer))

def load_vector_layer(vector_layer, template, group):
    QgsProject.instance().addMapLayer(vector_layer, False)
    group.addLayer(vector_layer)
    vector_layer.loadNamedStyle(template)
    QgsProject.instance().layerTreeRoot().findLayer(vector_layer).setCustomProperty("showFeatureCount", True)

def get_title_text(method, wpp_area, radar_info):
    if method == 'satu':
        periode_txt = datetime.strptime(radar_info.local, '%Y%m%d_%H%M%S').strftime('%d %B %Y PUKUL %H:%M:%S WIB')
    else:
        periode_txt = datetime.strptime(radar_info.local, '%Y%m%d_%H%M%S').strftime('%d %B %Y PUKUL %H:%M WIB')
    
    title_txt = f'PETA SEBARAN KAPAL DI PERAIRAN {wpp_area}\nPERIODE {periode_txt}'
    return title_txt

def get_wind_text(wind_range, wind_dir):
    if wind_range != None:
        wind_range = f"{' - '.join([str(i) for i in wind_range])} m/s"
    else:
        wind_range = 'n/a'
    
    if wind_dir == None:
        wind_dir = 'n/a'
        
    wind_txt = f'{wind_range}\n{wind_dir}'
    return wind_txt

def get_source_text(radar_info_list):
    radar_sourcetxt = ['Sumber:']
    for i, radar_info in enumerate(radar_info_list):
        mode_txt = radar_info.rdr_mode
        periode_txt = datetime.strptime(radar_info.utc, '%Y%m%d_%H%M%S').strftime('%Y-%m-%dT%H:%M:%S UTC')
        radar_txt = f'{i+1}. {mode_txt} ({periode_txt})'
        radar_sourcetxt.append(radar_txt)

    basemap_sourcetxt = f'{len(radar_info_list)+1}. Peta Rupabumi Digital Wilayah Indonesia BIG'
    radar_sourcetxt.append(basemap_sourcetxt)
    source_txt = '\n'.join(radar_sourcetxt)

    return source_txt

# define project type and remove previous layer
QgsProject.instance().read(PROJECT_PATH)
data_group = QgsProject.instance().layerTreeRoot().findGroups()[0]
basemap_group = QgsProject.instance().layerTreeRoot().findGroups()[1]
if len(data_group.findLayers()) > 0:
    for i in data_group.children():
        data_group.removeChildNode(i)

if len(basemap_group.findLayers()) > 3:
    raster_layer_remove = basemap_group.findLayers()[3:-1]
    for layer in raster_layer_remove:
        basemap_group.removeChildNode(layer)

project_path = QgsProject.instance().fileName()
project_basename = QFileInfo(project_path).baseName()
project_type = project_basename[-4:]

# define method
method = sys.argv[-1]

# input directory path
if method == 'satu':
    data_folder = QFileDialog.getExistingDirectory(
        None, 'Select Data Directory', BASE_PATH)
elif method == 'gabungan':
    data_folder = QFileDialog.getExistingDirectory(
        None, 'Select Data Directory', BASE_PATH)[:-4] + '*'

print('\nSumber data:')
print(data_folder)

# define list of data based on data folder
raster_list = glob.glob(f'{data_folder}/*.tif')
wind_list = glob.glob(f'{data_folder}/*Wind.gml')
ship_list = glob.glob(f'{data_folder}/*SHIP.shp')

OUTPUT_FOLDER = os.path.dirname(raster_list[-1])
TEMP_FOLDER = os.path.join(OUTPUT_FOLDER, 'temp')
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

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
    raster_basename_list = []
    raster_layer_list = []

    for raster_path in raster_list:
        rasterbasename = QFileInfo(raster_path).baseName()
        rasterlayer = QgsRasterLayer(raster_path, rasterbasename)
        if not rasterlayer.isValid():
            print("rasterlayer is not valid")

        raster_basename_list.append(rasterbasename)
        raster_layer_list.append(rasterlayer)
    
    # set up extent
    raster_extent = QgsRectangle()
    raster_extent.setMinimal()

    for raster_layer in raster_layer_list:
        # combine extent with raster layer extent
        raster_extent.combineExtentWith(raster_layer.extent())

    # set extent to canvas
    QgsMapCanvas().setExtent(raster_extent)
    QgsMapCanvas().refresh()

    for raster_layer in raster_layer_list:
        load_raster_layer(raster_layer, basemap_group)

    # get radar_info info from raster filename
    wil = os.path.basename(OUTPUT_FOLDER)[:-16]
    radar_info_list = []
    for raster_basename in raster_basename_list:
        radar_info = RadarInfo(raster_basename)
        radar_info_list.append(radar_info)
    
    local = radar_info.local

    # define layout method based on data length
    # if len(raster_list) == 1:
    #     method = 'satu'
    # else:
    #     method = 'gabungan'

# set raster extent
xmin = raster_extent.xMinimum()
xmax = raster_extent.xMaximum()
ymin = raster_extent.yMinimum()
ymax = raster_extent.yMaximum()

# load wind data and get wind range and direction
if len(wind_list) > 0:
    wind_layer = merge_vector_layer(wind_list)
    with edit(wind_layer):
        wind_layer.dataProvider().addAttributes(
            [
                QgsField("angle", QVariant.Double),
                QgsField("direction", QVariant.String),
            ]
        )
        wind_layer.updateFields()

        for feat in wind_layer.getFeatures():
            wind_ang = wind_angle(feat['zonalSpeed'], feat['meridionalSpeed'])
            wind_dir = wind_direction(wind_ang)
            feat['angle'] = float(wind_ang)
            feat['direction'] = str(wind_dir)
            wind_layer.updateFeature(feat)
    wind_range = get_wind_range(wind_layer)
    wind_dir = get_wind_direction(wind_layer)

# load wpp data and get WPP area which is overlaid within raster
wpp_extent = raster_extent
wpp_temp_path = os.path.join(TEMP_FOLDER, 'wpp_layer.gpkg')
wpp_layer = extract_by_extent(WPP_PATH, wpp_extent, output_path=wpp_temp_path)
wpp_area = get_wpp_area(wpp_layer)

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

    print('Mendapatkan informasi asosiasi dengan AIS dan VMS...\n')
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
    ship_temp_path = os.path.join(TEMP_FOLDER, 'ship_layer.gpkg')
    ship_layer = merge_vector_layer(ship_list, output_path=ship_temp_path)
    with edit(ship_layer):
        ship_layer.addAttribute(QgsField("DESC", QVariant.String))
        ship_layer.updateFields()
        
        for feat in ship_layer.getFeatures():
            if feat['AIS_MMSI'] != None:
                feat['DESC'] = 'AIS'
                ship_layer.updateFeature(feat)
    if len(vms_list) > 0:
        vms_temp_path = os.path.join(TEMP_FOLDER, 'vms_layer.gpkg')
        vms_layer = merge_vector_layer(vms_list, output_path=vms_temp_path)

        shipvms_temp_path = os.path.join(TEMP_FOLDER, 'shipvms_layer.gpkg')
        shipvms_layer = join_attributes_by_location(ship_layer, vms_layer, join_fields=['status'], output_path=shipvms_temp_path)
        with edit(shipvms_layer):
            for feat in shipvms_layer.getFeatures():
                if feat['status'] == 'vms':
                    feat['DESC'] = 'VMS'
                    shipvms_layer.updateFeature(feat)
        ship_layer = shipvms_layer
    
    column_dict = {
        'LON_CENTRE': 'Longitude',
        'LAT_CENTRE': 'Latitude',
        'TARGET_DIR': 'Heading (deg)',
        'LENGTH': 'Panjang (m)',
        'DESC': 'Asosiasi (AIS/VMS)',
        'AIS_MMSI': 'MMSI',
    }
    export_vector_layer(ship_layer, ship_csv_path, driver='CSV', column_dict=column_dict)
    export_vector_layer(ship_layer, ship_geo_path, driver='GeoJSON')
    ship_layer = QgsVectorLayer(ship_geo_path, layer_name)
    ship2_layer = QgsVectorLayer(ship_geo_path, trmlayer_name)

    # get ship elements and feature number
    print("\nMenghitung jumlah kapal...\n")
    ship_numbers = get_ship_numbers(ship_csv_path)
    feat_numbers = ship_layer.featureCount()

    # load two ship layers to project
    load_vector_layer(ship_layer, ship_template, data_group)
    load_vector_layer(ship2_layer, trm_template, data_group)

    # overlay wpp layer and ship extent
    ship_rect = ship_layer.extent()
    ship_xmin = ship_rect.xMinimum()
    ship_xmax = ship_rect.xMaximum()
    ship_ymin = ship_rect.yMinimum()
    ship_ymax = ship_rect.yMaximum()
    ship_extent = f'{ship_xmin}, {ship_xmax}, {ship_ymin}, {ship_ymax}'
    
    wppship_temp_path = os.path.join(TEMP_FOLDER, 'wppship_layer.gpkg')
    wpp_layer = extract_by_extent(WPP_PATH, ship_extent, output_path=wppship_temp_path)
    wpp_area = get_wpp_area(wpp_layer)

else:
    feat_numbers = 0
    ship_csv_path = None
    ship_numbers = get_ship_numbers(ship_csv_path)

# define layout list
layout_id = [0]
layout_list = [(i, QgsProject.instance().layoutManager().layouts()[i]) for i in layout_id]

# insert elements to layout
for layout in layout_list:
    # add ship size classification
    ship_item0 = sip.cast(layout[1].itemById(
        "unit0"), QgsLayoutItemLabel)
    ship_item0.setText(ship_numbers[0])
    ship_item1 = sip.cast(layout[1].itemById(
        "unit1"), QgsLayoutItemLabel)
    ship_item1.setText(ship_numbers[1])
    ship_item2 = sip.cast(layout[1].itemById(
        "unit2"), QgsLayoutItemLabel)
    ship_item2.setText(ship_numbers[2])
    ship_item3 = sip.cast(layout[1].itemById(
        "unit3"), QgsLayoutItemLabel)
    ship_item3.setText(ship_numbers[3])
    ship_item4 = sip.cast(layout[1].itemById(
        "unit4"), QgsLayoutItemLabel)
    ship_item4.setText(ship_numbers[4])
    ship_item5 = sip.cast(layout[1].itemById(
        "unit5"), QgsLayoutItemLabel)
    ship_item5.setText(ship_numbers[5])

    # add number of VMS, AIS and untransmitted ship
    ship_item6 = sip.cast(layout[1].itemById(
        "unit9"), QgsLayoutItemLabel)
    ship_item6.setText(ship_numbers[11])
    ship_item6 = sip.cast(layout[1].itemById(
        "unit6"), QgsLayoutItemLabel)
    ship_item6.setText(ship_numbers[9])
    ship_item7 = sip.cast(layout[1].itemById(
        "unit7"), QgsLayoutItemLabel)
    ship_item7.setText(ship_numbers[6])

    # add total number of ship
    ship_item8 = sip.cast(layout[1].itemById(
        "unit8"), QgsLayoutItemLabel)
    ship_item8.setText(ship_numbers[10])

    data_item = sip.cast(layout[1].itemById(
        "data"), QgsLayoutItemLabel)
    if (int(ship_numbers[9])) > 0 or (int(ship_numbers[11])) > 0:
        data_item.setText("<Ada data>")
    else:
        data_item.setText("<Tidak ada data>")

    # setup extent on main map
    map_item = sip.cast(layout[1].itemById("map"), QgsLayoutItemMap)
    map_item.zoomToExtent(raster_extent)

    # set the overview map
    overview_item = QgsLayoutItemMapOverview('overview', map_item)
    overview_item.setLinkedMap(map_item)

    # add title map
    title_txt = get_title_text(method, wpp_area, radar_info)
    title_item = sip.cast(layout[1].itemById("judul"), QgsLayoutItemLabel)
    title_item.setText(title_txt)

    # add wind information
    wind_txt = get_wind_text(wind_range, wind_dir)
    wind_item = sip.cast(layout[1].itemById("angin"), QgsLayoutItemLabel)
    wind_item.setText(wind_txt)

    # add source text
    source_txt = get_source_text(radar_info_list)
    source_item = sip.cast(layout[1].itemById("sumber"), QgsLayoutItemLabel)
    source_item.setText(source_txt)

    # set layout name
    layout[1].setName(layer_name)

# save project
outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
QgsProject.instance().write(outputproj_path)

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
qgs.exitQgis()

# remove all files in 'temp' folder
os.chdir(OUTPUT_FOLDER)
os.system('rmdir /s /q temp')

# open current project using command line
os.chdir(SCRIPT_PATH)
os.system(f'{QGIS_BAT} --project {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {OPENLAYOUT_PATH}')

print('\nMembuka project layout...')