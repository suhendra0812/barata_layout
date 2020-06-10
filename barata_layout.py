from qgis.core import (QgsApplication,
                       QgsProject,
                       QgsRectangle,
                       QgsRasterLayer,
                       QgsLayerTreeLayer,
                       QgsVectorLayer,
                       QgsField,
                       QgsGeometry,
                       QgsPointXY,
                       QgsVectorFileWriter,
                       QgsLayoutItemMap,
                       QgsLayoutItemMapOverview,
                       QgsLayoutItemLabel,
                       QgsRasterRange)
from qgis.gui import QgsMapCanvas
from qgis.utils import iface
from PyQt5.QtCore import QFileInfo, QVariant
from PyQt5.QtWidgets import QFileDialog
from datetime import datetime, timedelta
import geopandas as gpd
import numpy as np
import pandas as pd
import os
import glob
import sip


class QgsApp:
    def __init__(self, path):
        QgsApplication.setPrefixPath(path, True)
        self.qgs = QgsApplication([], False)

    def start(self):
        self.qgs.initQgis()

    def quit(self):
        self.qgs.exitQgis()


class FileDialog:
    def __init__(self, base_path):
        self.base_path = base_path

    def open(self, type='folder'):
        if type == 'dto':
            self.path = QFileDialog.getOpenFileName(
                None, "Select DTO Directory", self.base_path, 'DTO Files (*.kml *.shp)')[0]
        else:
            self.path = QFileDialog.getExistingDirectory(
                None, 'Select Data Directory', self.base_path)[:-4] + '*'
        return self.path


class Project:
    def __init__(self, project_path=None):
        # get project information
        if project_path != None:
            QgsProject.instance().read(project_path)
        else:
            pass
        self.projectPath = QgsProject.instance().fileName()
        self.projectBasename = QFileInfo(self.projectPath).baseName()
        self.projectType = self.projectBasename[-4:]

        # define group in project
        self.dataGroup = QgsProject.instance().layerTreeRoot().findGroups()[0]
        self.basemapGroup = QgsProject.instance(
        ).layerTreeRoot().findGroups()[1]

    def getProjectPath(self):
        return self.projectPath

    def getProjectBasename(self):
        self.projectBasename

    def getProjectType(self):
        return self.projectType

    def getDataGroup(self):
        return self.dataGroup

    def getBasemapGroup(self):
        return self.basemapGroup

    # remove layer from layer panel
    def removeLayerPanel(self):
        if len(self.dataGroup.findLayers()) > 0:
            for i in self.dataGroup.children():
                self.dataGroup.removeChildNode(i)
        else:
            pass

        if len(self.basemapGroup.findLayers()) > 3:
            self.rasterlayerRemove = self.basemapGroup.findLayers()[2:-1]
            for layer in self.rasterlayerRemove:
                self.basemapGroup.removeChildNode(layer)
        else:
            pass

    # remove registry layer history
    def removeLayerHistory(self):
        self.registryLayers = QgsProject.instance().mapLayers().keys()
        self.legendLayers = QgsProject.instance().layerTreeRoot().findLayerIds()
        self.layerToRemove = set(self.registryLayers) - set(self.legendLayers)
        QgsProject.instance().removeMapLayers(list(self.layerToRemove))

    # save project to specific directory
    def saveProject(self, output_path):
        QgsProject.instance().write(output_path)


class DataList:
    # list layer
    def __init__(self, base_path):
        self.base_path = base_path

    def getRasterList(self):
        self.rasterList = glob.glob(f'{self.base_path}\\*.tif')
        return self.rasterList

    def getShipList(self):
        self.shipList = glob.glob(f'{self.base_path}\\*SHIP.shp')
        return self.shipList

    def getOilList(self):
        self.oilList = glob.glob(f'{self.base_path}\\*OIL.shp')
        return self.oilList

    def getWindList(self):
        self.windList = glob.glob(f'{self.base_path}\\*Wind.gml')
        return self.windList


class LayerExtent:
    def __init__(self, layer_list):
        self.layer_list = layer_list

    def getExtent(self):
        # set up extent
        self.extent = QgsRectangle()
        self.extent.setMinimal()

        for layer in self.layer_list:
            # zoom to raster layer
            self.extent.combineExtentWith(layer.extent())

        # set extent to canvas
        QgsMapCanvas().setExtent(self.extent)
        QgsMapCanvas().refresh()

        return self.extent


class RasterLayer:
    def __init__(self, raster_list):
        self.rasterbasename_list = []
        self.rasterlayer_list = []

        for raster_path in raster_list:
            rasterbasename = QFileInfo(raster_path).baseName()
            rasterlayer = QgsRasterLayer(raster_path, rasterbasename)
            if not rasterlayer.isValid():
                print("rasterlayer is not valid")

            self.rasterbasename_list.append(rasterbasename)
            self.rasterlayer_list.append(rasterlayer)

    def getRasterBasename(self):
        return self.rasterbasename_list

    def getRasterLayer(self):
        return self.rasterlayer_list


class LoadRasterLayer:
    def __init__(self, layer, group):
        QgsProject.instance().addMapLayer(layer, False)

        # remove NoData value
        layer.dataProvider().setNoDataValue(1, 0)
        layer.dataProvider().setUserNoDataValue(1, [QgsRasterRange(0, 0)])

        # add raster layer to 'Basemap' group in 2nd order
        group.insertChildNode(2, QgsLayerTreeLayer(layer))


class WindData:
    def __init__(self, wind_list):
        # read wind data 'gml' in a list
        self.windgdf = gpd.GeoDataFrame(
            pd.concat([gpd.read_file(wind) for wind in wind_list], ignore_index=True))
        if self.windgdf[['speed', 'meridionalSpeed', 'zonalSpeed']].isnull().all().all():
            self.windrange = self.dire = 'n/a'
        else:
            self.windgdf['speed'] = self.windgdf['speed'].astype(float)
            self.windgdf['meridionalSpeed'] = self.windgdf['meridionalSpeed'].astype(
                float)
            self.windgdf['zonalSpeed'] = self.windgdf['zonalSpeed'].astype(
                float)

            # calculate wind direction using atan2 formula
            self.windgdf['direction'] = (np.arctan2(
                self.windgdf['meridionalSpeed'], self.windgdf['zonalSpeed']))*(180/np.pi) + 180

            # calculate wind speed (min, max, mean) and direction
            self.wind_sp = self.windgdf['speed']
            self.wind_dir = self.windgdf['direction']
            self.dir_mean = self.wind_dir.mean()
            self.wind_min = self.wind_sp.min()
            self.wind_max = self.wind_sp.max()
            self.wmin = float(f"{self.wind_min:.2f}")
            self.wmax = float(f"{self.wind_max:.2f}")
            self.windmin = str(self.wmin)
            self.windmax = str(self.wmax)
            self.windrange = f'{self.windmin} - {self.windmax} m/s'

            # define mean wind direction
            if self.dir_mean < 180:
                self.ar = self.dir_mean + 180
            elif self.dir_mean > 180:
                self.ar = self.dir_mean - 180

            # define wind direction value to wind direction name
            if self.ar > 22.5 and self.ar <= 67.5:
                self.dire = "Timur Laut"
            elif self.ar > 67.5 and self.ar <= 112.5:
                self.dire = "Timur"
            elif self.ar > 112.5 and self.ar <= 157.5:
                self.dire = "Tenggara"
            elif self.ar > 157.5 and self.ar <= 202.5:
                self.dire = "Selatan"
            elif self.ar > 202.5 and self.ar <= 247.5:
                self.dire = "Barat Daya"
            elif self.ar > 247.5 and self.ar <= 292.5:
                self.dire = "Barat"
            elif self.ar > 292.5 and self.ar <= 337.5:
                self.dire = "Barat Laut"
            else:
                self.dire = "Utara"

    def getWindGeoDataFrame(self):
        return self.windgdf


class DataLayer:
    def __init__(self, data_list):
        self.datagdf = gpd.GeoDataFrame(pd.concat(
            [gpd.read_file(data) for data in data_list], sort=False, ignore_index=True))

        self.feat_list = []
        self.attr_list = []
        self.layer_list = []

        for data_path in data_list:
            baseName = QFileInfo(data_path).baseName()

            layer = QgsVectorLayer(data_path, baseName, 'ogr')
            self.layer_list.append(layer)

            # compile feature and attribute of layer(s) to a list
            for feat in layer.getFeatures():
                self.feat_list.append(feat)
            for attr in layer.dataProvider().fields().toList():
                self.attr_list.append(attr)

    def getFeatList(self):
        return self.feat_list

    def getAttrList(self):
        return self.attr_list

    def getLayerList(self):
        return self.layer_list

    def getGeoDataFrame(self):
        return self.datagdf

    def getFeatExtent(self):
        if any(self.datagdf.geometry.geom_type == 'Point'):
            if len(self.datagdf) == 1:
                self.xmin = self.datagdf.geometry.x.min() - 0.001
                self.xmax = self.datagdf.geometry.x.max() + 0.001
                self.ymin = self.datagdf.geometry.y.min() - 0.001
                self.ymax = self.datagdf.geometry.y.max() + 0.001
            elif len(self.datagdf) > 1:
                self.xmin = self.datagdf.geometry.x.min()
                self.xmax = self.datagdf.geometry.x.max()
                self.ymin = self.datagdf.geometry.y.min()
                self.ymax = self.datagdf.geometry.y.max()
        else:
            if len(self.datagdf) == 1:
                self.xmin = self.datagdf.geometry.centroid.x.min() - 0.001
                self.xmax = self.datagdf.geometry.centroid.x.max() + 0.001
                self.ymin = self.datagdf.geometry.centroid.y.min() - 0.001
                self.ymax = self.datagdf.geometry.centroid.y.max() + 0.001
            elif len(self.datagdf) > 1:
                self.xmin = self.datagdf.geometry.centroid.x.min()
                self.xmax = self.datagdf.geometry.centroid.x.max()
                self.ymin = self.datagdf.geometry.centroid.y.min()
                self.ymax = self.datagdf.geometry.centroid.y.max()

        return self.xmin, self.xmax, self.ymin, self.ymax


class DTOLayer:
    def __init__(self, dto_path, info_list=None):
        self.baseName = QFileInfo(dto_path).baseName()
        self.layer = QgsVectorLayer(dto_path, self.baseName, 'ogr')
        self.subLayers = self.layer.dataProvider().subLayers()

        self.sublayer_list = []
        self.subfeat_list = []
        self.subattr_list = []

        for subLayer in self.subLayers:
            name = subLayer.split('!!::!!')[1]
            if name[:4] == 'PROG':
                uri = "%s|layername=%s" % (dto_path, name)

                sub_layer = QgsVectorLayer(uri, name, 'ogr')
                for feat in sub_layer.getFeatures():
                    if feat.attributes()[:2][1] != None:
                        self.subfeat_list.append(feat)

                sub_attr = sub_layer.dataProvider().fields().toList()

                self.sublayer_list.append(sub_layer)
                self.subattr_list.append(sub_attr)

            elif name[:5] == 'swath':
                uri = "%s|layername=%s" % (dto_path, name)

                sub_layer = QgsVectorLayer(uri, name, 'ogr')
                sub_feat = [feat for feat in sub_layer.getFeatures()]
                sub_attr = sub_layer.dataProvider().fields().toList()

                self.sublayer_list.append(sub_layer)
                self.subfeat_list.extend(sub_feat)
                self.subattr_list.append(sub_attr)

        self.dtoattr_list = [
            QgsField("Satellite", QVariant.String, 'String', 80),
            QgsField("Mode", QVariant.String, 'String', 80),
            QgsField("Start Time", QVariant.String, 'String', 80),
            QgsField("Stop Time", QVariant.String, 'String', 80),
            QgsField("Direction", QVariant.String, 'String', 80),
            QgsField("Look Side", QVariant.String, 'String', 80),
            QgsField("Look Angle", QVariant.Double, "double", 10, 3),
            QgsField("Beam", QVariant.String, 'String', 80),
        ]

        self.dtolayer = QgsVectorLayer(
            "Polygon?crs=epsg:4326", self.baseName, "memory")
        self.dtolayer_data = self.dtolayer.dataProvider()
        self.dtolayer.startEditing()
        self.dtolayer_data.addAttributes(self.dtoattr_list)
        self.dtolayer.updateFields()
        self.dtolayer_data.addFeatures(self.subfeat_list)

        self.dtoattr_list = self.dtolayer.dataProvider().fields().toList()

        if info_list != None:
            for i, f in zip(info_list, self.dtolayer.getFeatures()):
                sat = i.dto_info['Satellite']
                mode = i.dto_info['Sensor Mode']
                beam = i.dto_info['Beam']
                if sat == 'RADARSAT-2':
                    start = i.dto_info['Start UTC Time']
                    stop = i.dto_info['Stop UTC Time']
                    dire = i.dto_info['Pass Direction']
                    side = i.dto_info['Satellite Orientation']
                    angle = i.dto_info['Incidence Angle']
                else:
                    start = i.dto_info['Sensing Start']
                    stop = i.dto_info['Sensing Stop']
                    dire = i.dto_info['Orbit Direction']
                    side = i.dto_info['Look Side']
                    angle = i.dto_info['Look Angle']

                id = f.id()
                attrib = {
                    0: sat,
                    1: mode,
                    2: start,
                    3: stop,
                    4: dire,
                    5: side,
                    6: angle,
                    7: beam,
                }
                self.dtolayer.dataProvider(
                ).changeAttributeValues({id: attrib})
        self.dtolayer.commitChanges()

        self.dtofeat_list = [feat for feat in self.dtolayer.getFeatures()]

    def getFeatList(self):
        return self.dtofeat_list

    def getAttrList(self):
        return self.dtoattr_list

    def getLayer(self):
        return self.dtolayer


class AggregationLayer:
    def __init__(self, feat_list, attr_list, layer_name):
        if layer_name[-4:] == 'ship':
            self.agglayer = QgsVectorLayer(
                "Point?crs=epsg:4326", layer_name, "memory")
        else:
            self.agglayer = QgsVectorLayer(
                "Polygon?crs=epsg:4326", layer_name, "memory")

        self.agglayer_data = self.agglayer.dataProvider()
        self.agglayer.startEditing()
        self.agglayer_data.addAttributes(attr_list)
        self.agglayer.updateFields()
        self.agglayer_data.addFeatures(feat_list)
        self.agglayer.commitChanges()

        # duplicate agg layer to create transmitter/non transmitter ship category
        self.aggfeat_list = list(self.agglayer.getFeatures())
        self.aggattr_list = self.agglayer.dataProvider().fields().toList()

    def getAggFeatList(self):
        return self.aggfeat_list

    def getAggAttrList(self):
        return self.aggattr_list

    def getAggLayer(self):
        return self.agglayer


class AggregationLayerV2:
    def __init__(self, data_list):
        self.data_gdf = gpd.GeoDataFrame(
            pd.concat(
                [gpd.read_file(data) for data in data_list],
                ignore_index=True,
            )
        )

    def getAggLayer(self, layer_name):
        agglayer = QgsVectorLayer(self.data_gdf.to_json(), layer_name, 'ogr')
        return agglayer


class TransmittedLayer:
    def __init__(self, feat_list, attr_list, vms_list, layer_name):
        if len(vms_list) > 0:
            self.vmsgdf = gpd.GeoDataFrame(
                pd.concat([gpd.read_file(vms) for vms in vms_list], ignore_index=True))
            try:
                self.vmsstat = self.vmsgdf[self.vmsgdf['status'] == 'vms']
            except:
                self.vmsstat = self.vmsgdf[self.vmsgdf['STATUS'] == 'VMS']

        self.trmlayer = QgsVectorLayer(
            "Point?crs=epsg:4326", layer_name, "memory")
        self.trmlayer_data = self.trmlayer.dataProvider()
        self.trmlayer.startEditing()
        self.trmlayer_data.addAttributes(attr_list)
        self.trmlayer.updateFields()
        self.trmlayer_data.addFeatures(feat_list)
        self.trmlayer.commitChanges()

        # add new field named 'DESC'
        self.trmlayer.dataProvider().addAttributes(
            [QgsField("DESC", QVariant.String, 'String', 80)])
        self.trmlayer.updateFields()

        # define if 'AIS_MMSI' column was not None, the 'DESC' column is filled by 'Transmitter', else 'Non Transmitter'
        self.trmfeat_list = list(self.trmlayer.getFeatures())
        self.trmattr_list = self.trmlayer.dataProvider().fields().toList()
        self.trmattr_len = len(self.trmattr_list)

        self.trmlayer.startEditing()
        for trmfeat in self.trmfeat_list:
            aismmsi = trmfeat.attributes()[self.trmattr_len-2]
            id = trmfeat.id()
            if aismmsi == None:
                desc = {(self.trmattr_len-1): None}
            else:
                desc = {(self.trmattr_len-1): 'AIS'}

            trmfeat_geom = trmfeat.geometry()

            if len(vms_list) > 0:
                for _, vms in self.vmsstat.iterrows():
                    vms_geom = vms.geometry
                    vms_geom_qgs = QgsGeometry.fromPointXY(
                        QgsPointXY(vms_geom.x, vms_geom.y))
                    if trmfeat_geom.intersects(vms_geom_qgs):
                        desc = {(self.trmattr_len-1): 'VMS'}

            self.trmlayer.dataProvider().changeAttributeValues({id: desc})
        self.trmlayer.commitChanges()

    def getTrmFeatList(self):
        return self.trmfeat_list

    def getTrmAttrList(self):
        return self.trmattr_list

    def getTrmLayer(self):
        return self.trmlayer


class DelimitedLayer:
    def __init__(self, data_path, layer_name):
        self.uri = (
            f"file:///{data_path}?"
            "&delimiter=,"
            "&xField=Longitude"
            "&yField=Latitude"
            "&crs=EPSG:4326"
            "&decimal"
        )
        self.delimitedlayer = QgsVectorLayer(
            self.uri, layer_name, "delimitedtext")

    def getDelimitedLayer(self):
        return self.delimitedlayer


class LoadVectorLayer:
    def __init__(self, layer, group, template_path):
        QgsProject.instance().addMapLayer(layer, False)

        # add layer to group
        group.addLayer(layer)

        # load style to the layer and show feature count
        layer.loadNamedStyle(template_path)
        QgsProject.instance().layerTreeRoot().findLayer(
            layer).setCustomProperty("showFeatureCount", True)


class ExportLayer:
    def __init__(self, layer, path):
        self.layer = layer
        self.path = path

    def to_csv(self):
        QgsVectorFileWriter.writeAsVectorFormat(
            self.layer, self.path, "utf-8", self.layer.crs(), 'csv')

    def to_shp(self):
        QgsVectorFileWriter.writeAsVectorFormat(
            self.layer, self.path, "utf-8", self.layer.crs(), "ESRI Shapefile")

    def to_kml(self):
        QgsVectorFileWriter.writeAsVectorFormat(
            self.layer, self.path, "utf-8", self.layer.crs(), "KML")


class DataElements:
    def __init__(self, project_type, datadf_path):
        if project_type == 'ship':
            if datadf_path != None:
                self.shipdf = pd.read_csv(datadf_path)

                self.ship_filter = self.shipdf.copy()
                self.ship_filter = self.ship_filter[[
                    'LON_CENTRE', 'LAT_CENTRE', 'TARGET_DIR', 'LENGTH', 'DESC', 'AIS_MMSI']]
                self.column_rename = {
                    'LON_CENTRE': 'Longitude',
                    'LAT_CENTRE': 'Latitude',
                    'TARGET_DIR': 'Heading (deg)',
                    'LENGTH': 'Panjang (m)',
                    'DESC': 'Asosiasi (AIS/VMS)',
                    'AIS_MMSI': 'MMSI',
                }
                self.ship_filter = self.ship_filter.rename(
                    columns=self.column_rename)

                self.ship_filter = self.ship_filter.round(6)
                self.ship_filter['Heading (deg)'] = self.ship_filter['Heading (deg)'].astype(
                    int)
                self.ship_filter['MMSI'] = self.ship_filter['MMSI'].astype(
                    'Int64')

                self.ship_filter.index += 1
                self.ship_filter.index.name = 'No.'

                self.ship_filter.to_csv(datadf_path)

                # get VMS count
                self.vms = self.shipdf[self.shipdf['DESC'] == 'VMS']
                self.fv = len(self.vms)

                # define ship size category
                self.ais = self.shipdf['AIS_MMSI'].isnull() == False
                self.echo = self.shipdf['AIS_MMSI'].isnull() == True
                self.fe = self.shipdf[self.echo]
                self.fa = self.shipdf[self.ais]

                # ship data selection based on size
                self.s = self.shipdf['LENGTH']
                self.se = self.fe['LENGTH']
                self.sa = self.fa['LENGTH']

                # sum untransmitted ship
                self.e6 = self.fe[(self.se <= 50)]  # kapal ikan
                self.e7 = self.fe[(self.se > 50)]  # bukan kapal ikan

                # transmitted ship selection by 50 size scale
                self.u7 = self.fa[(self.sa <= 50)]  # kapal ikan
                self.u8 = self.fa[(self.sa > 50)]  # bukan kapal ikan

                # calculate total number of ship
                self.t10 = len(self.shipdf)  # len(s) + len(ss)

                # ship classification by 10 size scale
                self.e0 = self.shipdf[(self.s <= 10)]
                self.e10 = self.shipdf[(self.s > 10) & (self.s <= 20)]
                self.e20 = self.shipdf[(self.s > 20) & (self.s <= 30)]
                self.e30 = self.shipdf[(self.s > 30) & (self.s <= 40)]
                self.e40 = self.shipdf[(self.s > 40) & (self.s <= 50)]
                self.e50 = self.shipdf[(self.s > 50)]

                # define component of ship number
                self.k0 = str(len(self.e0))
                self.k1 = str(len(self.e10))
                self.k2 = str(len(self.e20))
                self.k3 = str(len(self.e30))
                self.k4 = str(len(self.e40))
                self.k5 = str(len(self.e50))

                # total of untransmitted ship
                self.k6 = str(len(self.e6) + len(self.e7) - self.fv)

                # VMS transmitted ship
                self.k11 = str(self.fv)

                # AIS transmitted ship for <=50 and >50
                self.k7 = str(len(self.u7))
                self.k8 = str(len(self.u8))

                # total of AIS transmitted ship
                self.k9 = str(len(self.u7)+len(self.u8))

                # total number of ship
                self.k10 = str(self.t10)

            else:
                self.k0 = self.k1 = self.k2 = self.k3 = self.k4 = self.k5 = self.k6 = self.k7 = self.k8 = self.k9 = self.k10 = self.k11 = '0'

            print("\nMenghitung jumlah kapal\n")
            print(f"<10\tNon Transmitter\t\t\t= {self.k0}")
            print(f"20-30\tNon Transmitter\t\t\t= {self.k2}")
            print(f"30-40\tNon Transmitter\t\t\t= {self.k3}")
            print(f"10-20\tNon Transmitter\t\t\t= {self.k1}")
            print(f"40-50\tNon Transmitter\t\t\t= {self.k4}")
            print(f">50\tNon Transmitter\t\t\t= {self.k5}")
            print(f"\nKapal <=50 Bertransmitter AIS\t\t= {self.k7}")
            print(f"Kapal >50 Bertransmitter AIS\t\t= {self.k8}")
            print(f"\nJumlah Kapal Bertransmitter AIS\t\t= {self.k9}")
            print(f"Jumlah Kapal Bertransmitter VMS\t\t= {self.k11}")
            print(f"Jumlah Kapal Tidak Bertransmitter\t= {self.k6}")
            print(f"\nTotal jumlah kapal\t\t\t= {self.k10}")

        else:
            if datadf_path != None:
                self.oilgdf = gpd.read_file(datadf_path)

                self.oil_filter = self.oilgdf[[
                    'BARIC_LON', 'BARIC_LAT', 'LENGTH_KM', 'AREA_KM', 'WSPDMEAN', 'WDIRMEAN', 'ALARM_LEV']]
                self.column_rename = {
                    'BARIC_LON': 'Longitude',
                    'BARIC_LAT': 'Latitude',
                    'LENGTH_KM': 'Panjang (km)',
                    'AREA_KM': 'Luas (km2)',
                    'WSPDMEAN': 'Kecepatan Angin (m/s)',
                    'WDIRMEAN': 'Arah Angin (deg)',
                    'ALARM_LEV': 'Tingkat Kepercayaan',
                }
                self.oil_filter = self.oil_filter.rename(
                    columns=self.column_rename)
                self.oil_filter = self.oil_filter.round(6)

                self.oil_filter.index += 1
                self.oil_filter.index.name = 'No.'
                self.oil_filter.to_csv(f'{datadf_path[:-4]}.csv')

                # oil size stat
                self.lenmin = self.oilgdf['LENGTH_KM'].min()
                self.lenmax = self.oilgdf['LENGTH_KM'].max()

                self.widmin = self.oilgdf['AREA_KM'].min()
                self.widmax = self.oilgdf['AREA_KM'].max()

                # oil confindent stat
                self.high = self.oilgdf[self.oilgdf['ALARM_LEV'] == 'HIGH']
                self.low = self.oilgdf[self.oilgdf['ALARM_LEV'] == 'LOW']

                self.hi = len(self.high)
                self.lo = len(self.low)

            else:
                self.lenmin = self.lenmax = self.widmin = self.widmax = self.hi = self.lo = 0

            print("\nMenghitung statistik tumpahan minyak")
            print(f"\nPanjang tumpahan minyak terendah\t\t= {self.lenmin} km")
            print(f"Panjang tumpahan minyak tertinggi\t\t= {self.lenmax} km")
            print(
                f"\nLuas tumpahan minyak terendah\t\t\t= {self.widmin} km\u00B2")
            print(
                f"Luas tumpahan minyak tertinggi\t\t\t= {self.widmax} km\u00B2")
            print(
                f"\nJumlah tumpahan minyak berkepercayaan tinggi\t= {self.hi}")
            print(f"Jumlah tumpahan minyak berkepercayaan rendah\t= {self.lo}")
            print(f"\nTotal jumlah tumpahan minyak\t\t\t= {self.hi+self.lo}")

    def getShipElements(self):
        return [self.k0, self.k1, self.k2, self.k3, self.k4, self.k5, self.k6, self.k7, self.k8, self.k9, self.k10, self.k11]

    def getOilElements(self):
        return [self.hi, self.lo, self.lenmin, self.lenmax, self.widmin, self.widmax]


class WindOilLayer:
    def __init__(self, oilgdf, windgdf, oillayer):
        self.pts = windgdf.copy()
        self.polygon = oilgdf.copy()

        # create buffer of oil layer
        self.polygon.geometry = self.polygon.geometry.buffer(0.027)

        self.meanspd_in_polys = []
        self.meandir_in_polys = []
        self.maxspd_in_polys = []
        self.minspd_in_polys = []
        for _, poly in self.polygon.iterrows():
            spd_in_this_poly = []
            dir_in_this_poly = []
            for _, pt in self.pts.iterrows():
                if poly.geometry.intersects(pt.geometry):
                    speed = float(f"{pt['speed']:.2f}")
                    direction = float(f"{pt['direction']:.2f}")
                    spd_in_this_poly.append(speed)
                    dir_in_this_poly.append(direction)
            if len(spd_in_this_poly) > 0:
                self.meanspd_in_polys.append(np.mean(spd_in_this_poly))
                self.maxspd_in_polys.append(max(spd_in_this_poly))
                self.minspd_in_polys.append(min(spd_in_this_poly))
            else:
                pass

            if len(dir_in_this_poly) > 0:
                self.meandir_in_polys.append(np.mean(dir_in_this_poly))
            else:
                pass

        self.polygon['WSPDMIN'] = self.minspd_in_polys
        self.polygon['WSPDMAX'] = self.maxspd_in_polys
        self.polygon['WSPDMEAN'] = self.meanspd_in_polys
        self.polygon['WDIRMEAN'] = self.meandir_in_polys

        # compile wind stats to list
        self.spdmin = list(self.polygon['WSPDMIN'])
        self.spdmax = list(self.polygon['WSPDMAX'])
        self.spdmean = list(self.polygon['WSPDMEAN'])
        self.dirmean = list(self.polygon['WDIRMEAN'])

        self.wind_oillayer = oillayer

        self.wind_oilattr_list = [
            wind_oilattr for wind_oilattr in oillayer.dataProvider().fields().toList()]
        self.wind_oilattr_len = len(self.wind_oilattr_list)

        # add wind stats attribute fields
        self.windattr_list = [
            QgsField("WSPDMIN", QVariant.Double, "double", 10, 3),
            QgsField("WSPDMAX", QVariant.Double, "double", 10, 3),
            QgsField("WSPDMEAN", QVariant.Double, "double", 10, 3),
            QgsField("WDIRMEAN", QVariant.Double, "double", 10, 3),
        ]
        self.wind_oillayer.dataProvider().addAttributes(self.windattr_list)
        self.wind_oillayer.updateFields()

        # input wind stats to layer
        self.wind_oilfeat = self.wind_oillayer.getFeatures()
        self.wind_oillayer.startEditing()
        for i, ii, iii, iv, f in zip(self.spdmin, self.spdmax, self.spdmean, self.dirmean, self.wind_oilfeat):
            id = f.id()
            wind_oilattr = {self.wind_oilattr_len: i, self.wind_oilattr_len +
                            1: ii, self.wind_oilattr_len+2: iii, self.wind_oilattr_len+3: iv}
            self.wind_oillayer.dataProvider().changeAttributeValues({
                id: wind_oilattr})
        self.wind_oillayer.commitChanges()

    def getWindOilLayer(self):
        return self.wind_oillayer


class WPPLayer:
    def __init__(self, wpp_path, extent):
        if isinstance(extent, tuple):
            self.xmin, self.xmax, self.ymin, self.ymax = extent
        else:
            self.xmin = extent.xMinimum()
            self.xmax = extent.xMaximum()
            self.ymin = extent.yMinimum()
            self.ymax = extent.yMaximum()

        self.wppgdf = gpd.read_file(wpp_path)

        self.wpp_filter = self.wppgdf.cx[self.xmin:self.xmax,
                                         self.ymin:self.ymax]
        self.wpp_list = [wpp[-3:] for wpp in self.wpp_filter['WPP']]

        if len(self.wpp_list) == 1:
            self.wpp_area = f'WPP NRI {self.wpp_list[0]}'
        elif len(self.wpp_list) == 2:
            self.wpp_area = f'WPP NRI {self.wpp_list[0]} & {self.wpp_list[1]}'
        elif len(self.wpp_list) > 2:
            self.wpp_area = f'WPP NRI {self.wpp_list[0]}, {self.wpp_list[1]} & {self.wpp_list[2]}'
        else:
            self.wpp_area = 'LUAR INDONESIA'

    def getWPPGeoDataFrame(self):
        return self.wppgdf


class Layout:
    def __init__(self, project_type=None, method=None, feat_number=None, location=None, radar_info_list=None, wpp_layer=None, wind_data=None):
        self.bulan_dict = {
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
        self.project_type = project_type
        self.method = method
        self.feat_number = feat_number
        self.radar_info = radar_info_list
        self.wpp_layer = wpp_layer
        self.wind_data = wind_data

        if self.project_type == 'oils':
            if feat_number == 0:
                self.layout_id = [0]
            elif feat_number == 1:
                self.layout_id = [1]
            elif feat_number > 1:
                self.layout_id = [3, 2]
        else:
            self.layout_id = [0]
        self.layout_list = [(i, QgsProject.instance().layoutManager().layouts()[
                             i]) for i in self.layout_id]

    def getLayoutList(self):
        return self.layout_list

    def getTitleText(self):
        wpp = self.wpp_layer
        radar = self.radar_info[-1]
        bulan = self.bulan_dict

        if self.project_type == 'ship':
            if self.method == 'satu':
                title_txt = [
                    f'PETA SEBARAN KAPAL DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB']
            else:
                title_txt = [
                    f'PETA SEBARAN KAPAL DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB']
        else:
            if self.feat_number == 0:
                self.layout_id = [0]
            elif self.feat_number == 1:
                self.layout_id = [1]
            elif self.feat_number > 1:
                self.layout_id = [3, 2]

            if self.method == 'satu':
                if self.layout_id == [3, 2]:
                    title_txt = [f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area} (BAGIAN [%$id+1%])\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB',
                                 f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB']
                else:
                    title_txt = [
                        f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m}:{radar.d} WIB']
            else:
                if self.layout_id == [3, 2]:
                    title_txt = [f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area} (BAGIAN [%$id+1%])\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB',
                                 f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB']
                else:
                    title_txt = [
                        f'PETA DETEKSI TUMPAHAN MINYAK DI PERAIRAN {wpp.wpp_area}\nPERIODE {radar.tgl_local} {bulan[radar.bln_local]} {radar.thn_local} PUKUL {radar.jam_local}:{radar.m} WIB']

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
        if not wind == None:
            wind_txt = f'{wind.windrange}\n{wind.dire}'
        else:
            wind_txt = 'n/a\nn/a'
        return wind_txt

    def insertTitleText(self):
        title_txt = self.getTitleText()
        for layout, title in zip(self.layout_list, title_txt):
            # add title map
            title_item = sip.cast(layout[1].itemById(
                "judul"), QgsLayoutItemLabel)
            title_item.setText(title)

    def insertSourceText(self):
        source_txt = self.getSourceText()
        for layout in self.layout_list:
            # add source text
            source_item = sip.cast(layout[1].itemById(
                "sumber"), QgsLayoutItemLabel)
            source_item.setText(source_txt)

    def insertWindText(self):
        wind_txt = self.getWindText()
        for layout in self.layout_list:
            # add wind information
            wind_item = sip.cast(layout[1].itemById(
                "angin"), QgsLayoutItemLabel)
            wind_item.setText(wind_txt)

    def setMap(self, extent):
        for layout in self.layout_list:
            # setup extent on main map
            map_item = sip.cast(layout[1].itemById("map"), QgsLayoutItemMap)
            map_item.zoomToExtent(extent)

            # set the overview map
            overview_item = QgsLayoutItemMapOverview('overview', map_item)
            overview_item.setLinkedMap(map_item)

    def insertShipElements(self, ship_elements):
        for layout in self.layout_list:
            # add ship size classification
            ship_item0 = sip.cast(layout[1].itemById(
                "unit0"), QgsLayoutItemLabel)
            ship_item0.setText(ship_elements[0])
            ship_item1 = sip.cast(layout[1].itemById(
                "unit1"), QgsLayoutItemLabel)
            ship_item1.setText(ship_elements[1])
            ship_item2 = sip.cast(layout[1].itemById(
                "unit2"), QgsLayoutItemLabel)
            ship_item2.setText(ship_elements[2])
            ship_item3 = sip.cast(layout[1].itemById(
                "unit3"), QgsLayoutItemLabel)
            ship_item3.setText(ship_elements[3])
            ship_item4 = sip.cast(layout[1].itemById(
                "unit4"), QgsLayoutItemLabel)
            ship_item4.setText(ship_elements[4])
            ship_item5 = sip.cast(layout[1].itemById(
                "unit5"), QgsLayoutItemLabel)
            ship_item5.setText(ship_elements[5])

            # add number of VMS, AIS and untransmitted ship
            ship_item6 = sip.cast(layout[1].itemById(
                "unit9"), QgsLayoutItemLabel)
            ship_item6.setText(ship_elements[11])
            ship_item6 = sip.cast(layout[1].itemById(
                "unit6"), QgsLayoutItemLabel)
            ship_item6.setText(ship_elements[9])
            ship_item7 = sip.cast(layout[1].itemById(
                "unit7"), QgsLayoutItemLabel)
            ship_item7.setText(ship_elements[6])

            # add total number of ship
            ship_item8 = sip.cast(layout[1].itemById(
                "unit8"), QgsLayoutItemLabel)
            ship_item8.setText(ship_elements[10])

            data_item = sip.cast(layout[1].itemById(
                "data"), QgsLayoutItemLabel)
            if (int(ship_elements[9])) > 0 or (int(ship_elements[11])) > 0:
                data_item.setText("<Ada data>")
            else:
                data_item.setText("<Tidak ada data>")

    def setOilAreaText(self, area_txt):
        for layout in self.layout_list:
            if layout[0] == 2:
                # add area text
                area_item = sip.cast(layout[1].itemById(
                    "luas"), QgsLayoutItemLabel)
                area_item.setText(area_txt)

    def setLayoutName(self, layout_name):
        for layout in self.layout_list:
            # set layout name
            layout[1].setName(layout_name)
            if layout[0] == 3:
                layout[1].setName(f'{layout_name}_')

    def setAtlas(self, layer):
        for layout in self.layout_list:
            if layout[0] == 1:
                atlas_name = "@layout_name"
            elif layout[0] == 3:
                atlas_name = "@layout_name||@atlas_featurenumber"
            # set atlas
            layout[1].atlas().setCoverageLayer(layer)
            layout[1].atlas().setEnabled(True)
            layout[1].atlas().setFilenameExpression(atlas_name)

    def openLayout(self):
        for layout in self.layout_list:
            # open layout
            iface.openLayoutDesigner(layout[1])
            layout[1].refresh()


class LayoutDTO(Layout):
    def __init__(self, project_type=None, dtoinfo_list=None, wpp_layer=None):
        super().__init__(project_type)
        self.layout_list = super().getLayoutList()
        self.dtoinfo_list = dtoinfo_list
        self.wpp_layer = wpp_layer

    def getTitleExp(self):
        title_exp = """[%upper(to_date_indonesian("Start Time", 7) + ' PUKUL ' + format_date((to_datetime(left("Start Time", 19))) + to_interval('7 hours'), 'hh:mm:ss') + ' WIB')%]"""

        return title_exp

    def getNoteExp(self):
        note_exp = """[%title(to_date_indonesian("Start Time", (7-12)))%] sekitar pukul [%CASE WHEN to_time(substr("Start Time", 12, 8)) >  to_time('06:21:00') AND to_time(substr("Start Time", 12, 8)) <  to_time('18:21:00') THEN '06:00 WIB' ELSE '20:00 WIB' END%]"""

        return note_exp

    def getAtlasExp(self):
        atlas_exp = """substr(@project_basename, 0, -19)||(format_date(to_datetime(left("Start Time", 19))+to_interval('7 hours'), 'yyyyMMdd_hhmmss'))||'_dto'"""

        return atlas_exp

    def setMap(self, extent):
        for layout in self.layout_list:
            # setup extent on main map
            map_item = sip.cast(layout[1].itemById("map"), QgsLayoutItemMap)
            extent.scale(2)
            map_item.zoomToExtent(extent)

    def setAtlas(self, layer):
        atlas_exp = self.getAtlasExp()
        for layout in self.layout_list:
            # set atlas
            layout[1].atlas().setCoverageLayer(layer)
            layout[1].atlas().setEnabled(True)
            layout[1].atlas().setFilenameExpression(atlas_exp)

    def insertTitleText(self):
        title_exp = self.getTitleExp()
        sat = self.dtoinfo_list[0].sat
        wpp = self.wpp_layer.wpp_area
        for layout in self.layout_list:
            # add title map
            title_item = sip.cast(layout[1].itemById(
                "judul"), QgsLayoutItemLabel)
            title_item.setText(
                f'PETA AREA DETEKSI CITRA RADAR {sat.upper()} DI PERAIRAN {wpp}\r\nPERIODE {title_exp}')

    def insertNoteText(self):
        note_exp = self.getNoteExp()
        for layout in self.layout_list:
            # add note
            note_item = sip.cast(layout[1].itemById(
                "note"), QgsLayoutItemLabel)
            note_item.setText(
                f'CATATAN:\nNotifikasi citra dapat diakuisisi atau tidak:\n{note_exp}')


if __name__ == '__main__':
    pass
