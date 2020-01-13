import sys, os, glob
import pandas as pd

script_path = 'D:\\BARATA\\11.barata_layout'
sys.path.append(script_path)
from barata_layout import Project, Layout

#define project type and project path
project_type = Project().getProjectType()
project_path = Project().getProjectPath()

#get data list from directory based on project type
if project_type == 'ship':
	data_list = glob.glob(f'{os.path.dirname(project_path)}\\*ship.csv')
else:
	data_list = glob.glob(f'{os.path.dirname(project_path)}\\*oils.csv')

#define feature number
if len(data_list) > 0:
	datadf = pd.read_csv(data_list[-1])
	feat_number = len(datadf)
else:
	feat_number = 0

#execute open layout
Layout(project_type=project_type, feat_number=feat_number).openLayout()

if __name__ == '__main__':
    pass



