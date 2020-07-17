import os

layoutship_path = "layouts/layout_ship.py"
layoutoils_path = "layouts/layout_oils.py"
layoutdto_path = "layouts/layout_dto.py"

while True:
    option = input("\nPilih tipe project (ship/oils/dto): ")
    if option.lower() == 'ship':
        os.system(f'python-qgis {layoutship_path}')
        break
    elif option.lower() == 'oils':
        os.system(f'python-qgis {layoutoils_path}')
        break
    elif option.lower() == 'dto':
        os.system(f'python-qgis {layoutdto_path}')
        break
    else:
        print('Tipe project yang Anda masukkan tidak sesuai')

input('\nKetik ENTER untuk keluar!')
