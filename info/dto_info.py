import os, sys
from datetime import datetime, timedelta

# source paths
SCRIPT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_PATH = os.path.dirname(SCRIPT_PATH)

sys.path.append(SCRIPT_PATH)

from utils import read_kml


class DTOInfo:
    def __init__(self, dto_path, idx):
        self.dto_info = read_kml.DTO(dto_path, idx).to_dict()
        if self.dto_info['Satellite'] == 'RADARSAT-2':
            self.sat = 'RADARSAT-2'
            self.sat_id = 'RS'
            self.time = self.dto_info.get('Start UTC Time')
            self.sensing_utc = datetime.strptime(self.time[:19], '%Y-%m-%dT%H:%M:%S')
        else:
            self.sat = 'COSMO-SkyMed'
            self.sat_id = 'CS'
            self.time = self.dto_info.get('Sensing Start')
            self.sensing_utc = datetime.strptime(self.time[:19], '%Y-%m-%d %H:%M:%S')

        self.sensing_local = self.sensing_utc + timedelta(hours=7)
        self.notif_local = self.sensing_local - timedelta(hours=12)

        self.tgl_sensing = "{:02d}".format(self.sensing_local.day)
        self.bln_sensing = "{:02d}".format(self.sensing_local.month)
        self.thn_sensing = "{:04d}".format(self.sensing_local.year)
        self.jam_sensing = "{:02d}".format(self.sensing_local.hour)

        self.tgl_notif = "{:02d}".format(self.notif_local.day)
        self.bln_notif = "{:02d}".format(self.notif_local.month)
        self.thn_notif = "{:04d}".format(self.notif_local.year)
        self.jam_notif = "{:02d}".format(self.notif_local.hour)

        self.m = "{:02d}".format(self.sensing_local.minute)
        self.d = "{:02d}".format(self.sensing_local.second)

        self.local = f'{self.thn_sensing}{self.bln_sensing}{self.tgl_sensing}_{self.jam_sensing}{self.m}{self.d}'
