# -*- coding: utf-8 -*-

from __future__ import print_function

import errno
import os
import ujson
import io
from enron.parser import Parser
from enron.downloader import Downloader


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


if __name__ == '__main__':

    data_dir = "maildir"
    dist_dir = "data"
    result_filename = "email.threads.json"

    if not (os.path.isdir(data_dir)):
        Downloader().download()
    if not (os.path.isdir(dist_dir)):
        os.mkdir(dist_dir)

    # email_parser = Parser()
    # data = parse(data_dir)
    #
    # output_path = "{}/{}".format(dist_dir, result_filename)
    # with open(output_path, 'w') as f:
    #     ujson.dump(data, f)
