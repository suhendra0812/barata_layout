from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Conversions')
def to_direction(value, feature, parent):
    """
    Calculates the parameter direction value(degree) and convert it to direction string.
    <h2>Example usage:</h2>
    <ul>
      <li>to_direction(0) -> Utara</li>
    </ul>
    """
    if value < 180:
        ar=value + 180
    elif value > 180:
        ar=value - 180
    if ar > 22.5 and ar <= 67.5:
            dire="Timur Laut"
    elif ar > 67.5 and ar <= 112.5:
        dire="Timur"
    elif ar > 112.5 and ar <= 157.5:
        dire="Tenggara"
    elif ar > 157.5 and ar <= 202.5:
        dire="Selatan"
    elif ar > 202.5 and ar <= 247.5:
        dire="Barat Daya"
    elif ar > 247.5 and ar <= 292.5:
        dire="Barat"
    elif ar > 292.5 and ar <= 337.5:
        dire="Barat Laut"
    else :
        dire="Utara"
        
    return dire
