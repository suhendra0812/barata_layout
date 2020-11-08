import sys, os

# source paths
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)
BASEMAP_PATH = f'{BASE_PATH}/1.basemaps'
TEMPLATE_PATH = f'{SCRIPT_PATH}/templates'
QGIS_PATH = 'C:/OSGeo4W64/apps/qgis'
PROJECT_PATH = f'{TEMPLATE_PATH}/project/layout_oils.qgz'
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
    OilData,
    DataElements,
    LoadLayer,
    Layout,
)
from info.radar_info import RadarInfo

# set QGIS application path and initialize it
qgs_app = QgsApp(QGIS_PATH)
qgs_app.start()

# define project type and remove previous layer
project_layout = Project(PROJECT_PATH)
project_layout.removeLayerPanel()
project_layout.removeLayerHistory()
project_type = project_layout.getProjectType()

# define method
method = sys.argv[-1]

# input directory path
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
    
    local = radar_info.local

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
    wind_gdf = wind_data.getGeoDataFrame()
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
oil_list = data_list.getOilList()
if len(oil_list) > 0:
    print('- Ada data tumpahan minyak')

    # define path of oil template and oil csv path
    oil_template = f'{TEMPLATE_PATH}/layer/oils_level_layer_template.qml'
    oilgdf_path = f'{OUTPUT_FOLDER}/{layer_name}.geojson'
    oildf_path = f'{OUTPUT_FOLDER}/{layer_name}.csv'

    # get aggregation and transmitted layer of oil data
    oil_data = OilData(oil_list, wind_list)
    oil_gdf = oil_data.getOilGeoDataFrame()
    oil_gdf.to_file(oilgdf_path, driver='GeoJSON')
    oil_df = oil_data.getOilDataFrame()
    oil_df.to_csv(oildf_path)
    oil_layer = oil_data.getLayer(oilgdf_path, layer_name)

    # get oil elements and feature number
    print("\nMenghitung statistik tumpahan minyak...\n")
    oil_elements = DataElements(oil_gdf).getOilElements()
    feat_number = len(oil_gdf)

    # load oil layer to project
    load_oils = LoadLayer(project_layout, oil_layer, oil_template)
    load_oils.addVectorToMap()

    # overlay wpp layer and oil extent
    oil_extent = oil_gdf.total_bounds
    wpp_data = WPPData(WPP_PATH, oil_extent)

    # get value of oil area
    area = sum([i for i in oil_gdf['AREA_KM']])
    area_txt = f'{str(round(area, 2))} km\u00B2'

else:
    print('- Tidak ada data tumpahan minyak')
    feat_number = 0

    oil_gdf = None
    oil_elements = DataElements(oil_gdf).getOilElements()

# define layout manager
layout_manager = Layout(project_type, method, feat_number, wil, radar_info_list, wpp_data, wind_data)

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
outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
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

# open current project using command line
os.chdir(SCRIPT_PATH)
os.system(f'{QGIS_BAT} --project {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {OPENLAYOUT_PATH}')

print('\nMembuka project layout...')
