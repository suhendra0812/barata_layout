from qgis.core import (
    QgsApplication,
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
    QgsRasterRange,
    QgsCoordinateTransformContext
)
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
    def __init__(self, base_path, method='gabungan'):
        self.base_path = base_path
        self.method = method

    def open(self, type='folder'):
        if type == 'dto':
            self.path = QFileDialog.getOpenFileName(
                None, "Select DTO Directory", self.base_path, 'DTO Files (*.kml *.shp)')[0]
        else:
            if self.method == 'satu':
                self.path = QFileDialog.getExistingDirectory(
                    None, 'Select Data Directory', self.base_path)
            elif self.method == 'gabungan':
                self.path = QFileDialog.getExistingDirectory(
                    None, 'Select Data Directory', self.base_path)[:-4] + '*'
            else:
                pass

        return self.path


class Project:
    def __init__(self, project_path=None):
        # get project information
        if project_path is not None:
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
        return self.projectBasename

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
            self.rasterlayerRemove = self.basemapGroup.findLayers()[3:-1]
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
        self.rasterList = glob.glob(f'{self.base_path}/*.tif')
        return self.rasterList

    def getShipList(self):
        self.shipList = glob.glob(f'{self.base_path}/*SHIP.shp')
        return self.shipList

    def getOilList(self):
        self.oilList = glob.glob(f'{self.base_path}/*OIL.shp')
        return self.oilList

    def getWindList(self):
        self.windList = glob.glob(f'{self.base_path}/*Wind.gml')
        return self.windList


class LayerExtent:
    def __init__(self, layer):
        if isinstance(layer, list):
            self.layer_list = layer
        elif isinstance(layer, QgsVectorLayer):
            self.layer_list = [layer]

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


class AggregationData:
    def __init__(self, data_list):
        self.data_list = data_list
        self.data_gdf = gpd.GeoDataFrame(
            pd.concat(
                [gpd.read_file(data) for data in self.data_list],
                ignore_index=True,
            )
        )
        self.data_gdf.drop_duplicates(inplace=True, ignore_index=True)

    def getGeoDataFrame(self):
        return self.data_gdf

    def getLayer(self, layer_path, layer_name):
        layer = QgsVectorLayer(layer_path, layer_name, 'ogr')
        return layer


class WindData(AggregationData):
    def __init__(self, wind_list):
        super().__init__(wind_list)

        # read wind data 'gml' in a list
        self.wind_gdf = super().getGeoDataFrame()

        if self.wind_gdf[['speed', 'meridionalSpeed', 'zonalSpeed']].isnull().all().all():
            self.windrange = self.dire = 'n/a'
        else:
            self.wind_gdf['speed'] = self.wind_gdf['speed'].astype(float)
            self.wind_gdf['meridionalSpeed'] = self.wind_gdf['meridionalSpeed'].astype(
                float)
            self.wind_gdf['zonalSpeed'] = self.wind_gdf['zonalSpeed'].astype(
                float)

            # calculate wind direction using atan2 formula
            self.wind_gdf['direction'] = np.arctan2(
                self.wind_gdf['meridionalSpeed'],
                self.wind_gdf['zonalSpeed'],
            )*(180/np.pi) + 180

            # calculate wind speed (min, max, mean) and direction
            self.wind_sp = self.wind_gdf['speed']
            self.wind_dir = self.wind_gdf['direction']
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


class ShipData(AggregationData):
    def __init__(self, data_list, vms_list):
        super().__init__(data_list)

        self.ship_gdf = super().getGeoDataFrame()
        self.vms_list = vms_list

        self.ship_gdf['DESC'] = [
            'AIS' if i is not None else None for i in self.ship_gdf['AIS_MMSI']]

        if len(self.vms_list) > 0:
            vms_gdf = gpd.GeoDataFrame(
                pd.concat(
                    [gpd.read_file(vms) for vms in self.vms_list],
                    ignore_index=True,
                )
            )
            vms_gdf.drop_duplicates(inplace=True, ignore_index=True)

            shipvms_gdf = gpd.sjoin(self.ship_gdf, vms_gdf, how='left')

            for i in range(len(shipvms_gdf)):
                if shipvms_gdf.loc[i, 'status'] == 'vms':
                    self.ship_gdf.loc[i, 'DESC'] = 'VMS'

    def getShipGeoDataFrame(self):
        return self.ship_gdf

    def getShipDataFrame(self):
        shipfilter_df = self.ship_gdf.copy()
        shipfilter_df = shipfilter_df[[
            'LON_CENTRE', 'LAT_CENTRE', 'TARGET_DIR', 'LENGTH', 'DESC', 'AIS_MMSI']]
        shipfilter_df.rename(
            columns={
                'LON_CENTRE': 'Longitude',
                'LAT_CENTRE': 'Latitude',
                'TARGET_DIR': 'Heading (deg)',
                'LENGTH': 'Panjang (m)',
                'DESC': 'Asosiasi (AIS/VMS)',
                'AIS_MMSI': 'MMSI',
            },
            inplace=True,
        )

        shipfilter_df.index += 1
        shipfilter_df.index.name = 'No.'

        return shipfilter_df


class OilData(WindData):
    def __init__(self, oil_list, wind_list):
        AggregationData.__init__(self, oil_list)
        self.oil_gdf = AggregationData.getGeoDataFrame(self)

        if len(wind_list) > 0:
            WindData.__init__(self, wind_list)
            wind_gdf = WindData.getGeoDataFrame(self)

            windoil_gdf = gpd.sjoin(self.oil_gdf, wind_gdf, how='left')
            wspd_min = windoil_gdf.groupby(id)['speed'].agg('min')
            wspd_max = windoil_gdf.groupby(id)['speed'].agg('max')
            wspd_mean = windoil_gdf.groupby(id)['speed'].agg('mean')
            wdir_mean = windoil_gdf.groupby(id)['direction'].agg('mean')

            self.oil_gdf['WSPDMIN'] = wspd_min
            self.oil_gdf['WSPDMAX'] = wspd_max
            self.oil_gdf['WSPDMEAN'] = wspd_mean
            self.oil_gdf['WDIRMEAN'] = wdir_mean
        else:
            self.oil_gdf['WSPDMIN'] = [
                np.nan for i in range(len(self.oil_gdf))]
            self.oil_gdf['WSPDMAX'] = [
                np.nan for i in range(len(self.oil_gdf))]
            self.oil_gdf['WSPDMEAN'] = [
                np.nan for i in range(len(self.oil_gdf))]
            self.oil_gdf['WDIRMEAN'] = [
                np.nan for i in range(len(self.oil_gdf))]

    def getOilGeoDataFrame(self):
        return self.oil_gdf

    def getOilDataFrame(self):
        oilfilter_gdf = self.oil_gdf.copy()
        oilfilter_gdf = oilfilter_gdf[[
            'BARIC_LON', 'BARIC_LAT', 'LENGTH_KM', 'AREA_KM', 'WSPDMEAN', 'WDIRMEAN', 'ALARM_LEV']]
        oilfilter_gdf.rename(
            columns={
                'BARIC_LON': 'Longitude',
                'BARIC_LAT': 'Latitude',
                'LENGTH_KM': 'Panjang (km)',
                'AREA_KM': 'Luas (km2)',
                'WSPDMEAN': 'Kecepatan Angin (m/s)',
                'WDIRMEAN': 'Arah Angin (deg)',
                'ALARM_LEV': 'Tingkat Kepercayaan',
            },
            inplace=True,
        )

        oilfilter_gdf.index += 1
        oilfilter_gdf.index.name = 'No.'
        return oilfilter_gdf


class DTOData(AggregationData):
    def __init__(self, dto_path, info_list=None):
        self.dto_path = dto_path

        gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
        self.dto_gdf = gpd.read_file(dto_path, driver='KML')

        if not self.dto_gdf['Name'].str.contains('swath').any():
            self.dto_gdf = self.dto_gdf.loc[1:]
        else:
            self.dto_gdf = self.dto_gdf[~self.dto_gdf['Name'].str.contains(
                'frame')]

        if info_list != None:
            self.dto_gdf = gpd.GeoDataFrame(geometry=self.dto_gdf.geometry)
            sat_list = []
            mode_list = []
            beam_list = []
            start_list = []
            stop_list = []
            dire_list = []
            side_list = []
            angle_list = []

            for i in range(len(info_list)):
                sat = info_list[i].dto_info['Satellite']
                mode = info_list[i].dto_info['Sensor Mode']
                beam = info_list[i].dto_info['Beam']
                if sat == 'RADARSAT-2':
                    start = info_list[i].dto_info['Start UTC Time']
                    stop = info_list[i].dto_info['Stop UTC Time']
                    dire = info_list[i].dto_info['Pass Direction']
                    side = info_list[i].dto_info['Satellite Orientation']
                    angle = info_list[i].dto_info['Incidence Angle']
                else:
                    start = info_list[i].dto_info['Sensing Start']
                    stop = info_list[i].dto_info['Sensing Stop']
                    dire = info_list[i].dto_info['Orbit Direction']
                    side = info_list[i].dto_info['Look Side']
                    angle = info_list[i].dto_info['Look Angle']

                sat_list.append(sat)
                mode_list.append(mode)
                beam_list.append(beam)
                start_list.append(start)
                stop_list.append(stop)
                dire_list.append(dire)
                side_list.append(side)
                angle_list.append(angle)

            self.dto_gdf["Satellite"] = sat_list
            self.dto_gdf["Mode"] = mode_list
            self.dto_gdf["Start Time"] = start_list
            self.dto_gdf["Stop Time"] = stop_list
            self.dto_gdf["Direction"] = dire_list
            self.dto_gdf["Look Side"] = side_list
            self.dto_gdf["Look Angle"] = angle_list
            self.dto_gdf["Beam"] = beam_list

    def getDTOGeoDataFrame(self):
        return self.dto_gdf


class WPPData:
    def __init__(self, wpp_path, extent):
        if isinstance(extent, tuple):
            self.xmin, self.xmax, self.ymin, self.ymax = extent
        elif isinstance(extent, np.ndarray):
            self.xmin, self.ymin, self.xmax, self.ymax = extent
        else:
            self.xmin = extent.xMinimum()
            self.xmax = extent.xMaximum()
            self.ymin = extent.yMinimum()
            self.ymax = extent.yMaximum()

        self.wpp_gdf = gpd.read_file(wpp_path)

        self.wpp_filter = self.wpp_gdf.cx[self.xmin:self.xmax,
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
        return self.wpp_gdf


class DataElements:
    def __init__(self, data_gdf):
        self.data_gdf = data_gdf

    def getShipElements(self):
        if self.data_gdf is not None:
            # get VMS count
            self.vms = self.data_gdf[self.data_gdf['DESC'] == 'VMS']
            self.fv = len(self.vms)

            # define ship size category
            self.ais = self.data_gdf['AIS_MMSI'].isnull() == False
            self.echo = self.data_gdf['AIS_MMSI'].isnull() == True
            self.fe = self.data_gdf[self.echo]
            self.fa = self.data_gdf[self.ais]

            # ship data selection based on size
            self.s = self.data_gdf['LENGTH']
            self.se = self.fe['LENGTH']
            self.sa = self.fa['LENGTH']

            # sum untransmitted ship
            self.e6 = self.fe[(self.se <= 50)]  # kapal ikan
            self.e7 = self.fe[(self.se > 50)]  # bukan kapal ikan

            # transmitted ship selection by 50 size scale
            self.u7 = self.fa[(self.sa <= 50)]  # kapal ikan
            self.u8 = self.fa[(self.sa > 50)]  # bukan kapal ikan

            # calculate total number of ship
            self.t10 = len(self.data_gdf)  # len(s) + len(ss)

            # ship classification by 10 size scale
            self.e0 = self.data_gdf[(self.s <= 10)]
            self.e10 = self.data_gdf[(self.s > 10) & (self.s <= 20)]
            self.e20 = self.data_gdf[(self.s > 20) & (self.s <= 30)]
            self.e30 = self.data_gdf[(self.s > 30) & (self.s <= 40)]
            self.e40 = self.data_gdf[(self.s > 40) & (self.s <= 50)]
            self.e50 = self.data_gdf[(self.s > 50)]

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

        return [self.k0, self.k1, self.k2, self.k3, self.k4, self.k5, self.k6, self.k7, self.k8, self.k9, self.k10, self.k11]

    def getOilElements(self):
        if self.data_gdf is not None:
            # oil size stat
            self.lenmin = self.data_gdf['LENGTH_KM'].min()
            self.lenmax = self.data_gdf['LENGTH_KM'].max()

            self.widmin = self.data_gdf['AREA_KM'].min()
            self.widmax = self.data_gdf['AREA_KM'].max()

            # oil confindent stat
            self.high = self.data_gdf[self.data_gdf['ALARM_LEV'] == 'HIGH']
            self.low = self.data_gdf[self.data_gdf['ALARM_LEV'] == 'LOW']

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

        return [self.hi, self.lo, self.lenmin, self.lenmax, self.widmin, self.widmax]


class LoadLayer:
    def __init__(self, project, layer, template=None):
        self.data_group = project.getDataGroup()
        self.basemap_group = project.getBasemapGroup()
        
        self.layer = layer
        QgsProject.instance().addMapLayer(layer, False)

        if template is not None:
            self.template = template

    def addRasterToMap(self):
        # remove NoData value
        self.layer.dataProvider().setNoDataValue(1, 0)
        self.layer.dataProvider().setUserNoDataValue(1, [QgsRasterRange(0, 0)])

        # add raster layer to 'Basemap' group in 2nd order
        self.basemap_group.insertChildNode(3, QgsLayerTreeLayer(self.layer))
    
    def addVectorToMap(self):
        # add layer to group
        self.data_group.addLayer(self.layer)

        # load style to the layer and show feature count
        self.layer.loadNamedStyle(self.template)
        QgsProject.instance().layerTreeRoot().findLayer(
            self.layer).setCustomProperty("showFeatureCount", True)


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
        title_exp = """[%upper(format_date("Start Time"+ to_interval('7 hours'), 'dd MMMM yyyy pukul hh:mm:ss WIB', 'id'))%]"""

        return title_exp

    def getNoteExp(self):
        note_exp = """[%title(format_date("Start Time", 'dd MMMM yyyy', 'id'))%] sekitar pukul [%CASE WHEN to_time("Start Time") >=  to_time('06:21:00') AND to_time("Start Time") <=  to_time('18:21:00') THEN '06:00 WIB' ELSE '20:00 WIB' END%] \nSensor Mode : [% "Mode" %]"""

        return note_exp

    def getAtlasExp(self):
        atlas_exp = """substr(@project_basename, 0, -19)||(format_date("Start Time"+to_interval('7 hours'), 'yyyyMMdd_hhmmss'))||'_dto'"""

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
