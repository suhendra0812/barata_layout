from qgis.core import QgsProject, QgsRectangle, QgsRasterLayer, QgsLayerTreeLayer, QgsVectorLayer, QgsField, QgsGeometry, QgsPointXY, QgsVectorFileWriter, QgsLayoutItemMap, QgsLayoutItemMapOverview, QgsLayoutItemLabel, QgsRasterRange
from qgis.gui import QgsMapCanvas
from qgis.utils import iface
from PyQt5.QtCore import QFileInfo, QVariant
from PyQt5.QtWidgets import QInputDialog, QFileDialog
from datetime import datetime, timedelta
import geopandas as gpd
import numpy as np
import pandas as pd
import os
import glob
import sip


class Project:
    def __init__(self, project_path=None):
        #get project information
        if project_path != None:
            QgsProject.instance().read(project_path)
        else:
            pass
        self.__projectPath = QgsProject.instance().fileName()
        self.__projectBasename = QFileInfo(self.__projectPath).baseName()
        self.__projectType = self.__projectBasename[-4:]
    
        #define group in project
        self.__dataGroup = QgsProject.instance().layerTreeRoot().findGroups()[0]
        self.__basemapGroup = QgsProject.instance().layerTreeRoot().findGroups()[1]
    
    def getProjectPath(self):
        return self.__projectPath

    def getProjectBasename(self):
        self.__projectBasename
    
    def getProjectType(self):
        return self.__projectType
    
    def getDataGroup(self):
        return self.__dataGroup
    
    def getBasemapGroup(self):
        return self.__basemapGroup
        
    #remove layer from layer panel
    def removeLayerPanel(self):
        if len(self.__dataGroup.findLayers()) > 0:
            for i in self.__dataGroup.children():
                self.__dataGroup.removeChildNode(i)
        else:
            pass

        if len(self.__basemapGroup.findLayers()) > 3:
            self.__rasterlayerRemove = self.__basemapGroup.findLayers()[2:-1]
            for layer in self.__rasterlayerRemove:
                self.__basemapGroup.removeChildNode(layer)
        else:
            pass
        
    #remove registry layer history
    def removeLayerHistory(self):
        self.__registryLayers = QgsProject.instance().mapLayers().keys()
        self.__legendLayers = QgsProject.instance().layerTreeRoot().findLayerIds()
        self.__layerToRemove = set(self.__registryLayers) - set(self.__legendLayers)
        QgsProject.instance().removeMapLayers(list(self.__layerToRemove))
    
    #save project to specific directory
    def saveProject(self, output_path):
        QgsProject.instance().write(output_path)
    
class DataList:
    #list layer
    def __init__(self, sourcePath):
        self.__rasterList = glob.glob(f'{sourcePath}\\*.tif')
        self.__shipList = glob.glob(f'{sourcePath}\\*SHIP.shp')
        self.__oilList = glob.glob(f'{sourcePath}\\*OIL.shp')
        self.__windList = glob.glob(f'{sourcePath}\\*Wind.gml')
    
    def getRasterList(self):
        return self.__rasterList
    
    def getShipList(self):
        return self.__shipList
        
    def getOilList(self):
        return self.__oilList
    
    def getWindList(self):
        return self.__windList
    
class RasterLayer:
    def __init__(self, raster_list):
        self.__rasterbasename_list = []
        self.__rasterlayer_list = []
        
        #set up extent
        self.__extent = QgsRectangle()
        self.__extent.setMinimal()
        
        for raster_path in raster_list:
            rasterbasename = os.path.basename(raster_path)[:-4]
            rasterlayer = QgsRasterLayer(raster_path, rasterbasename)
            if not rasterlayer.isValid():
                print("rasterlayer is not valid")
                
            self.__rasterbasename_list.append(rasterbasename)
            self.__rasterlayer_list.append(rasterlayer)
            
            #zoom to raster layer
            self.__extent.combineExtentWith(rasterlayer.extent())
        
        #set extent to canvas
        QgsMapCanvas().setExtent(self.__extent)
        QgsMapCanvas().refresh()
        
    def getRasterBasename(self):
        return self.__rasterbasename_list
        
    def getRasterLayer(self):
        return self.__rasterlayer_list
    
    def getRasterExtent(self):
        return self.__extent
    
class LoadRasterLayer:
    def __init__(self, layer, group):
        QgsProject.instance().addMapLayer(layer, False)
        
        #remove NoData value
        layer.dataProvider().setNoDataValue(1, 0)
        layer.dataProvider().setUserNoDataValue(1, [QgsRasterRange(0,0)])
                    
        #add raster layer to 'Basemap' group in 2nd order
        group.insertChildNode(2, QgsLayerTreeLayer(layer))

class RadarInfo:
    def __init__(self, rasterBaseName):
        self.__rdr = rasterBaseName[0:3]
        if self.__rdr == 'CSK':
            self.rdr_name = 'COSMO-SkyMed'
            self.mode={'WR':'ScanSAR Wide Region',
                       'HR':'ScanSAR Huge Region',
                       'S2':'Enhanced Spotlight',
                       'PP':'Ping Pong',
                       'HI':'Himage'}

            self.con=rasterBaseName[4:5]
            self.pola=rasterBaseName[12:14]
            
            self.tgl = rasterBaseName[33:35]
            self.bln = rasterBaseName[31:33]
            self.thn = rasterBaseName[27:31]
            self.j = rasterBaseName[35:37]
            self.m = rasterBaseName[37:39]
            self.d = rasterBaseName[39:41]

            self.rdr_fn = f"{self.rdr_name} {self.con}"
            self.rdr_mode = f'{self.rdr_fn}, {self.mode[self.pola]}'
            
        elif self.__rdr == 'Rad' or self.__rdr == 'RS2':
            self.rdr_name = 'RADARSAT-2'
            self.mode = {'':'',
                         'SN':'ScanSAR Narrow',
                         'FW':'Wide Fine',
                         'S2':'Spotlight',
                         'SC':'ScanSAR',
                         'SW':'ScanSAR Wide',
                         'WD':'Wide',
                         'UF':'Ultrafine',
                         'XF':'Extra Fine',
                         'EH':'Extended High',
                         'SQ':'Standar Quad Polarization',
                         'MF':'Multi Look Fine'}

            self.rdr_fn = self.rdr_name

            if self.__rdr == 'RS2':
                self.con=rasterBaseName[2:3]
                self.pola=rasterBaseName[32:34]
                
                self.tgl = rasterBaseName[42:44]
                self.bln = rasterBaseName[40:42]
                self.thn = rasterBaseName[36:40]
                self.j = rasterBaseName[45:47]
                self.m = rasterBaseName[47:49]
                self.d = rasterBaseName[49:51]

                self.rdr_mode = f'{self.rdr_fn}, {self.mode[self.pola]}'

            elif self.__rdr == 'Rad':
                self.con=rasterBaseName[9:10]
                self.pola=''

                self.tgl = rasterBaseName[53:55]
                self.bln = rasterBaseName[50:52]
                self.thn = rasterBaseName[45:49]
                self.j = rasterBaseName[56:58]
                self.m = rasterBaseName[59:61]
                self.d = rasterBaseName[62:64]

                self.rdr_mode = self.rdr_fn
            
        elif self.__rdr[:2] == 'S1':
            self.rdr_name = 'Sentinel 1'
            self.mode={'SM':'Stripmap',
                       'IW':'Interferometric Wide Swath',
                       'EW':'Extra Wide Swath',
                       'WV':'Wave'}

            self.con=rasterBaseName[2:3]
            self.pola=rasterBaseName[4:6]

            self.tgl = rasterBaseName[23:25]
            self.bln = rasterBaseName[21:23]
            self.thn = rasterBaseName[17:21]
            self.j = rasterBaseName[26:28]
            self.m = rasterBaseName[28:30]
            self.d = rasterBaseName[30:32]

            self.rdr_fn = f'{self.rdr_name}{self.con}'
            self.rdr_mode = f'{self.rdr_fn}, {self.mode[self.pola]}'
         
        self.__utc_datetime = datetime.strptime(f"{self.thn}-{self.bln}-{self.tgl} {self.j}:{self.m}:{self.d}", "%Y-%m-%d %H:%M:%S")

        self.__GMT_7 = 7
        self.__result_local_datetime = self.__utc_datetime + timedelta(hours=self.__GMT_7)
        self.__u=str(self.__result_local_datetime)
        self.thn_local=self.__u[:4]
        self.bln_local=self.__u[5:7]
        self.tgl_local=self.__u[8:10]
        self.jam_local=self.__u[11:13]
        self.utc = f"{self.thn}{self.bln}{self.tgl}_{self.j}{self.m}{self.d}"
        self.local = f"{self.thn_local}{self.bln_local}{self.tgl_local}_{self.jam_local}{self.m}{self.d}"
        
class WindData:
    def __init__(self, wind_list):
        #read wind data 'gml' in a list
        self.__windgdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(wind) for wind in wind_list], ignore_index=True))
        if self.__windgdf[['speed', 'meridionalSpeed', 'zonalSpeed']].isnull().all().all():
            self.__windrange=self.__dire= 'n/a'
        else:
            self.__windgdf['speed'] = self.__windgdf['speed'].astype(float)
            self.__windgdf['meridionalSpeed'] = self.__windgdf['meridionalSpeed'].astype(float)
            self.__windgdf['zonalSpeed'] = self.__windgdf['zonalSpeed'].astype(float)
            
            #calculate wind direction using atan2 formula
            self.__windgdf['direction'] = (np.arctan2(self.__windgdf['meridionalSpeed'], self.__windgdf['zonalSpeed']))*(180/np.pi) + 180

            #calculate wind speed (min, max, mean) and direction
            self.__wind_sp=self.__windgdf['speed']
            self.__wind_dir = self.__windgdf['direction']
            self.__dir_mean = self.__wind_dir.mean()
            self.__wind_min = self.__wind_sp.min()
            self.__wind_max = self.__wind_sp.max()
            self.__wmin = float(f"{self.__wind_min:.2f}")
            self.__wmax = float(f"{self.__wind_max:.2f}")
            self.__windmin = str(self.__wmin)
            self.__windmax = str(self.__wmax)
            self.windrange = f'{self.__windmin} - {self.__windmax} m/s'
            
            #define mean wind direction
            if self.__dir_mean < 180:
                self.__ar=self.__dir_mean + 180
            elif self.__dir_mean > 180:
                self.__ar=self.__dir_mean - 180

            #define wind direction value to wind direction name
            if self.__ar > 22.5 and self.__ar <= 67.5:
                self.dire="Timur Laut"
            elif self.__ar > 67.5 and self.__ar <= 112.5:
                self.dire="Timur"
            elif self.__ar > 112.5 and self.__ar <= 157.5:
                self.dire="Tenggara"
            elif self.__ar > 157.5 and self.__ar <= 202.5:
                self.dire="Selatan"
            elif self.__ar > 202.5 and self.__ar <= 247.5:
                self.dire="Barat Daya"
            elif self.__ar > 247.5 and self.__ar <= 292.5:
                self.dire="Barat"
            elif self.__ar > 292.5 and self.__ar <= 337.5:
                self.dire="Barat Laut"
            else:
                self.dire="Utara"
    
    def getWindGeoDataFrame(self):
        return self.__windgdf
        
class DataLayer:
    def __init__(self, data_list, layer_name=None):
        self.__datagdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(data) for data in data_list], sort=False, ignore_index=True))
        
        self.__feat_list = []
        self.__attr_list = []
        self.__layer_list = []
        
        for data_path in data_list:
            if layer_name != None:
                self.__baseName = layer_name
            else:
                self.__baseName = os.path.basename(data_path)[:-4]

            self.__layer = QgsVectorLayer(data_path, self.__baseName, 'ogr')   
            self.__layer_list.append(self.__layer)
            
            #compile feature and attribute of layer(s) to a list
            for feat in self.__layer.getFeatures():
                self.__feat_list.append(feat)
            for attr in self.__layer.dataProvider().fields().toList():
                self.__attr_list.append(attr)
    
    def getFeatList(self):
        return self.__feat_list
    
    def getAttrList(self):
        return self.__attr_list
    
    def getLayerList(self):
        return self.__layer_list
    
    def getGeoDataFrame(self):
        return self.__datagdf
    
    def getFeatExtent(self):
        if any(self.__datagdf.geometry.geom_type == 'Point'):
            if len(self.__datagdf) == 1:
                self.__xmin = self.__datagdf.geometry.x.min() - 0.001
                self.__xmax = self.__datagdf.geometry.x.max() + 0.001
                self.__ymin = self.__datagdf.geometry.y.min() - 0.001
                self.__ymax = self.__datagdf.geometry.y.max() + 0.001
            elif len(self.__datagdf) > 1:
                self.__xmin = self.__datagdf.geometry.x.min()
                self.__xmax = self.__datagdf.geometry.x.max()
                self.__ymin = self.__datagdf.geometry.y.min()
                self.__ymax = self.__datagdf.geometry.y.max()
        else:
            if len(self.__datagdf) == 1:
                self.__xmin = self.__datagdf.geometry.centroid.x.min() - 0.001
                self.__xmax = self.__datagdf.geometry.centroid.x.max() + 0.001
                self.__ymin = self.__datagdf.geometry.centroid.y.min() - 0.001
                self.__ymax = self.__datagdf.geometry.centroid.y.max() + 0.001
            elif len(self.__datagdf) > 1:
                self.__xmin = self.__datagdf.geometry.centroid.x.min()
                self.__xmax = self.__datagdf.geometry.centroid.x.max() 
                self.__ymin = self.__datagdf.geometry.centroid.y.min() 
                self.__ymax = self.__datagdf.geometry.centroid.y.max() 
        
        return self.__xmin,self.__xmax,self.__ymin,self.__ymax
        
class AggregationLayer:
    def __init__(self, feat_list, attr_list, layer_name):
        if layer_name[-4:] == 'ship':
            self.__agglayer = QgsVectorLayer("Point?crs=epsg:4326", layer_name, "memory")
        else:
            self.__agglayer = QgsVectorLayer("Polygon?crs=epsg:4326", layer_name, "memory")
            
        self.__agglayer_data = self.__agglayer.dataProvider()
        self.__agglayer.startEditing()
        self.__agglayer_data.addAttributes(attr_list)
        self.__agglayer.updateFields()
        self.__agglayer_data.addFeatures(feat_list)
        self.__agglayer.commitChanges()
        
        #duplicate agg layer to create transmitter/non transmitter ship category
        self.__aggfeat_list = list(self.__agglayer.getFeatures())
        self.__aggattr_list = self.__agglayer.dataProvider().fields().toList()
    
    def getAggFeatList(self):
        return self.__aggfeat_list
        
    def getAggAttrList(self):
        return self.__aggattr_list
        
    def getAggLayer(self):
        return self.__agglayer

class TransmittedLayer:
    def __init__(self, feat_list, attr_list, vms_list, layer_name):
        if len(vms_list) > 0:
            print ('- Ada data VMS')
            self.__vmsgdf = gpd.GeoDataFrame(pd.concat([gpd.read_file(vms) for vms in vms_list], ignore_index=True))
            try:
                self.__vmsstat = self.__vmsgdf[self.__vmsgdf['status'] == 'vms']
            except:
                self.__vmsstat = self.__vmsgdf[self.__vmsgdf['STATUS'] == 'VMS']
        else:
            print ('- Tidak ada data VMS')
                
        self.__trmlayer = QgsVectorLayer("Point?crs=epsg:4326", layer_name, "memory")
        self.__trmlayer_data = self.__trmlayer.dataProvider()
        self.__trmlayer.startEditing()
        self.__trmlayer_data.addAttributes(attr_list)
        self.__trmlayer.updateFields()
        self.__trmlayer_data.addFeatures(feat_list)
        self.__trmlayer.commitChanges()
        
        #add new field named 'DESC'
        self.__trmlayer.dataProvider().addAttributes([QgsField("DESC",QVariant.String, 'String', 80)])
        self.__trmlayer.updateFields()
        
        #define if 'AIS_MMSI' column was not None, the 'DESC' column is filled by 'Transmitter', else 'Non Transmitter'
        self.__trmfeat_list = list(self.__trmlayer.getFeatures())
        self.__trmattr_list = self.__trmlayer.dataProvider().fields().toList()
        self.__trmattr_len = len(self.__trmattr_list)
        
        self.__trmlayer.startEditing()
        for trmfeat in self.__trmfeat_list:
            self.__aismmsi = trmfeat.attributes()[self.__trmattr_len-2]
            self.__id=trmfeat.id()
            if self.__aismmsi == None:
                self.__desc = {(self.__trmattr_len-1):None}
            else:
                self.__desc = {(self.__trmattr_len-1):'AIS'}
            
            self.__trmfeat_geom = trmfeat.geometry()
            
            if len(vms_list) > 0:
                for i, vms in self.__vmsstat.iterrows():
                    self.__vms_geom = vms.geometry
                    self.__vms_geom_qgs = QgsGeometry.fromPointXY(QgsPointXY(self.__vms_geom.x, self.__vms_geom.y))
                    if self.__trmfeat_geom.intersects(self.__vms_geom_qgs):
                        self.__desc = {(self.__trmattr_len-1):'VMS'}
            else:
                pass
                        
            self.__trmlayer.dataProvider().changeAttributeValues({self.__id:self.__desc})
        self.__trmlayer.commitChanges()
    
    def getTrmFeatList(self):
        return self.__trmfeat_list
        
    def getTrmAttrList(self):
        return self.__trmattr_list
        
    def getTrmLayer(self):
        return self.__trmlayer
        
class DelimitedLayer:
    def __init__(self, data_path, layer_name):
        self.__uri = (f"file:///{data_path}?"
                      "&delimiter=,"
                      "&xField=Longitude"
                      "&yField=Latitude"
                      "&crs=EPSG:4326"
                      "&decimal")
        self.__delimitedlayer = QgsVectorLayer(self.__uri, layer_name, "delimitedtext")
    
    def getDelimitedLayer(self):
        return self.__delimitedlayer

class LoadVectorLayer:
    def __init__(self, layer, group, template_path):
        QgsProject.instance().addMapLayer(layer, False)
        
        #add layer to group
        group.addLayer(layer)
        
        #load style to the layer and show feature count
        layer.loadNamedStyle(template_path)
        QgsProject.instance().layerTreeRoot().findLayer(layer).setCustomProperty("showFeatureCount", True)  

class ExportLayer:
    def __init__(self, layer, path):
        self.layer = layer
        self.path = path
    
    def to_csv(self):
        QgsVectorFileWriter.writeAsVectorFormat(self.layer, self.path, "utf-8", self.layer.crs(), 'csv')
    
    def to_shp(self):
        QgsVectorFileWriter.writeAsVectorFormat(self.layer, self.path, "utf-8", self.layer.crs(), "ESRI Shapefile")

class DataElements:
    def __init__(self, project_type, datadf_path):
        if project_type == 'ship':
            if datadf_path != None: 
                self.__shipdf = pd.read_csv(datadf_path)
                self.__ship_filter = self.__shipdf[['LON_CENTRE', 'LAT_CENTRE', 'TARGET_DIR', 'LENGTH', 'DESC', 'AIS_MMSI']]
                self.__ship_filter = self.__ship_filter.rename(columns={'LON_CENTRE':'Longitude',
                                                                        'LAT_CENTRE':'Latitude',
                                                                        'TARGET_DIR':'Heading (deg)',
                                                                        'LENGTH':'Panjang (m)',
                                                                        'DESC':'Asosiasi (VMS/AIS)',
                                                                        'AIS_MMSI':'MMSI'})

                self.__ship_filter = self.__ship_filter.round(6)
                self.__ship_filter['Heading (deg)'] = self.__ship_filter['Heading (deg)'].astype(int)
                self.__ship_filter['MMSI'] = self.__ship_filter['MMSI'].astype('Int64')

                self.__ship_filter.index+=1
                self.__ship_filter.index.name = 'No.'
                try:
                    self.__ship_filter.to_csv(datadf_path)
                except:
                    print ('File csv info kapal sedang dibuka')
                
                #get VMS count
                self.vms = self.__ship_filter[self.__ship_filter['Asosiasi (VMS/AIS)'] == 'VMS']
                self.fv = len(self.vms)
                
                #define ship size category
                self.ais=self.__shipdf['AIS_MMSI'].isnull() == False
                self.echo=self.__shipdf['AIS_MMSI'].isnull() == True
                self.fe=self.__shipdf[self.echo]
                self.fa=self.__shipdf[self.ais]

                #ship data selection based on size
                self.s=self.__shipdf['LENGTH']
                self.se=self.fe['LENGTH']
                self.sa=self.fa['LENGTH']

                #sum untransmitted ship
                self.e6=self.fe[(self.se <= 50)]#kapal ikan
                self.e7=self.fe[(self.se > 50)]#bukan kapal ikan

                #transmitted ship selection by 50 size scale
                self.u7=self.fa[(self.sa <= 50)]#kapal ikan
                self.u8=self.fa[(self.sa > 50)]#bukan kapal ikan

                #calculate total number of ship
                self.t10=len(self.__shipdf)#len(s) + len(ss)

                #ship classification by 10 size scale
                self.e0=self.__shipdf[(self.s <=10)]
                self.e10=self.__shipdf[(self.s > 10)&(self.s <=20)]
                self.e20=self.__shipdf[(self.s > 20)&(self.s <=30)]
                self.e30=self.__shipdf[(self.s > 30)&(self.s <=40)]
                self.e40=self.__shipdf[(self.s > 40)&(self.s <=50)]
                self.e50=self.__shipdf[(self.s > 50)]

                #define component of ship number
                self.k0=str(len(self.e0))
                self.k1=str(len(self.e10))
                self.k2=str(len(self.e20))
                self.k3=str(len(self.e30))
                self.k4=str(len(self.e40))
                self.k5=str(len(self.e50))
                
                #total of untransmitted ship
                self.k6=str(len(self.e6) + len(self.e7) - self.fv)
                
                #VMS transmitted ship
                self.k11=str(self.fv)
                
                #AIS transmitted ship for <=50 and >50
                self.k7=str(len(self.u7))
                self.k8=str(len(self.u8))
                
                #total of AIS transmitted ship
                self.k9=str(len(self.u7)+len(self.u8))
                
                #total number of ship
                self.k10=str(self.t10)

            else:
                self.k0=self.k1=self.k2=self.k3=self.k4=self.k5=self.k6=self.k7=self.k8=self.k9=self.k10=self.k11 = '0'
                
            print ("\nMenghitung jumlah kapal\n")
            print (f"<10\tNon Transmitter\t\t\t= {self.k0}")
            print (f"20-30\tNon Transmitter\t\t\t= {self.k2}")
            print (f"30-40\tNon Transmitter\t\t\t= {self.k3}")
            print (f"10-20\tNon Transmitter\t\t\t= {self.k1}")
            print (f"40-50\tNon Transmitter\t\t\t= {self.k4}")
            print (f">50\tNon Transmitter\t\t\t= {self.k5}")
            print (f"\nKapal <=50 Bertransmitter AIS\t\t= {self.k7}")
            print (f"Kapal >50 Bertransmitter AIS\t\t= {self.k8}")
            print (f"\nJumlah Kapal Bertransmitter AIS\t\t= {self.k9}")
            print (f"Jumlah Kapal Bertransmitter VMS\t\t= {self.k11}")
            print (f"Jumlah Kapal Tidak Bertransmitter\t= {self.k6}")
            print (f"\nTotal jumlah kapal\t\t\t= {self.k10}")
		
        else:
            if datadf_path != None:
                self.__oilgdf = gpd.read_file(datadf_path)
                self.__oil_filter = self.__oilgdf[['BARIC_LON', 'BARIC_LAT', 'LENGTH_KM', 'AREA_KM', 'WSPDMEAN', 'WDIRMEAN', 'ALARM_LEV']]
                self.__oil_filter = self.__oil_filter.rename(columns={'BARIC_LON':'Longitude',
                                                                      'BARIC_LAT':'Latitude',
                                                                      'LENGTH_KM':'Panjang (km)',
                                                                      'AREA_KM':'Luas (km2)',
                                                                      'WSPDMEAN':'Kecepatan Angin (m/s)',
                                                                      'WDIRMEAN':'Arah Angin (deg)',
                                                                      'ALARM_LEV':'Tingkat Kepercayaan'})
                self.__oil_filter = self.__oil_filter.round(6)

                self.__oil_filter.index+=1
                self.__oil_filter.index.name = 'No.'
                try:
                    self.__oil_filter.to_csv(f'{datadf_path[:-4]}.csv')
                except:
                    print ('File csv info kapal sedang dibuka')
                
                #oil size stat
                self.lenmin = self.__oilgdf['LENGTH_KM'].min()
                self.lenmax = self.__oilgdf['LENGTH_KM'].max()
                
                self.widmin = self.__oilgdf['AREA_KM'].min()
                self.widmax = self.__oilgdf['AREA_KM'].max()

                #oil confindent stat
                self.high = self.__oilgdf[self.__oilgdf['ALARM_LEV'] == 'HIGH']
                self.low = self.__oilgdf[self.__oilgdf['ALARM_LEV'] == 'LOW']
                
                self.hi = len(self.high)
                self.lo = len(self.low)
                
            else:
                self.lenmin=self.lenmax=self.widmin=self.widmax=self.hi=self.lo=None
                
            print ("\nMenghitung statistik tumpahan minyak")
            print (f"\nPanjang tumpahan minyak terendah\t\t= {self.lenmin} km")
            print (f"Panjang tumpahan minyak tertinggi\t\t= {self.lenmax} km")
            print (f"\nLuas tumpahan minyak terendah\t\t\t= {self.widmin} km\u00B2")
            print (f"Luas tumpahan minyak tertinggi\t\t\t= {self.widmax} km\u00B2")
            print (f"\nJumlah tumpahan minyak berkepercayaan tinggi\t= {self.hi}")
            print (f"Jumlah tumpahan minyak berkepercayaan rendah\t= {self.lo}")
            print (f"\nTotal jumlah tumpahan minyak\t\t\t= {self.hi+self.lo}")			
        
    def getShipElements(self):
        return [self.k0, self.k1, self.k2, self.k3, self.k4, self.k5, self.k6, self.k7, self.k8, self.k9, self.k10, self.k11]

    def getOilElements(self):
        return [self.hi, self.lo, self.lenmin, self.lenmax, self.widmin, self.widmax]
        
class WindOilLayer:
    def __init__(self, oilgdf, windgdf, oillayer):
        self.__pts = windgdf.copy()
        self.__polygon = oilgdf.copy()
        
        #create buffer of oil layer
        self.__polygon.geometry = self.__polygon.geometry.buffer(0.027)
        
        self.__meanspd_in_polys = []
        self.__meandir_in_polys = []
        self.__maxspd_in_polys = []
        self.__minspd_in_polys = []
        for i, poly in self.__polygon.iterrows():
            self.__spd_in_this_poly = []
            self.__dir_in_this_poly = []
            for j, pt in self.__pts.iterrows():
                if poly.geometry.intersects(pt.geometry):
                    self.__speed = float(f"{pt['speed']:.2f}")
                    self.__direction = float(f"{pt['direction']:.2f}")
                    self.__spd_in_this_poly.append(self.__speed)
                    self.__dir_in_this_poly.append(self.__direction)
            if len(self.__spd_in_this_poly) > 0:
                self.__meanspd_in_polys.append(np.mean(self.__spd_in_this_poly))
                self.__maxspd_in_polys.append(max(self.__spd_in_this_poly))
                self.__minspd_in_polys.append(min(self.__spd_in_this_poly))
            else:
                pass

            if len(self.__dir_in_this_poly) > 0:
                self.__meandir_in_polys.append(np.mean(self.__dir_in_this_poly))
            else:
                pass
        
        self.__polygon['WSPDMIN'] = gpd.GeoSeries(self.__minspd_in_polys)
        self.__polygon['WSPDMAX'] = gpd.GeoSeries(self.__maxspd_in_polys)
        self.__polygon['WSPDMEAN'] = gpd.GeoSeries(self.__meanspd_in_polys)
        self.__polygon['WDIRMEAN'] = gpd.GeoSeries(self.__meandir_in_polys)
        
        #compile wind stats to list
        self.__spdmin = list(self.__polygon['WSPDMIN'])
        self.__spdmax = list(self.__polygon['WSPDMAX'])
        self.__spdmean = list(self.__polygon['WSPDMEAN'])
        self.__dirmean = list(self.__polygon['WDIRMEAN'])
        
        self.__wind_oillayer = oillayer
        
        self.__wind_oilattr_list = [wind_oilattr for wind_oilattr in oillayer.dataProvider().fields().toList()]
        self.__wind_oilattr_len = len(self.__wind_oilattr_list)
        
        #add wind stats attribute fields
        self.__wind_oillayer.dataProvider().addAttributes([QgsField("WSPDMIN",QVariant.Double, "double", 10, 3),
                                                           QgsField("WSPDMAX",QVariant.Double, "double", 10, 3),
                                                           QgsField("WSPDMEAN",QVariant.Double, "double", 10, 3),
                                                           QgsField("WDIRMEAN",QVariant.Double, "double", 10, 3)])
        self.__wind_oillayer.updateFields()
        
        #input wind stats to layer
        self.__wind_oilfeat = self.__wind_oillayer.getFeatures()
        self.__wind_oillayer.startEditing()
        for i,ii,iii,iv,f in zip(self.__spdmin,self.__spdmax,self.__spdmean,self.__dirmean,self.__wind_oilfeat):
            self.__id=f.id()
            self.__wind_oilattr={self.__wind_oilattr_len:i,self.__wind_oilattr_len+1:ii,self.__wind_oilattr_len+2:iii,self.__wind_oilattr_len+3:iv}
            self.__wind_oillayer.dataProvider().changeAttributeValues({self.__id:self.__wind_oilattr})
        self.__wind_oillayer.commitChanges()
        
    def getWindOilLayer(self):
        return self.__wind_oillayer
    
class WPPLayer:
    def __init__(self, wpp_path, extent):
        if isinstance(extent, tuple):
            self.xmin,self.xmax,self.ymin,self.ymax = extent
        else:
            self.xmin = extent.xMinimum()
            self.xmax = extent.xMaximum()
            self.ymin = extent.yMinimum()
            self.ymax = extent.yMaximum()
        
        self.__wppgdf = gpd.read_file(wpp_path)
        
        self.__wpp_filter = self.__wppgdf.cx[self.xmin:self.xmax, self.ymin:self.ymax]
        self.__wpp_list = [wpp[-3:] for wpp in self.__wpp_filter['NAMA_WPP']]

        if len(self.__wpp_list) == 1:
            self.wpp_area = f'WPP NRI {self.__wpp_list[0]}'
        elif len(self.__wpp_list) == 2:
            self.wpp_area = f'WPP NRI {self.__wpp_list[0]} & {self.__wpp_list[1]}'
        elif len(self.__wpp_list) > 2:
            self.wpp_area = f'WPP NRI {self.__wpp_list[0]}, {self.__wpp_list[1]} & {self.__wpp_list[2]}'
        else:
            self.wpp_area = 'LUAR INDONESIA'
        
    def getWPPGeoDataFrame(self):
        return self.__wppgdf

class Layout:
    def __init__(self, project_type=None, method=None, feat_number=None, location=None, radar_info_list=None, wpp_layer=None, wind_data=None):
        self.bulan_dict = {'01':'JANUARI',
                           '02':'FEBRUARI',
                           '03':'MARET',
                           '04':'APRIL',
                           '05':'MEI',
                           '06':'JUNI',
                           '07':'JULI',
                           '08':'AGUSTUS',
                           '09':'SEPTEMBER',
                           '10':'OKTOBER',
                           '11':'NOVEMBER',
                           '12':'DESEMBER'}

        self.project_type = project_type
        self.method = method
        self.feat_number = feat_number
        self.radar_info = radar_info_list
        self.wpp_layer = wpp_layer
        self.wind_data = wind_data

        if self.project_type == 'ship':
            self.__layout_id = [0] 
        else:
            if feat_number == 0:
                self.__layout_id = [0]
            elif feat_number == 1:
                self.__layout_id = [1]
            elif feat_number > 1:
                self.__layout_id = [3,2]
        self.__layout_list = [(i, QgsProject.instance().layoutManager().layouts()[i]) for i in self.__layout_id]

    def getLayoutList(self):
        return self.__layout_list

    def getTitleText(self):
        wpp = self.wpp_layer
        radar = self.radar_info[-1]
        bulan = self.bulan_dict

        if self.project_type == 'ship':
            if self.method == 'satu':
                title_txt = [f'PETA SEBARAN KAPAL DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB']
            else:
                title_txt = [f'PETA SEBARAN KAPAL DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB']
        else:
            if self.feat_number == 0:
                self.__layout_id = [0]
            elif self.feat_number == 1:
                self.__layout_id = [1]
            elif self.feat_number > 1:
                self.__layout_id = [3,2]
                  
            if self.method == 'satu':
                if self.__layout_id == [3,2]:
                    title_txt = [f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area} (BAGIAN [%$id+1%])\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB',
                                      f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB']
                else:
                    title_txt = [f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB']
            else:
                if self.__layout_id == [3,2]:
                    title_txt = [f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area} (BAGIAN [%$id+1%])\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB',
                                      f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB']
                else:
                    title_txt = [f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB']
        
        return title_txt

    def getSourceText(self):
        radar_sourcetxt = ['Sumber:']
        for i, radar in enumerate(self.radar_info):
            radar_txt = f'{i+1}. {radar.rdr_mode} ({radar.thn}-{radar.bln}-{radar.tgl}T{radar.j}:{radar.m}:{radar.d} UTC)'
            radar_sourcetxt.append(radar_txt)

        basemap_sourcetxt = f'{len(self.radar_info)+1}. Peta Rupabumi Digital Wilayah Indonesia BIG'
        radar_sourcetxt.append(basemap_sourcetxt)
        source_txt = '\n'.join(radar_sourcetxt)
        
        return source_txt

    def getWindText(self):
        wind = self.wind_data
        wind_txt = f'{wind.windrange}\n{wind.dire}'
        return wind_txt
            
    def insertTitle(self):
        title_txt = self.getTitleText()
        for layout, title in zip(self.__layout_list, title_txt):
            #add title map
            self.__title_item = sip.cast(layout[1].itemById("judul"), QgsLayoutItemLabel)
            self.__title_item.setText(title)
    
    def insertSourceText(self):
        source_txt = self.getSourceText()
        for layout in self.__layout_list:
            #add source text
            self.__source_item = sip.cast(layout[1].itemById("sumber"), QgsLayoutItemLabel)
            self.__source_item.setText(source_txt)
    
    def insertWindText(self):
        wind_txt = self.getWindText()
        for layout in self.__layout_list:
            #add wind information
            self.__wind_item = sip.cast(layout[1].itemById("angin"), QgsLayoutItemLabel)
            self.__wind_item.setText(wind_txt)

    def setMap(self, extent):
        for layout in self.__layout_list:
            #setup extent on main map    
            self.__map_item = sip.cast(layout[1].itemById("map"), QgsLayoutItemMap)
            self.__map_item.zoomToExtent(extent)
    
            #set the overview map    
            self.__overview_item = QgsLayoutItemMapOverview('overview', self.__map_item)
            self.__overview_item.setLinkedMap(self.__map_item)

    def insertShipElements(self, ship_elements):
        for layout in self.__layout_list:
            #add ship size classification
            self.__ship_item0 = sip.cast(layout[1].itemById("unit0"), QgsLayoutItemLabel)
            self.__ship_item0.setText(ship_elements[0])
            self.__ship_item1 = sip.cast(layout[1].itemById("unit1"), QgsLayoutItemLabel)
            self.__ship_item1.setText(ship_elements[1])
            self.__ship_item2 = sip.cast(layout[1].itemById("unit2"), QgsLayoutItemLabel)
            self.__ship_item2.setText(ship_elements[2])
            self.__ship_item3 = sip.cast(layout[1].itemById("unit3"), QgsLayoutItemLabel)
            self.__ship_item3.setText(ship_elements[3])
            self.__ship_item4 = sip.cast(layout[1].itemById("unit4"), QgsLayoutItemLabel)
            self.__ship_item4.setText(ship_elements[4])
            self.__ship_item5 = sip.cast(layout[1].itemById("unit5"), QgsLayoutItemLabel)
            self.__ship_item5.setText(ship_elements[5])

            #add number of VMS, AIS and untransmitted ship
            self.__ship_item6 = sip.cast(layout[1].itemById("unit9"), QgsLayoutItemLabel)
            self.__ship_item6.setText(ship_elements[11])
            self.__ship_item6 = sip.cast(layout[1].itemById("unit6"), QgsLayoutItemLabel)
            self.__ship_item6.setText(ship_elements[9])
            self.__ship_item7 = sip.cast(layout[1].itemById("unit7"), QgsLayoutItemLabel)
            self.__ship_item7.setText(ship_elements[6])

            #add total number of ship
            self.__ship_item8 = sip.cast(layout[1].itemById("unit8"), QgsLayoutItemLabel)
            self.__ship_item8.setText(ship_elements[10])

            self.__data_item = sip.cast(layout[1].itemById("data"), QgsLayoutItemLabel)
            if (int(ship_elements[9])) > 0 or (int(ship_elements[11])) > 0:
                self.__data_item.setText("<Ada data>")
            else:
                self.__data_item.setText("<Tidak ada data>")
                
    def setOilAreaText(self, area_txt):
        for layout in self.__layout_list:
            if layout[0] == 2:
                #add area text
                area_item = sip.cast(layout[1].itemById("luas"), QgsLayoutItemLabel)
                area_item.setText(area_txt)
    
    def setLayoutName(self, layout_name):
        for layout in self.__layout_list:
            #set layout name
            layout[1].setName(layout_name)
            if layout[0] == 3:
                layout[1].setName(f'{layout_name}_')
    
    def setAtlas(self, layer):
        for layout in self.__layout_list:
            if layout[0] == 1:
                self.atlas_name = "@layout_name"
            elif layout[0] == 3:
                self.atlas_name = "@layout_name||@atlas_featurenumber"
            #set atlas
            layout[1].atlas().setCoverageLayer(layer)
            layout[1].atlas().setEnabled(True)
            layout[1].atlas().setFilenameExpression(self.atlas_name)
    
    def openLayout(self):
        for layout in self.__layout_list:
            #open layout
            iface.openLayoutDesigner(layout[1])
            layout[1].refresh()
		
if __name__ == '__main__':
    pass
    


