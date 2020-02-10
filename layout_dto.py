from datetime import datetime, timedelta
import sip
import geopandas as gpd
import glob

#source paths
basePath = "D:/BARATA/"
basemapPath = basePath + '//' + '1.basemaps'
templatePath = basePath + '//' + '4.templates'

sys.path.append(basePath)
import read_kml

#get project information
project = QgsProject.instance()
project_path = project.fileName()
projectFileInfo = QFileInfo(project_path)
projectbaseName = projectFileInfo.baseName()
data = projectbaseName[-4:]

#define root in project
root = QgsProject.instance().layerTreeRoot()
dataGroup = root.findGroups()[0]
basemapGroup = root.findGroups()[1]

#remove layer from layer panel
if len(dataGroup.findLayers()) > 0:
    for i in dataGroup.children():
        dataGroup.removeChildNode(i)
else:
    pass
    
#remove registry layer history
registryLayers = QgsProject.instance().mapLayers().keys()
legendLayers = root.findLayerIds()
layerToRemove = set(registryLayers) - set(legendLayers)
QgsProject.instance().removeMapLayers(list(layerToRemove))

dto_path = QFileDialog.getOpenFileName(None, "Select DTO Directory", basePath, 'DTO Files (*.kml *.shp)')[0]

#data_folder = QFileDialog.getExistingDirectory(None, "Select DTO Directory", basePath + "2.seonse_outputs")

print ('Sumber data:')
print (dto_path)

#list layer
#dto_list = glob.glob(data_folder + '\\' + '*.kml')

#sat = QInputDialog.getText(None, 'Satellite Option', 'Pilih jenis satelit (cosmo/radarsat)')[0]
#if sat == 'cosmo':
#    sat_id = 0
#elif sat == 'radarsat':
#    sat_id = 1

def extract_info(dto_path, idx):
    global sat, sat_id, tgl_sensing, bln_sensing, thn_sensing, jam_sensing, tgl_notif, bln_notif, thn_notif, jam_notif, m, d
    
    dto_info = read_kml.dto(dto_path, idx)
    if dto_info['Satellite'] == 'RADARSAT-2':
        sat = 'RADARSAT-2'
        sat_id = 'RS'
        time = dto_info.get('Start UTC Time')
        sensing_utc = datetime.strptime(time[:19], '%Y-%m-%dT%H:%M:%S')
    else:
        sat = 'COSMO-SKYMED'
        sat_id = 'CS'
        time = dto_info.get('Sensing Start')
        sensing_utc = datetime.strptime(time[:19], '%Y-%m-%d %H:%M:%S')
        
    sensing_local = sensing_utc + timedelta(hours=7)
    notif_local = sensing_local - timedelta(hours=12)


    tgl_sensing = "{:02d}".format(sensing_local.day)
    bln_sensing = "{:02d}".format(sensing_local.month)
    thn_sensing = "{:04d}".format(sensing_local.year)
    jam_sensing = "{:02d}".format(sensing_local.hour)

    tgl_notif = "{:02d}".format(notif_local.day)
    bln_notif = "{:02d}".format(notif_local.month)
    thn_notif = "{:04d}".format(notif_local.year)
    jam_notif = "{:02d}".format(notif_local.hour)

    m = "{:02d}".format(sensing_local.minute)
    d = "{:02d}".format(sensing_local.second)
    
    return time

#dictionary
Bulan={'01':'JANUARI','02':'FEBRUARI','03':'MARET','04':'APRIL','05':'MEI','06':'JUNI','07':'JULI','08':'AGUSTUS','09':'SEPTEMBER','10':'OKTOBER','11':'NOVEMBER','12':'DESEMBER'}

layer = QgsVectorLayer(dto_path, os.path.basename(dto_path)[:-4], 'ogr')
subLayers = layer.dataProvider().subLayers()

dtolayers = []
for subLayer in subLayers:
    name = subLayer.split('!!::!!')[1]
    if name[:4] == 'PROG' or name == 'swath-1':
        uri = "%s|layername=%s" % (dto_path, name)
        #Create layer
        sub_vlayer = QgsVectorLayer(uri, name, 'ogr')
        sublayer_feat = [feat for feat in sub_vlayer.getFeatures()]
        if len(sublayer_feat) == 1:
            dto_feat = sublayer_feat
        elif len(sublayer_feat) > 1:
            dto_feat = sublayer_feat[1:]
        feat_len = len(dto_feat)
        
        datelist = []
        for f in range(len(dto_feat)):
            idx = f + 1
            date = extract_info(dto_path, idx)
            datelist.append(date)
        
        #dto_attr = sub_vlayer.dataProvider().fields().toList()
        dto_attr = [QgsField("Datetime",QVariant.String, 'String', 80)]
        
        dtolayer = QgsVectorLayer("Polygon?crs=epsg:4326", sat_id, "memory")
        dtolayer_data = dtolayer.dataProvider()
        dtolayer.startEditing()
        dtolayer_data.addAttributes(dto_attr)
        dtolayer.updateFields()
        dtolayer_data.addFeatures(dto_feat)
        
        for i,f in zip(datelist, dtolayer.getFeatures()):
            id=f.id()
            attrib={(len(dto_attr)-1):i}
            dtolayer.dataProvider().changeAttributeValues({id:attrib})
            
        dtolayer.commitChanges()
        
        dtolayers.append(dtolayer)
        
        #Add layer to map
        QgsProject.instance().addMapLayer(dtolayer, False)
        
        #add ship layer to 'DTO' group
        dataGroup.addLayer(dtolayer)
        
        #load style to the layer
        dtolayer.loadNamedStyle(templatePath + '//' + "template_multi_dto_layer.qml")

#zoom to layer
extent = QgsRectangle()
extent.setMinimal()
for layer in dtolayers:
    extent.combineExtentWith(layer.extent())
iface.mapCanvas().setExtent(extent)
iface.mapCanvas().refresh()

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

print ('-------------------')
print ('Layout telah dibuat')
