from qgis.core import *
from qgis.gui import *
from datetime import datetime, timedelta

@qgsfunction(args='auto', group='Date and Time')
def to_date_indonesian(time, delta, feature, parent):
    """
    Extract and convert month of the datetime to Indonesian format.
    <h2>Example usage:</h2>
    <ul>
      <li>to_date_indonesian('2019-01-01 00:00:00', 7) -> 01 Januari 2019</li>
      <li>to_date_indonesian("field1") -> 01 Februari 2019</li>
    </ul>
    """
    try:
        utc = datetime.strptime(time[:19], '%Y-%m-%dT%H:%M:%S')
    except:
        utc = datetime.strptime(time[:19], '%Y-%m-%d %H:%M:%S')
    local = utc + timedelta(hours = delta)
    tgl = "{:02d}".format(utc.day)
    bln = "{:02d}".format(utc.month)
    thn = "{:04d}".format(utc.year)
    jam = "{:02d}".format(utc.hour)
    
    m = "{:02d}".format(utc.minute)
    d = "{:02d}".format(utc.second)
    
    Bulan={'01':'Januari','02':'Februari','03':'Maret','04':'April','05':'Mei','06':'Juni','07':'Juli','08':'Agustus','09':'September','10':'Oktober','11':'November','12':'Desember'}
    
    date_indonesian = tgl + ' ' + Bulan[bln] + ' ' + thn
    
    return date_indonesian
