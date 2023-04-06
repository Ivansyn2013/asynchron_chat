import json
import re
import os
from chardet import detect

def get_data():
    file_list = os.listdir()
    for file in file_list:
        if os.path.splitext(file)[1] == '.txt':
            print(file)
            with open(file,'rb') as file:
                ENCODING = detect(file.readline())['encoding']
                data = file.read()
                data = data.decode(ENCODING)

                print(data)

if __name__ == '__main__':
    print(get_data())