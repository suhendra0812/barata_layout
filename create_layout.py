import os

option = input("\nPilih tipe project (ship/oils/dto): ")

layoutdto_path = "layout_dto.py"
runlayout_path = "run_layout.py"

if option == 'dto':
    os.system(f'python-qgis {layoutdto_path}')
else:
    os.system(f'python-qgis {runlayout_path} {option}')

input()
