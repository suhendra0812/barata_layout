from datetime import datetime, timedelta
import dateutil


class RadarInfo:
    def __init__(self, rasterBaseName):
        name_list = rasterBaseName.split("_")
        self.rdr = name_list[0]

        if self.rdr[:3] == 'CSK':
            self.rdr_name = 'COSMO-SkyMed'
            self.cons = self.rdr[-1]
            self.sensor = {
                'WR': 'ScanSAR Wide Region',
                'HR': 'ScanSAR Huge Region',
                'S2': 'Enhanced Spotlight',
                'PP': 'Ping Pong',
                'HI': 'Himage',
            }

            self.pola = name_list[5]
            self.mode = name_list[3]

            s_datetime = dateutil.parser.parse(name_list[8])

            self.tgl = s_datetime.strftime('%d')
            self.bln = s_datetime.strftime('%m')
            self.thn = s_datetime.strftime('%Y')
            self.j = s_datetime.strftime('%H')
            self.m = s_datetime.strftime('%M')
            self.d = s_datetime.strftime('%S')

            self.rdr_fn = f"{self.rdr_name} {self.cons}"
            self.rdr_mode = f'{self.rdr_fn}, {self.sensor[self.mode]}'

        elif self.rdr == 'RS2' or self.rdr == 'Radarsat-2':
            self.rdr_name = 'RADARSAT-2'
            self.sensor = {
                '': '',
                'SCN': 'ScanSAR Narrow',
                'F0W': 'Wide Fine',
                'S2': 'Spotlight',
                'SC': 'ScanSAR',
                'SCW': 'ScanSAR Wide',
                'WD': 'Wide',
                'UF': 'Ultrafine',
                'XF': 'Extra Fine',
                'EH': 'Extended High',
                'SQ': 'Standar Quad Polarization',
                'MF': 'Multi Look Fine',
            }

            self.rdr_fn = self.rdr_name

            if self.rdr == 'RS2':
                self.pola = name_list[-3]
                self.beam = name_list[4]
                self.mode = self.beam[:-1]

                s_date = name_list[5]
                s_time = name_list[6]
                s_datetime = dateutil.parser.parse(f'{s_date}{s_time}')

                self.tgl = s_datetime.strftime('%d')
                self.bln = s_datetime.strftime('%m')
                self.thn = s_datetime.strftime('%Y')
                self.j = s_datetime.strftime('%H')
                self.m = s_datetime.strftime('%M')
                self.d = s_datetime.strftime('%S')

                self.rdr_mode = f'{self.rdr_fn}, {self.sensor[self.mode]}'

            elif self.rdr == 'Radarsat-2':
                self.rdr_name = 'RADARSAT-2'
                self.pola = ''
                self.mode = ''

                s_datetime = dateutil.parser.parse(''.join(name_list[-7:-1]))

                self.tgl = s_datetime.strftime('%d')
                self.bln = s_datetime.strftime('%m')
                self.thn = s_datetime.strftime('%Y')
                self.j = s_datetime.strftime('%H')
                self.m = s_datetime.strftime('%M')
                self.d = s_datetime.strftime('%S')

                self.rdr_mode = self.rdr_fn

        elif self.rdr[:2] == 'S1':
            self.rdr_name = 'Sentinel-1'
            self.cons = self.rdr[-1]
            self.sensor = {
                'SM': 'StripMap',
                'IW': 'Interferometric Wide Swath',
                'EW': 'Extra Wide Swath',
                'WV': 'Wave',
            }
            self.mode = name_list[1]
            self.pola = name_list[3]

            s_datetime = dateutil.parser.parse(name_list[4])

            self.tgl = s_datetime.strftime('%d')
            self.bln = s_datetime.strftime('%m')
            self.thn = s_datetime.strftime('%Y')
            self.j = s_datetime.strftime('%H')
            self.m = s_datetime.strftime('%M')
            self.d = s_datetime.strftime('%S')

            self.rdr_fn = f'{self.rdr_name}{self.cons}'
            self.rdr_mode = f'{self.rdr_fn}, {self.sensor[self.mode]}'

        self.utc_datetime = s_datetime

        self.GMT_7 = 7
        self.result_local_datetime = self.utc_datetime + timedelta(hours=self.GMT_7)
        self.u = str(self.result_local_datetime)
        self.thn_local = self.u[:4]
        self.bln_local = self.u[5:7]
        self.tgl_local = self.u[8:10]
        self.jam_local = self.u[11:13]
        self.utc = f"{self.thn}{self.bln}{self.tgl}_{self.j}{self.m}{self.d}"
        self.local = f"{self.thn_local}{self.bln_local}{self.tgl_local}_{self.jam_local}{self.m}{self.d}"
