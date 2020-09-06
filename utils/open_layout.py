import sys, os, glob
import pandas as pd

# source paths
SCRIPT_PATH = os.getcwd()
BASE_PATH = os.path.dirname(SCRIPT_PATH)

sys.path.append(SCRIPT_PATH)
from barata.barata_layout import Project, Layout

# define project type and project path
project_type = Project().getProjectType()
project_path = Project().getProjectPath()

# define data folder
data_folder = os.path.dirname(project_path)

# get data list from directory based on project type
if project_type == 'oils':
    data_list = glob.glob(f'{data_folder}/*oils.csv')
    if len(data_list) > 0:
        datadf = pd.read_csv(data_list[-1])
        feat_number = len(datadf)
    else:
        feat_number = 0

    # execute open layout for oils
    Layout(project_type=project_type, feat_number=feat_number).openLayout()
else:
    # execute open layout
    Layout(project_type=project_type).openLayout()

if __name__ == '__main__':
    pass
