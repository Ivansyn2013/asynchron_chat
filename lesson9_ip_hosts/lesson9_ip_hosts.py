import socket
import subprocess
from time import sleep
from pprint import pprint
from ipaddress import ip_address, ip_network
from socket import gethostbyname
from tabulate import tabulate

def host_ping(ip_list, count_number=3):
    result = {'Доступен':[],
              'Недоступен':[]}
    for ip in ip_list:
        try:
            adress = ip_address(ip)
        except ValueError:
            try:
                ip = gethostbyname(ip)
                adress = ip_address(ip)
            except socket.gaierror as err:
                print(f'Недопустимое имя хоста {ip}')
                result['Недоступен'].append(str(ip))

        ping_pocess = subprocess.Popen(f"ping {adress} -c {count_number}",
                                       shell=True,
                                       stdout=subprocess.PIPE)
        ping_pocess.wait()
        print(ping_pocess.returncode)
        if ping_pocess.returncode == 0:
            result['Доступен'].append(ip)
        else:
            result['Недоступен'].append(str(ip))
    pprint(result)
    return result

def host_range_ping():
    start_ip = ip_address(input('Введите ip\n'))
    nums = int(input('Введите количество переборов\n'))
    ip_list = []

    for index in range(nums):
        new_ip = start_ip + index
        if str(new_ip).split('.')[2] != str(start_ip).split('.')[2]:
            print('В этой подсети адреса закончились')
            break
        print('Проверяю ' + str(new_ip))

        ip_list.append(new_ip)
    return host_ping(ip_list)



def host_range_ping_tab():
    adres_dict = host_range_ping()
    print()
    print(tabulate(*[adres_dict], headers=adres_dict.keys(), tablefmt='pipe', ))


if __name__ == "__main__":
    #host_ping(['77.88.55.242', 'ya.ru', 'fdsdweqf'])
    host_range_ping_tab()
