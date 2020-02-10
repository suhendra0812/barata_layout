from datetime import datetime, timedelta
import sip
import geopandas as gpd
import glob
from barata_layout import *
import read_kml

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
project_type = 'dto'

print (f'\nTipe project: {project_type}')

#define group
basemap_group = project_layout.getBasemapGroup()
data_group = project_layout.getDataGroup()

dto_path = FileDialog(BASE_PATH).open(type='dto')

print ('Sumber data:')
print (dto_path)

class DTOLayer:
    def __init__(self, dto_path):
        self.baseName = QFileInfo(dto_path).baseName()
        self.layer = QgsVectorLayer(dto_path, self.baseName, 'ogr')
        self.subLayers = self.layer.dataProvider().subLayers()

        self.dtolayer_list = []
        for subLayer in self.subLayers:
            self.name = subLayer.split('!!::!!')[1]
            if self.name[:4] == 'PROG' or self.name == 'swath-1':
                self.uri = "%s|layername=%s" % (dto_path, self.name)
                #Create layer
                self.sub_vlayer = QgsVectorLayer(self.uri, self.name, 'ogr')
                self.sublayer_feat = [feat for feat in self.sub_vlayer.getFeatures()]
                if len(self.sublayer_feat) == 1:
                    self.dto_feat = self.sublayer_feat
                elif len(sublayer_feat) > 1:
                    self.dto_feat = self.sublayer_feat[1:]
                
                self.infolist = []
                for f in range(len(self.dto_feat)):
                    self.idx = f + 1
                    self.info = DTOInfo(dto_path, self.idx)
                    self.infolist.append(self.info)
                
                #dto_attr = sub_vlayer.dataProvider().fields().toList()
                dto_attr = [QgsField("Datetime",QVariant.String, 'String', 80)]
                
                dtolayer = QgsVectorLayer("Polygon?crs=epsg:4326", sat_id, "memory")
                dtolayer_data = dtolayer.dataProvider()
                dtolayer.startEditing()
                dtolayer_data.addAttributes(dto_attr)
                dtolayer.updateFields()
                dtolayer_data.addFeatures(self.dto_feat)
                
                for i,f in zip(self.infolist, dtolayer.getFeatures()):
                    id=f.id()
                    attrib={(len(dto_attr)-1):i}
                    dtolayer.dataProvider().changeAttributeValues({id:attrib})
                    
                dtolayer.commitChanges()
                
                dtolayers.append(dtolayer)


#zoom to layer
extent = QgsRectangle()
extent.setMinimal()
for layer in dtolayers:
    extent.combineExtentWith(layer.extent())
QgsMapCanvas().setExtent(extent)
QgsMapCanvas().refresh()

#get WPP information based on layer extent
def get_wpp(extent):
    global wppgdf, xmin, xmax, ymin, ymax
    wpp_path = basemapPath + '//' + 'wpp_juni_2011_fix.shp'
    wppgdf = gpd.read_file(wpp_path)
    xmin = extent.xMinimum()
    xmax = extent.xMaximum()
    ymin = extent.yMinimum()
    ymax = extent.yMaximum()
    
    wpp_filter = wppgdf.cx[xmin:xmax, ymin:ymax]
    wpp_list = [wpp[-3:] for wpp in wpp_filter['NAMA_WPP']]

    if len(wpp_list) == 1:
        wpp = 'WPP NRI ' + wpp_list[0]
    elif len(wpp_list) == 2:
        wpp = 'WPP NRI ' + wpp_list[0] + ' & ' + wpp_list[1]
    elif len(wpp_list) > 2:
        wpp = 'WPP NRI ' + wpp_list[0] + ', ' + wpp_list[1] + ' & ' + wpp_list[2]
    else:
        pass
    
    return wpp

def layout_dto():
    #open layout 
    layout = QgsProject.instance().layoutManager().layouts()[0]
    
    title_exp = """[%upper(to_date_indonesian("Datetime", 7) + ' PUKUL ' + format_date((to_datetime(left("Datetime", 19))) + to_interval('7 hours'), 'hh:mm:ss') + ' WIB')%]"""
    
    #add title map
    title_item = sip.cast(layout.itemById("judul"), QgsLayoutItemLabel)
    title_item.setText(u'PETA AREA DETEKSI CITRA RADAR ' + sat + ' DI PERAIRAN ' + wpp + ' ' + '\r\nPERIODE ' + title_exp)
    
    note_exp = """[%title(to_date_indonesian("Datetime", (7-12)))%] sekitar pukul [%CASE WHEN to_time(substr("Datetime", 12, 8)) >  to_time('06:21:00') AND to_time(substr("Datetime", 12, 8)) <  to_time('18:21:00') THEN '06:00 WIB' ELSE '20:00 WIB' END%]"""
    
    #add note
    note_item = sip.cast(layout.itemById("note"), QgsLayoutItemLabel)
    note_item.setText('CATATAN:\nNotifikasi citra dapat diakuisisi atau tidak:\n' + note_exp)
    
    #setup extent on main map    
    map_item = sip.cast(layout.itemById("map"), QgsLayoutItemMap)
    extent.scale(2)
    map_item.zoomToExtent(extent)
    
    atlas_exp = """(format_date(to_datetime(left("Datetime", 19))+to_interval('7 hours'), 'yyyyMMdd_hhmmss'))||'_dto'"""
    
    layout.atlas().setCoverageLayer(dtolayer)
    layout.atlas().setEnabled(True)
    layout.atlas().setFilenameExpression(atlas_exp)
    
    iface.openLayoutDesigner(layout)
    
wpp = get_wpp(extent)
layout_dto()

# qgs.exitQgis()

print ('-------------------')
print ('Layout telah dibuat')
