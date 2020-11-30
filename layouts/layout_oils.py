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
from qgis.analysis import (
    QgsNativeAlgorithms,
    QgsInterpolator,
    QgsIDWInterpolator,
    QgsGridFileWriter
)
from PyQt5.QtCore import QFileInfo, QVariant
from PyQt5.QtWidgets import QFileDialog
import sip

# source paths
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)
BASEMAP_PATH = os.path.join(BASE_PATH, '1.basemaps')
TEMPLATE_PATH = os.path.join(SCRIPT_PATH, 'templates')
QGIS_PATH = 'C:/OSGeo4W64/apps/qgis'
PLUGINS_PATH = os.path.join(QGIS_PATH, 'python', 'plugins')
PROJECT_PATH = os.path.join(TEMPLATE_PATH, 'project', 'layout_oils.qgz')
WPP_PATH = os.path.join(BASEMAP_PATH, 'WPP_Full_PermenKP182014.shp')
OPENLAYOUT_PATH = os.path.join(SCRIPT_PATH, 'utils', 'open_layout.py')
QGIS_BAT = 'C:/OSGeo4W64/bin/qgis.bat'

sys.path.append(SCRIPT_PATH)
from info.radar_info import RadarInfo

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

def zonal_statistics(input_vector, input_raster, column_prefix='_', output_path=None):
    algorithm = 'native:zonalstatisticsfb'
    if output_path == None:
        output_path = QgsProcessing.TEMPORARY_OUTPUT
    params = {
        'INPUT': input_vector,
        'INPUT_RASTER': input_raster,
        'RASTER_BAND': 1,
        'COLUMN_PREFIX': column_prefix,
        'STATISTICS': [2,5,6],
        'OUTPUT': output_path
    }
    output = run_processing(algorithm, params)
    return output

def idw_interpolation(input_layer, extent, field_name, pixel_size, output_path):
    layer_data = QgsInterpolator.LayerData()
    layer_data.source = input_layer
    layer_data.zCoordInterpolation = False
    layer_data.interpolationAttribute = input_layer.fields().indexFromName(field_name)
    layer_data.mInputType = 0

    export_path = output_path

    idw_interpolator = QgsIDWInterpolator([layer_data])
    res = pixel_size
    ncols = int(( extent.xMaximum() - extent.xMinimum()) / res)
    nrows = int((extent.yMaximum() - extent.yMinimum()) / res)

    output = QgsGridFileWriter(idw_interpolator,export_path,extent,ncols,nrows)
    output.writeFile()

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

def get_oil_numbers(oil_csv_path=None):
    if oil_csv_path != None:
        oil_df = pd.read_csv(oil_csv_path)
        # oil size stat
        lenmin = oil_df['Panjang (km)'].min()
        lenmax = oil_df['Panjang (km)'].max()

        widmin = oil_df['Luas (km2)'].min()
        widmax = oil_df['Luas (km2)'].max()

        # oil confindent stat
        high = oil_df[oil_df['Tingkat Kepercayaan'] == 'HIGH']
        low = oil_df[oil_df['Tingkat Kepercayaan'] == 'LOW']

        hi = len(high)
        lo = len(low)

    else:
        lenmin = lenmax = widmin = widmax = hi = lo = 0

    print(f"Panjang tumpahan minyak terendah\t\t= {lenmin} km")
    print(f"Panjang tumpahan minyak tertinggi\t\t= {lenmax} km")
    print(
        f"\nLuas tumpahan minyak terendah\t\t\t= {widmin} km\u00B2")
    print(
        f"Luas tumpahan minyak tertinggi\t\t\t= {widmax} km\u00B2")
    print(
        f"\nJumlah tumpahan minyak berkepercayaan tinggi\t= {hi}")
    print(f"Jumlah tumpahan minyak berkepercayaan rendah\t= {lo}")
    print(f"\nTotal jumlah tumpahan minyak\t\t\t= {hi+lo}")

    return [hi, lo, lenmin, lenmax, widmin, widmax]

def get_oil_area_txt(oil_layer):
    oil_area = sum([feat['AREA_KM'] for feat in oil_layer.getFeatures()])
    oil_area_txt = f'{str(round(oil_area, 2))} km\u00B2'
    return oil_area_txt

def get_title_text(method, layout_id, wpp_area, radar_info):
    bulan = {
        '01': 'JANUARI',
        '02': 'FEBRUARI',
        '03': 'MARET',
        '04': 'APRIL',
        '05': 'MEI',
        '06': 'JUNI',
        '07': 'JULI',
        '08': 'AGUSTUS',
        '09': 'SEPTEMBER',
        '10': 'OKTOBER',
        '11': 'NOVEMBER',
        '12': 'DESEMBER'
    }

    if method == 'satu':
        periode_txt = f'{radar_info.tgl_local} {bulan[radar_info.bln_local]} {radar_info.thn_local} PUKUL {radar_info.jam_local}:{radar_info.m}:{radar_info.d} WIB'
    else:
        periode_txt = f'{radar_info.tgl_local} {bulan[radar_info.bln_local]} {radar_info.thn_local} PUKUL {radar_info.jam_local}:{radar_info.m} WIB'
    
    if layout_id == 3:
        title_txt = f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp_area} (BAGIAN [%$id+1%])\nPERIODE {periode_txt}'
    else:
        title_txt = f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp_area}\nPERIODE {periode_txt}'
    
    return title_txt

def get_wind_text(wind_range, wind_dir):
    if all(wind_range):
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
project_type = project_basename.split('_')[-1]

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
oil_list = glob.glob(f'{data_folder}/*OIL.shp')

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
if len(oil_list) > 0:
    print('- Ada data tumpahan minyak')
else:
    print('- Tidak ada data tumpahan minyak')

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
    wind_temp_path = os.path.join(TEMP_FOLDER, 'wind_layer.gpkg')
    wind_layer = merge_vector_layer(wind_list, output_path=wind_temp_path)
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
else:
    wind_range = (None, None)
    wind_dir = None

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
if len(oil_list) > 0:
    # define path of oil template and oil csv path
    oil_template = f'{TEMPLATE_PATH}/layer/oils_level_layer_template.qml'
    oil_geo_path = f'{OUTPUT_FOLDER}/{layer_name}.geojson'
    oil_csv_path = f'{OUTPUT_FOLDER}/{layer_name}.csv'

    # get aggregation and transmitted layer of oil data
    oil_temp_path = os.path.join(TEMP_FOLDER, 'oil_layer.gpkg')
    oil_layer = merge_vector_layer(oil_list, output_path=oil_temp_path)

    # get oil layer extent
    oil_extent = oil_layer.extent()

    with edit(oil_layer):
        oil_layer.dataProvider().addAttributes(
            [
                QgsField('MIN_WSPD', QVariant.Double),
                QgsField('MAX_WSPD', QVariant.Double),
                QgsField('MEAN_WSPD', QVariant.Double),
                QgsField('MIN_WANG', QVariant.Double),
                QgsField('MAX_WANG', QVariant.Double),
                QgsField('MEAN_WANG', QVariant.Double),
            ]
        )
    if len(wind_list) > 0:
        wspd_interp_path = os.path.join(TEMP_FOLDER, 'wspd_interp.tif')
        idw_interpolation(
            wind_layer,
            oil_extent,
            'speed',
            0.01,
            wspd_interp_path
        )
        wang_interp_path = os.path.join(TEMP_FOLDER, 'wang_interp.tif')
        idw_interpolation(
            wind_layer,
            oil_extent,
            'angle',
            0.01,
            wang_interp_path
        )
        
        wspdoil_temp_path = os.path.join(TEMP_FOLDER, 'wspdoil_layer.gpkg')
        wspdoil_layer = zonal_statistics(oil_layer, wspd_interp_path, column_prefix='speed_', output_path=wspdoil_temp_path)
        wangoil_temp_path = os.path.join(TEMP_FOLDER, 'wangoil_layer.gpkg')
        wangoil_layer = zonal_statistics(oil_layer, wang_interp_path, column_prefix='angle_', output_path=wangoil_temp_path)
        
        with edit(oil_layer):
            for oil_feat, wspdoil_feat in zip(oil_layer.getFeatures(), wspdoil_layer.getFeatures()):
                oil_feat['MIN_WSPD'] = wspdoil_feat['speed_min']
                oil_feat['MAX_WSPD'] = wspdoil_feat['speed_max']
                oil_feat['MEAN_WSPD'] = wspdoil_feat['speed_mean']
                oil_layer.updateFeature(oil_feat)
            for oil_feat, wangoil_feat in zip(oil_layer.getFeatures(), wangoil_layer.getFeatures()):
                oil_feat['MIN_WANG'] = wangoil_feat['angle_min']
                oil_feat['MAX_WANG'] = wangoil_feat['angle_max']
                oil_feat['MEAN_WANG'] = wangoil_feat['angle_mean']
                oil_layer.updateFeature(oil_feat)

    column_dict = {
        'BARIC_LON': 'Longitude',
        'BARIC_LAT': 'Latitude',
        'LENGTH_KM': 'Panjang (km)',
        'AREA_KM': 'Luas (km2)',
        'MEAN_WSPD': 'Kecepatan Angin (m/s)',
        'MEAN_WANG': 'Arah Angin (deg)',
        'ALARM_LEV': 'Tingkat Kepercayaan',
    }
    export_vector_layer(oil_layer, oil_csv_path, driver='CSV', column_dict=column_dict)
    export_vector_layer(oil_layer, oil_geo_path, driver='GeoJSON')
    oil_layer = QgsVectorLayer(oil_geo_path, layer_name)

    # get oil elements and feature number
    print("Menghitung statistik tumpahan minyak...\n")
    oil_numbers = get_oil_numbers(oil_csv_path)
    feat_numbers = oil_layer.featureCount()

    # load oil layer to project
    load_vector_layer(oil_layer, oil_template, data_group)

    # overlay wpp layer and oil extent
    wppoil_temp_path = os.path.join(TEMP_FOLDER, 'wppoil_layer.gpkg')
    wpp_layer = extract_by_extent(WPP_PATH, oil_extent, output_path=wppoil_temp_path)
    wpp_area = get_wpp_area(wpp_layer)
else:
    print('- Tidak ada data tumpahan minyak')
    feat_numbers = 0
    oil_csv_path = None
    oil_numbers = get_oil_numbers(oil_csv_path)

# define layout list
if feat_numbers == 0:
    layout_id = [0]
elif feat_numbers == 1:
    layout_id = [1]
elif feat_numbers > 1:
    layout_id = [3, 2]

layout_list = [(i, QgsProject.instance().layoutManager().layouts()[i]) for i in layout_id]

# set atlas and oil area text to specific layout
for layout in layout_list:
    if layout[0] == 1 or layout[0] == 3:
        if layout[0] == 1:
            atlas_name = "@layout_name"
        elif layout[0] == 3:
            atlas_name = "@layout_name||@atlas_featurenumber"
        # set atlas
        layout[1].atlas().setCoverageLayer(oil_layer)
        layout[1].atlas().setEnabled(True)
        layout[1].atlas().setFilenameExpression(atlas_name)
    elif layout[0] == 2:
        oil_area_txt = get_oil_area_txt(oil_layer)
        oil_area_item = sip.cast(layout[1].itemById("luas"), QgsLayoutItemLabel)
        oil_area_item.setText(oil_area_txt)

    # setup extent on main map
    map_item = sip.cast(layout[1].itemById("map"), QgsLayoutItemMap)
    map_item.zoomToExtent(raster_extent)

    # set the overview map
    overview_item = QgsLayoutItemMapOverview('overview', map_item)
    overview_item.setLinkedMap(map_item)

    # add title map
    title_txt = get_title_text(method, layout[0], wpp_area, radar_info)
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
    if layout[0] == 3:
        layout[1].setName(f'{layer_name}_')

# save project
outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
QgsProject.instance().write(outputproj_path)

print('\nLayout telah dibuat\n')

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
