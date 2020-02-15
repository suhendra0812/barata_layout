import sys
import os
from barata_layout import *
from radar_info import RadarInfo

# set QGIS application path and initialize it
qgs_path = 'C:\\OSGeo4W64\\apps\\qgis'
qgs_app = QgsApp(qgs_path)
qgs_app.start()

# source paths
BASE_PATH = "D:\\BARATA"
BASEMAP_PATH = f'{BASE_PATH}\\1.basemaps'
TEMPLATE_PATH = 'templates'

# define project type and remove previous layer
project_path = f'{TEMPLATE_PATH}\\project\\layout_oils.qgz'

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
oil_list = data_list.getOilList()
if len(oil_list) > 0:
    print('- Ada data tumpahan minyak')

    # define name and path
    oilgdf_path = f'{OUTPUT_FOLDER}\\{layer_name}.shp'

    # define path of oil template
    oil_template = f'{TEMPLATE_PATH}\\layer\\oils_level_layer_template.qml'

    # get list of features and attributes, geodataframe and feature extent
    oilfeat_list = DataLayer(oil_list).getFeatList()
    oilattr_list = DataLayer(oil_list).getAttrList()
    oilgdf = DataLayer(oil_list).getGeoDataFrame()
    oil_extent = DataLayer(oil_list).getFeatExtent()

    # get aggregation and transmitted layer of oil data
    agg_oillayer = AggregationLayer(oilfeat_list, oilattr_list, layer_name).getAggLayer()
    wind_oillayer = WindOilLayer(oilgdf, windgdf, agg_oillayer).getWindOilLayer()

    # export layer to shapefile
    ExportLayer(wind_oillayer, oilgdf_path).to_shp()

    # get oil elements and feature number
    oil_elements = DataElements(project_type, oilgdf_path).getOilElements()
    feat_number = len(oilfeat_list)

    # get oil layer of oil data
    oil_layer = DataLayer([oilgdf_path]).getLayerList()[0]

    # load oil layer to project
    LoadVectorLayer(oil_layer, data_group, oil_template)

    # overlay wpp layer and oil extent
    wpp_layer = WPPLayer(wpp_path, oil_extent)

    # get value of oil area
    area = sum([i for i in oilgdf['AREA_KM']])
    area_txt = f'{str(round(area, 2))} km\u00B2'

else:
    print('- Tidak ada data tumpahan minyak')
    feat_number = 0

    oildf_path = None
    oil_elements = DataElements(project_type, oildf_path).getOilElements()

# define layout manager
layout_manager = Layout(project_type, method, feat_number, wil, radar_info_list, wpp_layer, wind_data)

# get layout list
layout_list = layout_manager.getLayoutList()

# set atlas and oil area text to specific layout
for layout in layout_list:
    if layout[0] == 1 or layout[0] == 3:
        layout_manager.setAtlas(oil_layer)
    elif layout[0] == 2:
        layout_manager.setOilAreaText(area_txt)
    else:
        pass

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
