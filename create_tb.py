import os

baratatb_path = "barata/barata_tb.py"

while True:
    option = input('Pilih jenis project (ship/oils): ')
    if option.lower() == 'ship':
        project_type = 'ship'
        break
    elif option.lower() == 'oils':
        project_type = 'oils'
        break
    else:
        print('Tipe project yang Anda masukkan tidak sesuai')

print(f'Tipe project: {project_type.lower()}\n')

while True:
    option = input('Pilih jenis tb (satu[1] atau gabungan[2]): ')
    if option == '1' or option.lower() == 'satu':
        method = 'satu'
        break
    elif option == '2' or option.lower() == 'gabungan':
        method = 'gabungan'
        break
    else:
        print('Metode layout yang Anda masukkan tidak sesuai')

print(f'Metode layout: {method}\n')

os.system(f'python-qgis {baratatb_path} {project_type} {method}')
