import json
import re
import os
import csv
from chardet import detect

def get_data():
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    file_list = os.listdir()
    for file in file_list:
        if os.path.splitext(file)[1] == '.txt':

            with open(file,'rb') as file:
                ENCODING = detect(file.readline())['encoding']
                data = file.read()
                data = data.decode(ENCODING)

                os_prod_reg = re.compile(r'Изготовитель системы:\s*\S*')
                os_prod_list.append(os_prod_reg.findall(data)[0].split()[2])

                os_name_reg = re.compile(r'Windows\s\S*')
                os_name_list.append(os_name_reg.findall(data)[0])

                os_code_reg = re.compile(r'Код продукта:\s*\S*')
                os_code_list.append(os_code_reg.findall(data)[0].split()[2])

                os_type_reg = re.compile(r'Тип системы:\s*\S*')
                os_type_list.append(os_type_reg.findall(data)[0].split()[2])

            table_head = ['#',
                          'Изготовитель системы',
                          'Windows',
                          'Код продукта',
                          'Тип системы',
                          ]
    main_data.append(table_head)
    for index in range(0,3):
        row = []
        row.append(index+1)
        row.append(os_prod_list[index])
        row.append(os_name_list[index])
        row.append(os_code_list[index])
        row.append(os_type_list[index])
        main_data.append(row)

    return main_data

def write_to_csv(out_file):

    main_data = get_data()
    with open(out_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in main_data:
            writer.writerows(main_data)




if __name__ == '__main__':
    print(get_data())
    write_to_csv('outfie.csv')