import sys, os, glob
import pandas as pd

from qgis.core import QgsProject
from qgis.utils import iface
from PyQt5.QtCore import QFileInfo

# define project path and project type
project_path = QgsProject.instance().fileName()
project_basename = QFileInfo(project_path).baseName()
project_type = project_basename[-4:]

# define data folder
data_folder = os.path.dirname(project_path)

# get data list from directory based on project type
if project_type == 'oils':
    data_list = glob.glob(f'{data_folder}/*oils.csv')
    if len(data_list) > 0:
        datadf = pd.read_csv(data_list[-1])
        feat_number = len(datadf)

        if feat_number == 1:
            layout_id = [1]
        elif feat_number > 1:
            layout_id = [3, 2]

    else:
        feat_number = 0
        layout_id = [0]      
  
else:
    layout_id = [0]

layout_list = [(i, QgsProject.instance().layoutManager().layouts()[i]) for i in layout_id]

# execute open layout
for layout in layout_list:
    iface.openLayoutDesigner(layout[1])
    layout[1].refresh()
