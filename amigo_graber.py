import requests
import urllib.request
import json
import os
import time
import json
import base64
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import re


def load_page(target_url: str = None, headers: str = None):
    with requests.get(target_url, headers=headers) as response:
        return BeautifulSoup(response.text, "html.parser")


def download_images(path_to_save: str = '', name_to_save: str = '', target_urls: list = None):
    mkdir(path_to_save)
    for url in target_urls:
        with open(f'{path_to_save}/{name_to_save}', 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            print(name_to_save, " - downloaded successfully")


def save_to_csv(path_to_save: str = '', name_to_save: str = '', data: list = None, columns: list = None):
    mkdir(path_to_save)
    frame = pd.DataFrame(data, columns=columns)
    frame.to_csv(f'{path_to_save}/{name_to_save}', index=False)


def mkdir(path: str = ''):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


class NoneInPattern(Exception):
    pass


def parse_name(source):
    re_template = [
        re.compile(r'^(\D+[\s]?[\d]?)[\s]?[\d]{4}[\s]?'),
        re.compile('(^[\w]*[\s][\d]*[\s][\w]{2}[\s][\w][\s][\w,.]*)[,]?[\s][\w\s,]*$'),
    ]
    for pattern in re_template:
        result = pattern.findall(source)
        if result.__len__() == 1:
            return result[0]
    raise NoneInPattern('Error re pattern')


def parse_code(source):
    default_code = '255'
    re_template = [
        re.compile(r'^\D+[\s]?[\d]?[\s]?([\d]{4})[\s]?[^,]+[,\s]+\d+'),
    ]
    for pattern in re_template:
        result = pattern.findall(source)
        if result.__len__() == 1:
            return result[0]
    return default_code


def parse_color(source):
    #re.findall(r'^\D+[\s]?[\d]{4}[\s]?([^,]+)[,\s]+\d+', item.find('img')['title']
    default_color = 'Без цвета'
    re_template = [
        re.compile(r'^\D+[\s]?[\d]?[\s]?[\d]{4}[\s]?([^,]+)[,\s]+\d+'),
        re.compile('^[\w]*[\s][\d]*[\s][\w]{2}[\s][\w][\s][\w,.]*[,]?[\s]([\w\s,]*$)'),
    ]
    for pattern in re_template:
        result = pattern.findall(source)
        if result.__len__() == 1:
            return result[0]
    return default_color


def parse_height(source):
    re_template = [
        re.compile('^[\w]*[\s]([\d]*[\s][\w]{2})[\s][\w][\s][\w,.]*[,]?[\s][\w\s,]*$'),
        re.compile(r'([\d+]?[,]?\d+\D+$)'),
    ]
    for pattern in re_template:
        result = pattern.findall(source)
        if result.__len__() == 1:
            if 'мм' in result[0]:
                return str(int(str(result[0]).replace('мм', '').replace(' ', ''))/1000)
            if 'см' in result[0] or 'cм' in result[0]:
                return str(int(str(result[0]).replace('см', '').replace('cм', '').replace(' ', ''))/100)
            if 'м' in result[0]:
                return str(result[0]).replace('м', '').replace(' ', '').replace(',','.')

            return result[0]


if __name__ == '__main__':
    start_time = time.time()
    root_url = 'https://amigo.ru'
    targets = [
        #'https://amigo.ru/kollekcii/kollektsiya-vertikalnykh-tkaney/',
        #'https://amigo.ru/kollekcii/kollektsiya-vertikalnykh-tkaney/?PAGEN_1=2',
        #'https://amigo.ru/kollekcii/kollektsiya-tkaney-plisse/?PAGEN_1=3',
        'https://amigo.ru/kollekcii/kollektsiya-rulonnykh-tkaney/',
        #'https://amigo.ru/kollekcii/kollektsiya-vertikalnyy-plastik-alyuminiy/',
        ]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/2010010 Firefox/45.0'}
    path_to_save_images = 'results_vertical_alum/images'
    path_to_save_results = 'results_vertical_alum'
    total_error = 0
    total_items = 0
    rows_parse_data_text = []
    data_columns = ['name', 'code', 'color', 'height', 'img_name']

    for target in targets:
        page = load_page(target, headers)
        items = page(class_='ribbon-list-item')
        total_items += items.__len__()
        for item in items:
            parse_data_text = item.find('img')['title'].split(' ')
            try:
                raw_source = item.find('img')['title']
                name = parse_name(raw_source)
                code = parse_code(raw_source)
                color = parse_color(raw_source)
                height = parse_height(raw_source)
                print(name, code, color, height)
                rows_parse_data_text.append([
                    name,
                    code,
                    color,
                    height,
                    item.find('img')['src'].split('/')[-1],
                ])
                """
                download_images(
                    path_to_save=path_to_save_images,
                    name_to_save=item.find('img')['src'].split('/')[-1],
                    target_urls=[
                        root_url+item.find('img')['src'],
                    ]
                )
                """

                
            except IndexError:
                total_error += 1
                print('Error: ', item.find('img')['title'])
            except NoneInPattern as e:
                total_error += 1
                print(e)


    save_to_csv(path_to_save_results, 'results.csv', data=rows_parse_data_text, columns=data_columns)

    print(f'Processed {total_items} links. Total time {(time.time() - start_time)}. Total error: {total_error}')
