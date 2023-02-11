from bs4 import BeautifulSoup
import requests
import json
import codecs
import time
import urllib.robotparser
import secrets
import re
import logging


def download(url, redownload=False):
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(re.match(r'(?P<root>https?://.*?)\/.*', url).group('root') + "/robots.txt")
        rp.read()

        if rp.can_fetch('*', url):

            res = requests.get(url)

            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError:
                logging.warning('HTTPError:Cannot crawl page')

            soup = BeautifulSoup(res.content, 'html.parser')
            file_name = secrets.randbits(16)
            with open(f'webpages/{file_name}.html', 'wb') as f:
                f.write(res.content)

            with codecs.open('download_list_file.json', 'w', 'utf-8') as f:
                f.write(json.dumps({'title': soup.title.string, 'url': url, 'filepath': f'webpages/{file_name}.html'},
                                   ensure_ascii=False))

            if redownload:
                logging.info('redownload')
                time.sleep(1)
                for link in soup.find_all('a'):
                    if is_valid_url(link.get('href')):
                        download(str(link.get('href')))
                        time.sleep(1)

            logging.info('success')
        else:
            logging.warning('PermissionError:You dont have permission this page.')
    except:
        pass


def is_valid_url(url):
    pattern = re.compile(r'^https?://')
    match = pattern.match(url)
    return bool(match)
