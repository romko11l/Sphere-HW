#! /home/roman/anaconda3/bin/python3

"""A server builds the distribution of person's friends by age in vk.com"""

import socket
import logging
from datetime import datetime
import json
import re
import requests
import dicttoxml


ACCESS_TOKEN = 

INCORRECT_FORMAT_ERROR = "%s: В запросе передан невалидный формат"
TIMEOUT_ERROR = "%s: Истекло время ожидания запроса от %s"
RESPONSE_LOG = "%s: Обработан запрос от %s, размер ответа: %s"


def get_year(bdate):
    """Сalculating the year of birth from the date of birth.

    Keyword arguments:
        bdate -- date of birth string

    Returns:
        year of birth
    """
    point_count = 0
    res = ''
    for symb in bdate:
        if symb == '.':
            point_count += 1
        elif point_count == 2:
            res += symb
    if point_count < 2:
        return None
    return int(res)


def calc_frequency_list(user_id):
    """Building the distribution of the number of people by age.

    Keyword arguments:
        user_id -- validated vk id

    Returns:
        age frequency list
    """
    payload = {'user_ids': user_id, 'v': 5.121, 'access_token': ACCESS_TOKEN}
    response = requests.get('https://api.vk.com/method/users.get',
                            params=payload)
    response_json = response.json()
    if 'error' in response_json:
        return []
    if 'is_closed' not in response_json['response'][0]:
        return []
    user_id = response_json['response'][0]['id']
    payload = {'user_id': user_id, 'fields': 'bdate', 'v': 5.121,
               'access_token': ACCESS_TOKEN}
    response = requests.get('https://api.vk.com/method/friends.get',
                            params=payload)
    response_json = response.json()
    if 'response' not in response_json:
        return []
    friends_list = response_json['response']['items']
    bdate_list = []
    for friend in friends_list:
        if 'bdate' in friend:
            bdate_list.append(friend['bdate'])
    byear_list = []
    for bdate in bdate_list:
        res = get_year(bdate)
        if res is not None:
            byear_list.append(res)
    curr_year = datetime.now().year
    age_list = [curr_year - year for year in byear_list]
    frequency_dict = {}
    for age in age_list:
        frequency_dict[age] = 0
    for age in age_list:
        frequency_dict[age] += 1
    frequency_list = list(frequency_dict.items())
    frequency_list = sorted(frequency_list, key=lambda item: item[0])
    frequency_list = sorted(frequency_list, key=lambda item: item[1],
                            reverse=True)
    return frequency_list


def data_handling(data):
    """Validation of request and processing it.

    Keyword arguments:
        data -- request string from client

    Exceptions:
        KeyError - if received incorrect format

    Returns:
        answer in the required format
    """
    pattern1 = re.compile(r'vk_id=[\w]+&format=(json|xml)')
    pattern2 = re.compile(r'format=(json|xml)&vk_id=[\w]+')
    if pattern1.fullmatch(data) is None and pattern2.fullmatch(data) is None:
        raise KeyError
    if pattern1.fullmatch(data) is not None:
        vk_id, ans_format = tuple(data.split('&'))
    else:
        ans_format, vk_id = tuple(data.split('&'))
    vk_id = vk_id.split('=')[1]
    ans_format = ans_format.split('=')[1]
    if ans_format not in ('json', 'xml'):
        raise KeyError
    ans = calc_frequency_list(vk_id)
    if len(ans) == 0:
        ans_dict = {'error': 'no user data'}
    else:
        ans_dict = {}
        for pair in ans:
            upd = [(str(pair[0]), str(pair[1]))]
            ans_dict.update(upd)
    if ans_format == 'json':
        return json.dumps(ans_dict, indent=4).encode("utf-8")
    return dicttoxml.dicttoxml(ans_dict, custom_root='friends distribution')


def server(port=10001, timeout=5, max_conn=1):
    """Keeps connections running.

    Keyword arguments:
        port -- port associated with server
        timeout -- request timeout
        max_conn -- number of connections supported by the server
    """
    dicttoxml.LOG.setLevel(logging.ERROR)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.listen(max_conn)
    try:
        while True:
            try:
                conn, addr = sock.accept()
                conn.settimeout(timeout)
                now = datetime.now()
                data = conn.recv(1024)
                data = data.decode("utf-8")
                ans = data_handling(data)
                conn.send(ans)
                now1 = datetime.now()
                logging.info(RESPONSE_LOG, now1, now, len(ans))
                conn.close()
            except socket.timeout:
                now1 = datetime.now()
                logging.info(TIMEOUT_ERROR, now1, now)
                conn.send("Timeout interrupt\n".encode("utf-8"))
                conn.close()
            except KeyError:
                now1 = datetime.now()
                logging.info(INCORRECT_FORMAT_ERROR, now1)
                conn.send("Incorrect format\n".encode("utf-8"))
                conn.close()
    except KeyboardInterrupt:
        conn.close()


if __name__ == '__main__':
    pass
