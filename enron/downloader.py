import os
import tarfile

import requests
from tqdm import tqdm


class Downloader():

    def __init__(self):
        self.source_url = "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tgz"

    def download(self):
        file_path = self.source_url.split('/')[-1]
        if not os.path.exists(file_path):
            print("Download enron dataset...")
            self.download_file(self.source_url, file_path)
        print("Extracting {}...".format(file_path))
        self.extract(file_path)
        print("Removing {}...".format(file_path))
        os.remove(file_path)

    @staticmethod
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

    @staticmethod
    def extract(tar_path, extract_path="."):
        try:
            tar = tarfile.open(tar_path, 'r')
            for item in tqdm(tar):
                tar.extract(item, extract_path)
            tar.close()
        except Exception as e:
            raise Exception(e)