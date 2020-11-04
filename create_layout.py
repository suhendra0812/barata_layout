import os

python_qgis = 'C:/OSGeo4W64/bin/python-qgis.bat'

while True:
    type_option = input("\nPilih tipe project (ship/oils/dto): ")
    if type_option.lower() == 'ship':
        layout_path = "layouts/layout_ship.py"
        break
    elif type_option.lower() == 'oils':
        layout_path = "layouts/layout_oils.py"
        break
    elif type_option.lower() == 'dto':
        layout_path = "layouts/layout_dto.py"
        break
    else:
        print('Tipe project yang Anda masukkan tidak sesuai')

print(f'\nTipe project: {type_option.lower()}')

if type_option.lower() != 'dto':
    while True:
        method_option = input('Pilih metode layout (satu[1] atau gabungan[2]): ')
        if method_option == '1' or method_option.lower() == 'satu':
            method = 'satu'
            break
        elif method_option == '2' or method_option.lower() == 'gabungan':
            method = 'gabungan'
            break
        else:
            print('Metode layout yang Anda masukkan tidak sesuai')

    print(f'Metode layout: {method}\n')

    os.system(f'{python_qgis} {layout_path} {method}')

else:
    os.system(f'{python_qgis} {layout_path}')