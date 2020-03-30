from datetime import datetime, timedelta


class RadarInfo:
    def __init__(self, rasterBaseName):
        self.rdr = rasterBaseName[0:3]
        if self.rdr == 'CSK':
            self.rdr_name = 'COSMO-SkyMed'
            self.mode = {
                'WR': 'ScanSAR Wide Region',
                'HR': 'ScanSAR Huge Region',
                'S2': 'Enhanced Spotlight',
                'PP': 'Ping Pong',
                'HI': 'Himage',
            }

            self.con = rasterBaseName[4:5]
            self.pola = rasterBaseName[12:14]

            self.tgl = rasterBaseName[33:35]
            self.bln = rasterBaseName[31:33]
            self.thn = rasterBaseName[27:31]
            self.j = rasterBaseName[35:37]
            self.m = rasterBaseName[37:39]
            self.d = rasterBaseName[39:41]

            self.rdr_fn = f"{self.rdr_name} {self.con}"
            self.rdr_mode = f'{self.rdr_fn}, {self.mode[self.pola]}'

        elif self.rdr == 'Rad' or self.rdr == 'RS2':
            self.rdr_name = 'RADARSAT-2'
            self.mode = {
                '': '',
                'SN': 'ScanSAR Narrow',
                'FW': 'Wide Fine',
                'S2': 'Spotlight',
                'SC': 'ScanSAR',
                'SW': 'ScanSAR Wide',
                'WD': 'Wide',
                'UF': 'Ultrafine',
                'XF': 'Extra Fine',
                'EH': 'Extended High',
                'SQ': 'Standar Quad Polarization',
                'MF': 'Multi Look Fine',
            }

            self.rdr_fn = self.rdr_name

            if self.rdr == 'RS2':
                self.con = rasterBaseName[2:3]
                self.pola = rasterBaseName[32:34]

                self.tgl = rasterBaseName[42:44]
                self.bln = rasterBaseName[40:42]
                self.thn = rasterBaseName[36:40]
                self.j = rasterBaseName[45:47]
                self.m = rasterBaseName[47:49]
                self.d = rasterBaseName[49:51]

                self.rdr_mode = f'{self.rdr_fn}, {self.mode[self.pola]}'

            elif self.rdr == 'Rad':
                self.con = rasterBaseName[9:10]
                self.pola = ''

                self.tgl = rasterBaseName[53:55]
                self.bln = rasterBaseName[50:52]
                self.thn = rasterBaseName[45:49]
                self.j = rasterBaseName[56:58]
                self.m = rasterBaseName[59:61]
                self.d = rasterBaseName[62:64]

                self.rdr_mode = self.rdr_fn

        elif self.rdr[:2] == 'S1':
            self.rdr_name = 'Sentinel 1'
            self.mode = {
                'SM': 'Stripmap',
                'IW': 'Interferometric Wide Swath',
                'EW': 'Extra Wide Swath',
                'WV': 'Wave',
            }
            self.con = rasterBaseName[2:3]
            self.pola = rasterBaseName[4:6]

            self.tgl = rasterBaseName[23:25]
            self.bln = rasterBaseName[21:23]
            self.thn = rasterBaseName[17:21]
            self.j = rasterBaseName[26:28]
            self.m = rasterBaseName[28:30]
            self.d = rasterBaseName[30:32]

            self.rdr_fn = f'{self.rdr_name}{self.con}'
            self.rdr_mode = f'{self.rdr_fn}, {self.mode[self.pola]}'

        self.utc_datetime = datetime.strptime(f"{self.thn}-{self.bln}-{self.tgl} {self.j}:{self.m}:{self.d}", "%Y-%m-%d %H:%M:%S")

        self.GMT_7 = 7
        self.result_local_datetime = self.utc_datetime + timedelta(hours=self.GMT_7)
        self.u = str(self.result_local_datetime)
        self.thn_local = self.u[:4]
        self.bln_local = self.u[5:7]
        self.tgl_local = self.u[8:10]
        self.jam_local = self.u[11:13]
        self.utc = f"{self.thn}{self.bln}{self.tgl}_{self.j}{self.m}{self.d}"
        self.local = f"{self.thn_local}{self.bln_local}{self.tgl_local}_{self.jam_local}{self.m}{self.d}"
