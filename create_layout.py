import os

python_qgis = 'C:/OSGeo4W64/bin/python-qgis.bat'

while True:
    project_type = input("Pilih tipe project (ship/oils/dto): ")
    if project_type.lower() == 'ship':
        layout_path = "layouts/layout_ship.py"
        break
    elif project_type.lower() == 'oils':
        layout_path = "layouts/layout_oils.py"
        break
    elif project_type.lower() == 'dto':
        layout_path = "layouts/layout_dto.py"
        break
    else:
        print('Tipe project yang Anda masukkan tidak sesuai')

print(f'Tipe project: {project_type.lower()}\n')

if project_type.lower() != 'dto':
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

    os.system(f'{python_qgis} {layout_path} {method}\n')

else:
    while True:
        method_option = input('Pilih metode layout (satu[1] atau banyak[2]): ')
        if method_option == '1' or method_option.lower() == 'satu':
            method = 'satu'
            break
        elif method_option == '2' or method_option.lower() == 'banyak':
            method = 'banyak'
            break
        else:
            print('Metode layout yang Anda masukkan tidak sesuai')

    print(f'Metode layout: {method}\n')
    
    os.system(f'{python_qgis} {layout_path} {method}')