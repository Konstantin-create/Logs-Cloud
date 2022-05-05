from json import load
from urllib.request import urlopen


def get_address_by_ip(addr):
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    data = load(res)
    return data
