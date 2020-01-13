# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 18:06:05 2019

@author: WSBARATA01
"""

from zipfile import ZipFile
from xml.etree import ElementTree
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import glob
from itertools import groupby

#dto_path = r"X:\10.dto\KML_test\arafura_20190916_v1.kml"
                
class DTO:
    def __init__(self, dto_path, i):
        self.__dto_content = open(dto_path).read()
        self.__tree = ElementTree.fromstring(self.__dto_content)
        self.__kmlns = self.__tree.tag.split('}')[0][1:]
        self.__name_elems = self.__tree.findall(".//{%s}name" % self.__kmlns)
        if self.__name_elems[0].text[:10] == 'RADARSAT-2':
            self.__desc_elems = self.__tree.findall(".//{%s}description" % self.__kmlns)
            self.__dto_dict = {}
            self.__desc = self.__desc_elems[1].text.split('\n')[1:-1]
            for i in self.__desc:
                self.__x = i.split(': ')
                self.__dto_dict[self.__x[0]] = self.__x[1]
        else:
            self.__b_elems = self.__tree.findall(".//{%s}b" % self.__kmlns)
            self.__desc = [b.text for b in self.__b_elems]
            self.__info_list = self.__desc[2:]
            
            def split_condition(x):
                return x in {' '}
            
            self.__grouper = groupby(info_list, key=split_condition)
            self.__info_grouped = dict(enumerate((list(j) for i, j in self.__grouper if not i), 1))
            
            self.__info = self.__info_grouped[i]
            
            self.__pr_id = self.__info[0]
            self.__ar_counter = self.__info[1]
            self.__sensing_start = self.__info[2]
            self.__sensing_stop = self.__info[3]
            self.__sensor_mode = self.__info[4]
            self.__satellite = self.__info[5]
            self.__orbit_direction = self.__info[6]
            self.__look_side = self.__info[7]
            self.__look_angle = self.__info[8]
            self.__beam = self.__info[9]
            
            self.__dto_dict = {'PR ID':self.__pr_id,
                        'AR Counter':self.__ar_counter,
                        'Sensing Start':self.__sensing_start,
                        'Sensing Stop':self.__sensing_stop,
                        'Sensor Mode':self.__sensor_mode,
                        'Satellite':self.__satellite,
                        'Orbit Direction':self.__orbit_direction,
                        'Look Side':self.__look_side,
                        'Look Angle':self.__look_angle,
                        'Beam':self.__beam}

    def to_dict(self):
        return self.__dto_dict

#data_path = r"X:\2.seonse_outputs\cosmo_skymed\201812\kepri_20181207_23*"
    
class AIS:
    def __init__(self, data_path):
        self.__longitude = []
        self.__latitude = []
        self.__shipnumber = []
        self.__targetlength = []
        self.__ais_mmsi = []
        self.__geometry = []

        self.__zipfilelist = glob.glob(f'{data_path}\\*SHIPKML.zip')
        if len(self.__zipfilelist) > 0:
            self.__zipfilepath = self.__zipfilelist[0]
            self.__shipfilepath = glob.glob(f'{data_path}\\*SHIP.shp')[0]

            with ZipFile(self.__zipfilepath) as theZip:
                self.__fileNames = theZip.namelist()
                for fileName in self.__fileNames:
                    if fileName.endswith('kml'):
                        self.__content = theZip.open(fileName).read()
                        self.__tree = ElementTree.fromstring(self.__content)
                        self.__kmlns = self.__tree.tag.split('}')[0][1:]
                        self.__data_elems = self.__tree.findall(".//{%s}Data" % self.__kmlns)
                        self.__point_elems = self.__tree.findall(".//{%s}Point" % self.__kmlns)
                        for child in self.__point_elems:
                            for subchild in child:
                                self.__coords = (subchild.text).split(' ')
                                self.__x_coord = float(self.__coords[0])
                                self.__y_coord = float(self.__coords[1])
                                self.__geom = Point(self.__x_coord, self.__y_coord)
                                self.__longitude.append(self.__x_coord)
                                self.__latitude.append(self.__y_coord)
                                self.__geometry.append(self.__geom)
                        for data in self.__data_elems:
                            self.__name = data.get('name')
                            if self.__name == 'AIS MMSI':
                                self.__mmsi = data.find(".//{%s}value" % self.__kmlns).text
                                if self.__mmsi != 'N/A':
                                    self.__aismmsi = int(self.__mmsi)
                                else:
                                    self.__aismmsi = None
                                self.__ais_mmsi.append(self.__aismmsi)
                            if self.__name == 'Ship Number':
                                self.__number = data.find(".//{%s}value" % self.__kmlns).text
                                self.__shipnumber.append(int(self.__number))
                            if self.__name == 'Target Length':
                                self.__length =  data.find(".//{%s}value" % self.__kmlns).text
                                self.__targetlength.append(float(self.__length))
                                
            self.__aisdf = pd.DataFrame({'LON_CENTRE':self.__longitude, 'LAT_CENTRE':self.__latitude, 'SHIP_ID':self.__shipnumber, 'LENGTH':self.__targetlength, 'AIS_MMSI':self.__ais_mmsi})
            self.__aisdf['AIS_MMSI'] = self.__aisdf['AIS_MMSI'].where(pd.notnull(self.__aisdf['AIS_MMSI']), None)
            self.__shipgdf = gpd.read_file(self.__shipfilepath)
            self.__shipgdf['AIS_MMSI'] =  self.__aisdf['AIS_MMSI']
            self.__shipgdf.to_file(self.__shipfilepath)

    def to_gdf(self):
        return self.__shipgdf
