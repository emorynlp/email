import ujson
import os.path

class Extracter():
    def __init__(self):
        self.source = 'data/enron.json'
        self.all = 'data/email.all.json'
        self.threads_only = 'data/email.threads.json'

    def get_all(self):
        if os.path.exists(self.all):
            print('{} exists.'.format(self.all))
        else:
            email_type = 'file'
            self.extract(email_type, self.all)

    def get_threads_only(self):
        if os.path.exists(self.threads_only):
            print('{} exists.'.format(self.threads_only))
        else:
            email_type = 'is_thread'
            self.extract(email_type, self.threads_only)

    def extract(self, email_type, dist):
        result = []
        with open(self.source, 'r') as infile:
            data = ujson.load(infile)
        self.traverse_json(result, data, email_type)
        with open(dist, 'w') as outfile:
            ujson.dump(result, outfile)

    def traverse_json(self, result, data, email_type):
        for key, value in data.items():
            if type(value) is dict:
                self.traverse_json(result, value, email_type)
            elif type(value) is list:
                for i in value:
                    if type(i) is dict:
                        self.traverse_json(result, i, email_type)
            else:
                if email_type == 'is_thread':
                    if key == email_type and data[key]:
                        result.append(data)
                elif email_type == 'file':
                    result.append(data)
