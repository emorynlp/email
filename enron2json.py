# -*- coding: utf-8 -*-

from __future__ import print_function

import errno
import os
import requests
import ujson
import io
from tqdm import tqdm
from parser.enron_parser import EnronParser
import tarfile


def parse(path):
    data = {
        'type': 'folder',
        'name': os.path.basename(path),
        'path': path,
    }
    try:
        data['children'] = [
            parse(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        data['type'] = 'file'
        with io.open(path, errors='ignore') as f:
            file = f.read()
        threads, is_thread = email_parser.parse(file)
        data['emails'] = threads
        data['is_thread'] = is_thread
    return data


def download_file(url, file_path):
    chunk_size = 1024
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            pbar = tqdm(unit="B", total=int(r.headers['Content-Length']))
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    pbar.update(len(chunk))
                    f.write(chunk)


def extract(tar_path, extract_path="."):
    try:
        if os.path.isdir(data_dir):
            pass
        else:
            os.mkdir(data_dir)
        tar = tarfile.open(tar_path, 'r')
        for item in tqdm(tar):
            tar.extract(item, extract_path)
        tar.close()
    except Exception as e:
        raise Exception(e)


def fetch_enron_data():
    enron_data_source = "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tgz"
    file_path = enron_data_source.split('/')[-1]
    if not os.path.exists(file_path):
        print("Download enron dataset...")
        download_file(enron_data_source, file_path)
    print("Extracting {}...".format(file_path))
    extract(file_path)
    print("Removing {}...".format(file_path))
    os.remove(file_path)


if __name__ == '__main__':

    data_dir = "maildir"
    dist_dir = "data"
    result_filename = "email.threads.json"

    if not (os.path.isdir(data_dir)):
        fetch_enron_data()
    if not (os.path.isdir(dist_dir)):
        os.mkdir(dist_dir)

    email_parser = EnronParser()
    data = parse(data_dir)

    output_path = "{}/{}".format(dist_dir, result_filename)
    with open(output_path, 'w') as f:
        ujson.dump(data, f)
