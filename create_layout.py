import os

option = input("\nPilih tipe project (ship/oils/dto): ")

layoutship_path = "layout_ship.py"
layoutoils_path = "layout_oils.py"
layoutdto_path = "layout_dto.py"

if option == 'ship':
    os.system(f'python-qgis {layoutship_path}')
elif option == 'oils':
    os.system(f'python-qgis {layoutoils_path}')
else:
    os.system(f'python-qgis {layoutdto_path}')

input()
