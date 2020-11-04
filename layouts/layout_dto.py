import sys, os, shutil

# source paths
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)
BASEMAP_PATH = f'{BASE_PATH}/1.basemaps'
DTO_BASEPATH = f'{BASE_PATH}/6.dto'
TEMPLATE_PATH = f'{SCRIPT_PATH}/templates'
QGIS_PATH = 'C:/OSGeo4W64/apps/qgis'
PROJECT_PATH = f'{TEMPLATE_PATH}/project/layout_dto.qgz'
WPP_PATH = f'{BASEMAP_PATH}/WPP_Full_PermenKP182014.shp'
OPENLAYOUT_PATH = f'{SCRIPT_PATH}/utils/open_layout.py'
QGIS_BAT = 'C:/OSGeo4W64/bin/qgis.bat'

sys.path.append(SCRIPT_PATH)

from barata.barata_layout import (
    QgsApp,
    Project,
    FileDialog,
    DTOData,
    LayerExtent,
    WPPData,
    LoadLayer,
    LayoutDTO,
)
from info.dto_info import DTOInfo

# set QGIS application path and initialize it
qgs_app = QgsApp(QGIS_PATH)
qgs_app.start()

# get project information
project_layout = Project(PROJECT_PATH)
project_layout.removeLayerPanel()
project_layout.removeLayerHistory()
project_type = os.path.basename(PROJECT_PATH)[:-4][-3:]

dto_path = FileDialog(BASE_PATH).open(type=project_type)

print('\nSumber data:')
print(dto_path)

# get dto info list
dtoinfo_list = []
dto_gdf = DTOData(dto_path).getDTOGeoDataFrame()
for f in range(len(dto_gdf)):
    idx = f + 1
    dtoinfo = DTOInfo(dto_path, idx)
    dtoinfo_list.append(dtoinfo)

print(f'\nRadar\t\t: {dtoinfo_list[0].sat}')
print(f'Jumlah DTO\t: {len(dto_gdf)}')

# get variable from dto info
filename = os.path.basename(dto_path)
fn_split = filename.split('_')

# user = fn_split[0]
# location = fn_split[1]
# if user.isdigit() and location.isdigit():
user = input('\nMasukkan nama instansi\t: ')
location = input('Masukkan nama wilayah\t: ')

local = dtoinfo_list[0].local
layer_name = f'{user}_{location}_{local}_{project_type}'
if dtoinfo_list[0].sat == 'RADARSAT-2':
    sat_dir = 'radarsat'
else:
    sat_dir = 'cosmo_skymed'

OUTPUT_FOLDER = f'{DTO_BASEPATH}/{sat_dir}/{local[:6]}/{local[:8]}/{layer_name[:-4]}'

if not os.path.exists(OUTPUT_FOLDER):
    try:
        os.makedirs(OUTPUT_FOLDER)
    except:
        os.mkdir(OUTPUT_FOLDER)

dtogdf_path = f'{OUTPUT_FOLDER}/{layer_name}.geojson'
newdto_path = f'{OUTPUT_FOLDER}/{layer_name}.kml'

shutil.copyfile(dto_path, newdto_path)

# create and get dto temporary layer
dto_data = DTOData(dto_path, dtoinfo_list)
dto_gdf = dto_data.getDTOGeoDataFrame()
dto_gdf.to_file(dtogdf_path, driver='GeoJSON')
dto_layer = dto_data.getLayer(dtogdf_path, dtoinfo_list[0].sat_id)

# load dto layer to project
dto_template = f'{TEMPLATE_PATH}/layer/dto_layer_template.qml'
load_dto = LoadLayer(project_layout, dto_layer, dto_template)
load_dto.addVectorToMap()

# zoom to layer
extent = LayerExtent(dto_layer).getExtent()

# load wpp data and get WPP area which is overlaid within raster
wpp_layer = WPPData(WPP_PATH, extent)

# define layout manager
layout_manager = LayoutDTO(project_type, dtoinfo_list, wpp_layer)

# set and insert attributes to layout
layout_manager.setMap(extent)
layout_manager.setAtlas(dto_layer)
layout_manager.insertTitleText()
layout_manager.insertNoteText()

# save project
outputproj_path = f'{OUTPUT_FOLDER}/{layer_name}.qgz'
project_layout.saveProject(outputproj_path)

print('\nLayout telah dibuat\n')

print('\nSelesai')

qgs_app.quit()

# set raster extent
xmin = extent.xMinimum()
xmax = extent.xMaximum()
ymin = extent.yMinimum()
ymax = extent.yMaximum()

# open current project using command line
os.chdir(SCRIPT_PATH)
os.system(f'{QGIS_BAT} --project {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {OPENLAYOUT_PATH}')

print('\nMembuka project layout...')
