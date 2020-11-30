import sys, os, shutil
import dateutil.parser
from datetime import datetime, timedelta
from xml.etree import ElementTree

from qgis.core import (
    edit,
    QgsApplication,
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsProcessing,
    QgsProject,
    QgsLayoutItemLabel,
    QgsLayoutItemMap,
    QgsFeature,
    QgsField,
    QgsVectorFileWriter,
    QgsCoordinateTransformContext
)
from qgis.analysis import QgsNativeAlgorithms
from PyQt5.QtCore import QFileInfo, QVariant
from PyQt5.QtWidgets import QFileDialog
import sip

# source paths
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)
BASEMAP_PATH = f'{BASE_PATH}/1.basemaps'
DTO_BASEPATH = f'{BASE_PATH}/6.dto'
TEMPLATE_PATH = f'{SCRIPT_PATH}/templates'
QGIS_PATH = 'C:/OSGeo4W64/apps/qgis'
PLUGINS_PATH = os.path.join(QGIS_PATH, 'python', 'plugins')
PROJECT_PATH = f'{TEMPLATE_PATH}/project/layout_dto.qgz'
WPP_PATH = f'{BASEMAP_PATH}/WPP_Full_PermenKP182014.shp'
OPENLAYOUT_PATH = f'{SCRIPT_PATH}/utils/open_layout.py'
QGIS_BAT = 'C:/OSGeo4W64/bin/qgis.bat'

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

def dto_layer(kml_path, layer_name):
    layer = QgsVectorLayer(kml_path,"layer","ogr")
    subLayers =layer.dataProvider().subLayers()

    dto_layer = QgsVectorLayer('Polygon', layer_name, 'memory')

    geom_list = []
    attr_list = []
    field_list = []
    for subLayer in subLayers:
        geom = subLayer.split('!!::!!')[3]
        if geom == 'Polygon':
            name = subLayer.split('!!::!!')[1]
            uri = "%s|layername=%s" % (kml_path, name)
            #Create layer
            sub_vlayer = QgsVectorLayer(uri, name, 'ogr')
            for feat in sub_vlayer.getFeatures():
                desc = feat['description']
                if desc != None:
                    desc = desc.strip()
                    geom_list.append(feat.geometry())
                    if 'RADARSAT' in desc:
                        desc_dict = {}
                        for d in desc.split('\n'):
                            x = d.split(': ')
                            desc_dict[x[0]] = x[1]
                        attr = list(desc_dict.values())
                        field = list(desc_dict.keys())
                        attr_list.append(attr)
                        field_list.append(field)
                    elif 'SAR' in desc:        
                        tree = ElementTree.fromstring(desc)
                        b_elems = tree.findall(".//b")
                        attr = [b.text for b in b_elems]
                        attr_list.append(attr)

    feat_list = []
    for i, geom in enumerate(geom_list):
        feat = QgsFeature()
        feat.setGeometry(geom)
        feat.setAttributes(attr_list[i])
        feat_list.append(feat)

    feat_len = [len(feat.attributes()) for feat in feat_list][0]

    if feat_len == 11:
        dto_layer.dataProvider().addAttributes([
            QgsField('PR ID', QVariant.Int),
            QgsField('AR Counter', QVariant.Int),
            QgsField('Sensing Start', QVariant.DateTime),
            QgsField('Sensing Stop', QVariant.DateTime),
            QgsField('Sensor Mode', QVariant.String),
            QgsField('Satellite', QVariant.String),
            QgsField('Orbit Direction', QVariant.String),
            QgsField('Look Side', QVariant.String),
            QgsField('Look Angle', QVariant.Double),
            QgsField('Beam', QVariant.String),
        ])
    elif feat_len == 19:
        dto_layer.dataProvider().addAttributes([
            QgsField(field_list[0][0], QVariant.String),
            QgsField(field_list[0][1], QVariant.String),
            QgsField(field_list[0][2], QVariant.DateTime),
            QgsField(field_list[0][3], QVariant.DateTime),
            QgsField(field_list[0][4], QVariant.Double),
            QgsField(field_list[0][5], QVariant.String),
            QgsField(field_list[0][6], QVariant.Double),
            QgsField(field_list[0][7], QVariant.Double),
            QgsField(field_list[0][8], QVariant.String),
            QgsField(field_list[0][9], QVariant.String),
            QgsField(field_list[0][10], QVariant.Double),
            QgsField(field_list[0][11], QVariant.String),
            QgsField(field_list[0][12], QVariant.String),
            QgsField(field_list[0][13], QVariant.String),
            QgsField(field_list[0][14], QVariant.String),
            QgsField(field_list[0][15], QVariant.String),
            QgsField(field_list[0][16], QVariant.Int),
            QgsField(field_list[0][17], QVariant.Int),
            QgsField(field_list[0][18], QVariant.String),
        ])

    dto_layer.updateFields()    
        
    dto_layer.dataProvider().addFeatures(feat_list)

    return dto_layer

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

def load_vector_layer(vector_layer, template, group):
    QgsProject.instance().addMapLayer(vector_layer, False)
    group.addLayer(vector_layer)
    vector_layer.loadNamedStyle(template)
    QgsProject.instance().layerTreeRoot().findLayer(vector_layer).setCustomProperty("showFeatureCount", True)

# define method
method = sys.argv[-1]

if method == 'banyak':
    data_folder = QFileDialog.getExistingDirectory(None, 'Select Data Directory', BASE_PATH)
    dto_list = glob.glob(f'{data_folder}/*.kml')

    user = input('\nMasukkan nama instansi\t: ').lower()
    location = input('Masukkan nama wilayah\t: ').lower()

    for dto_path in dto_list:
        print('\nSumber data:')
        print(dto_path)

        # get project information
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

        # get dto info list
        dtoinfo_list = []
        dto_name = QFileInfo(dto_path).baseName()
        dto_layer = dto_layer(dto_path, dto_name)
        dto_count = dto_layer.featureCount()

        sat_name = [feat['Satellite'] for feat in dto_layer.getFeatures()][0]
        print(f'\nRadar\t\t: {sat_name}')
        print(f'Jumlah DTO\t: {dto_count}')

        if sat_name == 'RADARSAT-2':
            utc = [feat['Start UTC Time'] for feat in dto_layer.getFeatures()][0]
        else:
            utc = [feat['Sensing Start'] for feat in dto_layer.getFeatures()][0]
        
        local = dateutil.parser.parse(utc) + timedelta(hours=7).strftime('%Y%m%d_%H%M%S')
        layer_name = f'{user}_{location}_{local}_{project_type}'
        if sat_name == 'RADARSAT-2':
            sat_dir = 'radarsat'
        else:
            sat_dir = 'cosmo_skymed'

        OUTPUT_FOLDER = f'{DTO_BASEPATH}/{sat_dir}/{local[:6]}/{local[:8]}/{layer_name[:-4]}'
        TEMP_FOLDER = os.path.join(OUTPUT_FOLDER, 'temp')
        if not os.path.exists(TEMP_FOLDER):
            os.makedirs(TEMP_FOLDER)

        # save project
        outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
        QgsProject.instance().write(outputproj_path)

        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        dtogeo_path = f'{OUTPUT_FOLDER}/{layer_name}.geojson'
        newdto_path = f'{OUTPUT_FOLDER}/{layer_name}.kml'

        shutil.copyfile(dto_path, newdto_path)

        # create and get dto temporary layer
        export_vector_layer(dto_layer, dtogeo_path, driver='GeoJSON')
        dto_layer = QgsVectorLayer(dtogeo_path, layer_name)

        # load dto layer to project
        dto_template = f'{TEMPLATE_PATH}/layer/dto_layer_template.qml'
        load_vector_layer(dto_layer, dto_template, data_group)

        # zoom to layer
        dto_rect = dto_layer.extent()
        dto_xmin = dto_rect.xMinimum()
        dto_xmax = dto_rect.xMaximum()
        dto_ymin = dto_rect.yMinimum()
        dto_ymax = dto_rect.yMaximum()
        dto_extent = f'{dto_xmin}, {dto_xmax}, {dto_ymin}, {dto_ymax}'

        # load wpp data and get WPP area which is overlaid within raster
        wppdto_temp_path = os.path.join(TEMP_FOLDER, 'wppship_layer.gpkg')
        wpp_layer = extract_by_extent(WPP_PATH, ship_extent, output_path=wppship_temp_path)
        wpp_area = get_wpp_area(wpp_layer)

        # define layout list
        layout_id = [0]
        layout_list = [(i, QgsProject.instance().layoutManager().layouts()[i]) for i in layout_id]

        # setup extent on main map
        map_item = sip.cast(layout[1].itemById("map"), QgsLayoutItemMap)
        extent.scale(2)
        map_item.zoomToExtent(dto_rect)

        # set atlas
        title_exp = """[%upper(format_date("Start Time"+ to_interval('7 hours'), 'dd MMMM yyyy pukul hh:mm:ss WIB', 'id'))%]"""
        atlas_exp = """substr(@project_basename, 0, -19)||(format_date("Start Time"+to_interval('7 hours'), 'yyyyMMdd_hhmmss'))||'_dto'"""
        note_exp = """[%title(format_date("Start Time", 'dd MMMM yyyy', 'id'))%] sekitar pukul [%CASE WHEN to_time("Start Time") >=  to_time('06:21:00') AND to_time("Start Time") <=  to_time('18:21:00') THEN '06:00 WIB' ELSE '20:00 WIB' END%] \nSensor Mode : [% "Mode" %]"""
        for layout in layout_list:
            # set atlas
            layout[1].atlas().setCoverageLayer(layer)
            layout[1].atlas().setEnabled(True)
            layout[1].atlas().setFilenameExpression(atlas_exp)
        
            # add title map
            title_item = sip.cast(layout[1].itemById("judul"), QgsLayoutItemLabel)
            title_item.setText(
                f'PETA AREA DETEKSI CITRA RADAR {sat_name.upper()} DI PERAIRAN {wpp_area}\r\nPERIODE {title_exp}')

            # add note
            note_item = sip.cast(layout[1].itemById("note"), QgsLayoutItemLabel)
            note_item.setText(
                f'CATATAN:\nNotifikasi citra dapat diakuisisi atau tidak:\n{note_exp}')

        # save project
        QgsProject.instance().write(outputproj_path)

        print('\nLayout telah dibuat')

        print('\nSelesai')

else:
    # get project information
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

    dto_path = QFileDialog.getOpenFileName(None, "Select DTO Directory", BASE_PATH, 'DTO Files (*.kml *.shp)')[0]

    print('\nSumber data:')
    print(dto_path)

    # get dto info list
    dtoinfo_list = []
    dto_name = QFileInfo(dto_path).baseName()
    dto_layer = dto_layer(dto_path, dto_name)
    dto_count = dto_layer.featureCount()

    user = input('\nMasukkan nama instansi\t: ').lower()
    location = input('Masukkan nama wilayah\t: ').lower()

    sat_name = [feat['Satellite'] for feat in dto_layer.getFeatures()][0]
    print(f'\nRadar\t\t: {sat_name}')
    print(f'Jumlah DTO\t: {dto_count}')

    if sat_name == 'RADARSAT-2':
        utc = [feat['Start UTC Time'] for feat in dto_layer.getFeatures()][0]
    else:
        utc = [feat['Sensing Start'] for feat in dto_layer.getFeatures()][0]
    
    local = (dateutil.parser.parse(utc) + timedelta(hours=7)).strftime('%Y%m%d_%H%M%S')
    layer_name = f'{user}_{location}_{local}_{project_type}'
    if sat_name == 'RADARSAT-2':
        sat_dir = 'radarsat'
    else:
        sat_dir = 'cosmo_skymed'

    OUTPUT_FOLDER = f'{DTO_BASEPATH}/{sat_dir}/{local[:6]}/{local[:8]}/{layer_name[:-4]}'
    TEMP_FOLDER = os.path.join(OUTPUT_FOLDER, 'temp')
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    # save project
    outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
    QgsProject.instance().write(outputproj_path)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    dtogeo_path = f'{OUTPUT_FOLDER}/{layer_name}.geojson'
    newdto_path = f'{OUTPUT_FOLDER}/{layer_name}.kml'

    shutil.copyfile(dto_path, newdto_path)

    # create and get dto temporary layer
    export_vector_layer(dto_layer, dtogeo_path, driver='GeoJSON')
    dto_layer = QgsVectorLayer(dtogeo_path, layer_name)

    # load dto layer to project
    dto_template = f'{TEMPLATE_PATH}/layer/dto_layer_template.qml'
    load_vector_layer(dto_layer, dto_template, data_group)

    # zoom to layer
    dto_rect = dto_layer.extent()
    dto_xmin = dto_rect.xMinimum()
    dto_xmax = dto_rect.xMaximum()
    dto_ymin = dto_rect.yMinimum()
    dto_ymax = dto_rect.yMaximum()
    dto_extent = f'{dto_xmin}, {dto_xmax}, {dto_ymin}, {dto_ymax}'

    # load wpp data and get WPP area which is overlaid within raster
    wppdto_temp_path = os.path.join(TEMP_FOLDER, 'wppship_layer.gpkg')
    wpp_layer = extract_by_extent(WPP_PATH, dto_extent, output_path=wppdto_temp_path)
    wpp_area = get_wpp_area(wpp_layer)

    # define layout list
    layout_id = [0]
    layout_list = [(i, QgsProject.instance().layoutManager().layouts()[i]) for i in layout_id]

    title_exp = """[%upper(format_date("Start Time"+ to_interval('7 hours'), 'dd MMMM yyyy pukul hh:mm:ss WIB', 'id'))%]"""
    atlas_exp = """substr(@project_basename, 0, -19)||(format_date("Start Time"+to_interval('7 hours'), 'yyyyMMdd_hhmmss'))||'_dto'"""
    note_exp = """[%title(format_date("Start Time", 'dd MMMM yyyy', 'id'))%] sekitar pukul [%CASE WHEN to_time("Start Time") >=  to_time('06:21:00') AND to_time("Start Time") <=  to_time('18:21:00') THEN '06:00 WIB' ELSE '20:00 WIB' END%] \nSensor Mode : [% "Mode" %]"""
    
    for layout in layout_list:
        # setup extent on main map
        map_item = sip.cast(layout[1].itemById("map"), QgsLayoutItemMap)
        dto_rect.scale(2)
        map_item.zoomToExtent(dto_rect)

        # set atlas
        layout[1].atlas().setCoverageLayer(dto_layer)
        layout[1].atlas().setEnabled(True)
        layout[1].atlas().setFilenameExpression(atlas_exp)
    
        # add title map
        title_item = sip.cast(layout[1].itemById("judul"), QgsLayoutItemLabel)
        title_item.setText(
            f'PETA AREA DETEKSI CITRA RADAR {sat_name.upper()} DI PERAIRAN {wpp_area}\r\nPERIODE {title_exp}')

        # add note
        note_item = sip.cast(layout[1].itemById("note"), QgsLayoutItemLabel)
        note_item.setText(
            f'CATATAN:\nNotifikasi citra dapat diakuisisi atau tidak:\n{note_exp}')

    # save project
    QgsProject.instance().write(outputproj_path)

    print('\nLayout telah dibuat')

    print('\nSelesai')

qgs.exitQgis()

# remove all files in 'temp' folder
os.chdir(OUTPUT_FOLDER)
os.system('rmdir /s /q temp')

if method == 'satu':
    # open current project using command line
    os.chdir(SCRIPT_PATH)
    os.system(f'{QGIS_BAT} --project {outputproj_path} --extent {dto_xmin},{dto_ymin},{dto_xmax},{dto_ymax} --code {OPENLAYOUT_PATH}')

    print('\nMembuka project layout...')
