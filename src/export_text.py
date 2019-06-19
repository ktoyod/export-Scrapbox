import json
import os
import requests
import time
from urllib.parse import urljoin

import config
import path


def get_titles_list(skip=0, limit=100):
    params = {'skip': skip, 'limit': limit}
    pages = requests.get(config.Config.PROJECT_URL,
                         params=params,
                         cookies={'connect.sid': config.Config.CONNECT_SID})
    pages_list = json.loads(pages.text)['pages']
    titles_list = [page['title'] for page in pages_list]

    return titles_list


def get_text(title):
    text_url = urljoin(config.Config.PROJECT_URL + '/', f'{title}/text')
    text = requests.get(text_url, cookies={'connect.sid': config.Config.CONNECT_SID})
    return text.text


def save_texts(titles_list):
    cnt = 1
    total_pages = len(titles_list)

    for title in titles_list:
        print(f'{cnt}/{total_pages}: {title}', end='')
        if ':' in title:
            print(' -> skip')
            continue

        text = get_text(title)
        time.sleep(1)

        title = title.replace('/', '-')
        text_path = os.path.join(path.Path.OUTPUT_TEXT_PATH, f'{title}.txt')
        with open(text_path, 'w') as f:
            f.write(text)
            print(f' -> {text_path}')
            cnt += 1


def main():
    titles_list = get_titles_list(limit=500)
    time.sleep(1)
    save_texts(titles_list)


if __name__ == '__main__':
    main()
