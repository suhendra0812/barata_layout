import sys, os
from barata_layout import *
from dto_info import DTOInfo

#set QGIS application path and initialize it
qgs_path = 'C:\\OSGeo4W64\\apps\\qgis'
qgs_app = QgsApp(qgs_path)
qgs_app.start()

#source paths
BASE_PATH = "D:\\BARATA"
BASEMAP_PATH = f'{BASE_PATH}\\1.basemaps'
TEMPLATE_PATH = 'templates'

#get project information
project_path = f'{TEMPLATE_PATH}\\project\\layout_dto.qgz'

project_layout = Project(project_path)
project_layout.removeLayerPanel()
project_layout.removeLayerHistory()
project_type = os.path.basename(project_path)[:-4][-3:]

print (f'\nTipe project: {project_type}')

#define group
basemap_group = project_layout.getBasemapGroup()
data_group = project_layout.getDataGroup()

dto_path = FileDialog(BASE_PATH).open(type=project_type)

print ('Sumber data:')
print (dto_path)

#get dto feature list
dtofeat_list = DTOLayer(dto_path).getFeatList()

OUTPUT_FOLDER = os.path.dirname(dto_path)

#get dto info list
dtoinfo_list = []
for f in range(len(dtofeat_list)):
    idx = f + 1
    dtoinfo = DTOInfo(dto_path, idx)
    dtoinfo_list.append(dtoinfo)

print(f'Jumlah DTO: {len(dtofeat_list)}')
print(f'Radar: {dtoinfo_list[-1].sat}')

#get variable from dto info
wil = os.path.basename(dto_path)[:-4][:-4][:-16]
local = dtoinfo_list[-1].local
layer_name = f'{wil}_{local}_{project_type}'
dtogdf_path = f'{OUTPUT_FOLDER}\\{layer_name}.shp'

#create and get dto temporary layer
templayer = DTOLayer(dto_path, dtoinfo_list).getLayer()

#export the temporary layer to shapefile
ExportLayer(templayer, dtogdf_path).to_shp()

#get dto layer list from exported shapefile
dtolayer_list = DataLayer([dtogdf_path]).getLayerList()

#load dto layer to project
dto_template = f'{TEMPLATE_PATH}\\layer\\dto_layer_template.qml'
for dtolayer in dtolayer_list:
    dtolayer.setName(dtoinfo_list[-1].sat_id)
    LoadVectorLayer(dtolayer, data_group, dto_template)

#zoom to layer
extent = LayerExtent([dtolayer]).getExtent()
    
#load wpp data and get WPP area which is overlaid within raster
wpp_path = f'{BASEMAP_PATH}\\WPP_Full_PermenKP182014.shp'
wpp_layer = WPPLayer(wpp_path, extent)

#define layout manager
layout_manager = LayoutDTO(project_type, dtoinfo_list, wpp_layer)

#set and insert attributes to layout
layout_manager.setMap(extent)
layout_manager.setAtlas(dtolayer)
layout_manager.insertTitleText()
layout_manager.insertNoteText()

#save project
outputproj_path = f'{OUTPUT_FOLDER}\\{layer_name}.qgz'
project_layout.saveProject(outputproj_path)

print ('\nLayout telah dibuat\n')

print ('\nSelesai')

qgs_app.quit()

#set raster extent
xmin = extent.xMinimum()
xmax = extent.xMaximum()
ymin = extent.yMinimum()
ymax = extent.yMaximum()

#define open layout script path
OPENLAYOUT_SCRIPT = 'open_layout.py'

#open current project using command line
os.system(f'qgis --projectfile {outputproj_path} --extent {xmin},{ymin},{xmax},{ymax} --code {OPENLAYOUT_SCRIPT}')

print ('\nMembuka project layout...')
