from zipfile import ZipFile
from xml.etree import ElementTree
from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
import glob
from itertools import groupby

#dto_path = r"D:\BARATA\6.dto\cosmo_skymed\201909\20190915\natuna_20190915_himage_1504_6814.kml"


class DTO:
    def __init__(self, dto_path, i):
        with open(dto_path) as dto:
            dto_content = dto.read()
            tree = ElementTree.fromstring(dto_content)
            kmlns = tree.tag.split('}')[0][1:]
            name_elems = tree.findall(".//{%s}name" % kmlns)
            def check_string(text):
                return any([True if text in name.text else False for name in name_elems])
            
            if name_elems[3].text[:4] == 'PROG':
                b_elems = tree.findall(".//{%s}b" % kmlns)
                desc = [b.text for b in b_elems]
                info_list = desc[2:]

                def split_condition(x):
                    return x in {' '}

                grouper = groupby(info_list, key=split_condition)
                info_grouped = dict(enumerate((list(j) for i, j in grouper if not i), 1))

                info = info_grouped[i]

                pr_id = info[0]
                ar_counter = info[1]
                sensing_start = info[2]
                sensing_stop = info[3]
                sensor_mode = info[4]
                satellite = info[5]
                orbit_direction = info[6]
                look_side = info[7]
                look_angle = info[8]
                beam = info[9]

                self.dto_dict = {
                    'PR ID': pr_id,
                    'AR Counter': ar_counter,
                    'Sensing Start': sensing_start,
                    'Sensing Stop': sensing_stop,
                    'Sensor Mode': sensor_mode,
                    'Satellite': satellite,
                    'Orbit Direction': orbit_direction,
                    'Look Side': look_side,
                    'Look Angle': look_angle,
                    'Beam': beam,
                }

            elif name_elems[0].text[:10] == 'RADARSAT-2':
                desc_elems = tree.findall(".//{%s}description" % kmlns)

                info_list = []
                for desc_elem in desc_elems:
                    desc = desc_elem.text.split('\n')[1:-1]

                    desc_dict = {}
                    for d in desc:
                        x = d.split(': ')
                        desc_dict[x[0]] = x[1]
                    info_list.append(desc_dict)

                self.dto_dict = info_list[1:][i-1]

            elif check_string('Cosmo-SkyMed'):
                edata_elems = tree.findall('.//{%s}ExtendedData' % kmlns)
                self.dto_dict = {}
                for i, data in enumerate(edata_elems[i], start=1):
                        name = data.get('name')
                        for value in data:
                                self.dto_dict.update({name: value.text})
                
                self.dto_dict['Sensor'] = self.dto_dict['Sensor'].split('-')[0].strip()
                self.dto_dict['Sensor Mode'] = self.dto_dict.pop('Sensor')
                self.dto_dict['Beam'] = self.dto_dict.pop('SensorMode')
                self.dto_dict['Start'] = self.dto_dict['Start'].replace('T', ' ')
                self.dto_dict['End'] = self.dto_dict['End'].replace('T', ' ')
                self.dto_dict['Sensing Start'] = self.dto_dict.pop('Start')
                self.dto_dict['Sensing Stop'] = self.dto_dict.pop('End')
                self.dto_dict['Orbit Direction'] = self.dto_dict.pop('Pass')
                self.dto_dict['Look Side'] = self.dto_dict.pop('Slew')
                self.dto_dict['Look Angle'] = self.dto_dict.pop('LookAngle')

    def to_dict(self):
        return self.dto_dict

#data_path = r"X:\2.seonse_outputs\cosmo_skymed\201812\kepri_20181207_23*"


class AIS:
    def __init__(self, data_path):
        longitude = []
        latitude = []
        shipnumber = []
        targetlength = []
        ais_mmsi = []
        geometry = []

        zipfilelist = glob.glob(f'{data_path}/*SHIPKML.zip')
        if len(zipfilelist) > 0:
            zipfilepath = zipfilelist[0]
            shipfilepath = glob.glob(f'{data_path}/*SHIP.shp')[0]

            with ZipFile(zipfilepath) as theZip:
                fileNames = theZip.namelist()
                for fileName in fileNames:
                    if fileName.endswith('kml'):
                        content = theZip.open(fileName).read()
                        tree = ElementTree.fromstring(content)
                        kmlns = tree.tag.split('}')[0][1:]
                        data_elems = tree.findall(".//{%s}Data" % kmlns)
                        point_elems = tree.findall(".//{%s}Point" % kmlns)
                        for child in point_elems:
                            for subchild in child:
                                coords = (subchild.text).split(' ')
                                x_coord = float(coords[0])
                                y_coord = float(coords[1])
                                geom = Point(x_coord, y_coord)
                                longitude.append(x_coord)
                                latitude.append(y_coord)
                                geometry.append(geom)
                        for data in data_elems:
                            name = data.get('name')
                            if name == 'AIS MMSI':
                                mmsi = data.find(".//{%s}value" % kmlns).text
                                if mmsi != 'N/A':
                                    aismmsi = int(mmsi)
                                else:
                                    aismmsi = None
                                ais_mmsi.append(aismmsi)
                            if name == 'Ship Number':
                                number = data.find(".//{%s}value" % kmlns).text
                                shipnumber.append(int(number))
                            if name == 'Target Length':
                                length = data.find(".//{%s}value" % kmlns).text
                                targetlength.append(float(length))

            ais_dict = {
                'LON_CENTRE': longitude,
                'LAT_CENTRE': latitude,
                'SHIP_ID': shipnumber,
                'LENGTH': targetlength,
                'AIS_MMSI': ais_mmsi,
            }
            aisdf = pd.DataFrame(ais_dict)
            aisdf['AIS_MMSI'] = aisdf['AIS_MMSI'].where(pd.notnull(aisdf['AIS_MMSI']), None)
            self.shipgdf = gpd.read_file(shipfilepath)
            self.shipgdf['AIS_MMSI'] = aisdf['AIS_MMSI']
            self.shipgdf.to_file(shipfilepath)

    def to_gdf(self):
        return self.shipgdf
