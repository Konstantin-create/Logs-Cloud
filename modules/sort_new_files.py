import json
import os
import threading

import netaddr
import requests


def sort_new(path):
    # region = path[path.rfind('//') + 2:][:2].lower()
    abs_file_path = os.path.abspath(__file__)
    abs_path, filename = os.path.split(abs_file_path)
    abs_path = abs_path[:abs_path.rfind('\\')]
    # with open(f'{abs_path}/data/counter.json', 'r') as file:
    #     counter_data = json.load(file)
    #     file.close()
    # counter_data[region] = 1
    # with open(f'{abs_path}/data/counter.json', 'w') as file:
    #     json.dump(file, counter_data)
    #     file.close()
    get_pwd(path, abs_path)
    get_ftp(path, abs_path)
    get_user_info(path, abs_path)


def get_pwd(path, save_dir):
    try:
        dir_name = path[path.rfind('//') + 2:]
        try:
            with open(f'{path}//Passwords.txt', 'r') as file:
                pwd = file.read()
                file.close()
        except:
            with open(f'{path}//passwords.txt', 'r') as file:
                pwd = file.read()
                file.close()
        with open(f'{save_dir}/data/Passwords.txt', 'r') as file:
            all_pwd = file.read()
            file.close()
        if pwd in all_pwd:
            pass
        else:
            with open(f'{save_dir}/data/Passwords.txt', 'a') as file:
                file.write(dir_name + ' {[\n' + pwd + ' ]}\n')
                file.close()
            getIp(path, save_dir, pwd, dir_name)

    except Exception as e:
        print(e)


def get_ftp(path, save_dir):
    try:
        dir_name = path[path.rfind('//') + 2:]
        with open(f'{path}/FTP/Credentials.txt', 'r') as file:
            ftp = file.read()
            file.close()
        if ftp.count('Server') <= ftp.count('UNKNOWN'):
            pass
        else:
            with open(f'{save_dir}/data/FTPs.txt', 'a') as file:
                file.write(dir_name + ' {[\n' + ftp + ' ]}\n')
                file.close()
    except Exception as e:
        pass


def get_user_info(path, save_dir):
    dir_name = path[path.rfind('//') + 2:]
    user = {'user_hash': dir_name, 'ip': 'None', 'zip_code': 'None', 'location': 'None'}
    with open(f'{path}//UserInformation.txt', 'r') as file:
        user_info_data = file.readlines()
        file.close()
    for line in user_info_data:
        if 'IP: ' in line:
            user['ip'] = line.split(':')[1].strip()
        elif 'Zip Code: ' in line:
            user['zip_code'] = line.split(':')[1].strip()
        elif 'Location: ' in line:
            user['location'] = line.split(':')[1].strip()
    with open(f'{save_dir}/data/users_info.json', 'r') as file:
        json_data = json.load(file)
        file.close()
    with open(f'{save_dir}/data/users_info.json', 'w') as file:
        json_data.append(user)
        json.dump(json_data, file)
        file.close()


class getIp:
    def __init__(self, path, save_dir, data, dir_name):
        self.output = ""
        data = data.split('\n')
        for i in range(len(data)):
            if data[i].count('.') == 3:
                if not '127.0.0.1' in data[i]:
                    if not '192.' in data[i]:
                        ip = data[i][data[i].find('//') + 2:data[i].find('/', data[i].find('/') + 4)]
                        if ip != '' and netaddr.valid_ipv4(ip):
                            self.type_ip = data[i][4:data[i].find('//') + 2]
                            threading.Thread(
                                target=lambda: self.validate2(ip, data[i], data[i + 1], data[i + 2], dir_name,
                                                              save_dir)).start()

    def check(self, host):
        try:
            requests.get(self.type_ip + host)
        except Exception as e:
            return False
        else:
            return True

    def validate2(self, ip, data1, data2, data3, dir_name, save_dir):
        if self.check(ip):
            with open(f'{save_dir}/data/ip.txt', 'a') as file:
                file.write(dir_name + ' {[\n' + str(data1 + '\n' + data2 + '\n' + data3 + '\n') + ' ]}\n')
                file.close()
