# -*- coding: utf-8 -*-
import os
import re
import sys
import json

import requests
from PIL import Image


try:
    import api
    from config import APP_ID, APP_KEY, FACE_PATH
    from compress import resize_image
except Exception as ex:
    print(ex)
    exit(1)


BEAUTY_THRESHOLD = 60
DEFAULT_SRC_FILE = 'download.png'
OPTIMIZED_FILE = 'optimized.png'


def is_url(url):
    return url.startswith(("http", "https"))


def download_file(url, download_path):
    try:
        r = requests.get(url, stream=True, timeout=5)
        if r.status_code == 200:
            with open(download_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(e)
        return False


def main():
    """
    main
    :return:
    """
    while True:
        print('> input image file or url')
        addr = input('> ')
        addr = addr.strip()
        if addr == "":
            continue

        if is_url(addr):
            if download_file(addr, FACE_PATH + DEFAULT_SRC_FILE) == False:
                continue
            else:
                addr = FACE_PATH + DEFAULT_SRC_FILE
        else:
            if os.path.exists(addr) == False:
                continue

        resize_image(addr, OPTIMIZED_FILE, 1024 * 1024)

        with open(OPTIMIZED_FILE, 'rb') as bin_data:
            image_data = bin_data.read()

        ai_obj = api.AiPlat(APP_ID, APP_KEY)
        rsp = ai_obj.face_detectface(image_data, 0)

        if rsp['ret'] == 0:
            print(">  ", rsp['data']['text'])
            ok, mark = is_siwa(rsp['data']['text'])
            if ok:
                print("> contains: ", mark)
            continue

        else:
            print("识别异常")
            print(rsp)
            continue


def is_siwa(content):
    res = regex.search(content)
    if res:
        return True, res.group()
    return False, ""

regex = re.compile("丝袜|美女|长腿|短裙|脚|内裤|黑丝|黑色")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
