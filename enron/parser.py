import email
import re
from email.parser import HeaderParser
from validate_email import validate_email
import time

header_parser = HeaderParser()


class Parser():
    def __init__(self):
        self.re_forward = re.compile(r'(.*-.*Forwarded.*)')
        self.re_forward_ = re.compile(r'(.*---------------------------)')
        self.re_original = re.compile(r'(.*-.*Original Message.*-.*)')
        self.re_from = re.compile(r'(From:.*)')
        self.re_to = re.compile(r'To:.*')
        self.re_cc = re.compile(r'([Cc][Cc]:.*)')
        self.re_bcc = re.compile(r'(Bcc:.*)')
        self.re_subject = re.compile(r'(Subject:.*)')

    def parse(self, file):
        return self.establish_structure(file)

    def merge(self, receivers):
        is_merge = False
        if len(receivers) == 2 and all(validate_email(receiver) for receiver in receivers) == False:
            if ' ' not in receivers[0].strip():
                is_merge = True;
        if is_merge:
            return ([receivers[0] + ',' + receivers[1]])
        else:
            return (receivers)

    def split_receivers(self, receiver_type, d):
        if ';' in d[receiver_type]:
            d[receiver_type] = d[receiver_type].replace("\r", "") \
                .replace("\n", "") \
                .replace("\t", "").strip().split(';')
        else:
            d[receiver_type] = d[receiver_type].replace("\r", "") \
                .replace("\n", "") \
                .replace("\t", "").strip().split(',')
        return d

    def get_headers(self, text):
        headers = header_parser.parsestr(text)
        d = {header: name for header, name in headers.items()}
        for receiver_type in ['To', 'Cc', 'Bcc']:
            try:
                d = self.split_receivers(receiver_type, d)
                d[receiver_type] = self.merge(d[receiver_type])
            except KeyError:
                pass
        return d

    def get_body(self, text):
        content = email.message_from_string(text)
        if content.is_multipart():
            for part in content.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    content = part.get_payload(decode=True)  # decode
                    content = content.decode('utf-8')
                    break
        else:
            content = content.get_payload(decode=True)
            content = content.decode('utf-8')
        return content

    def establish_structure(self, file):
        mail = {}
        mail.update(self.get_headers(file))
        content = self.get_body(file)
        body, threads, is_threads = self.split_threads(content)
        mail['body'] = body
        result = []
        result.append(mail)

        if is_threads:
            for thread in threads:
                result.append(thread)
        return result, is_threads

    def split_threads(self, content):
        threads = []
        thread = []
        is_threads = bool(self.re_forward.search(content) or self.re_original.search(content))
        if (is_threads):
            for idx, line in enumerate(content.splitlines()):
                line = line.strip()
                if len(line) == 0:
                    continue
                if self.re_forward_.search(content.splitlines()[idx]):
                    continue
                if self.re_forward.search(line) or self.re_original.search(line):
                    threads.append("\n".join(thread))
                    thread = []
                else:
                    thread.append(line)
            threads.append("\n".join(thread))
            if len(threads) > 1:
                result = self.process_threads(threads)
                body = result[0]['body']
                return body, result[1:], is_threads
            else:
                is_threads = False
                return content, threads, is_threads
        else:
            return content, threads, is_threads

    def process_receivers(self, reg, mail, receiver_type, line, idx, skip_idx, thread):
        timeout = time.time() + 10

        if ';' in line:
            mail[receiver_type] = line[reg.start() + len(receiver_type + ': '):].rstrip(',').split(';')
        else:
            mail[receiver_type] = line[reg.start() + len(receiver_type + ': '):].rstrip(',').split(',')

        mail[receiver_type] = self.merge(mail[receiver_type])
        i = 1

        while True:
            try:
                if ';' in thread.splitlines()[idx + i]:
                    emails = thread.splitlines()[idx + i].split(';')
                else:
                    emails = thread.splitlines()[idx + i].split(',')
                emails = self.merge(emails)
            except IndexError:
                break

            if all(validate_email(e) for e in emails):
                mail[receiver_type].extend(emails)
                skip_idx.append(idx + i)
            i += 1
            try:
                if ';' in thread.splitlines()[idx + i]:
                    emails = thread.splitlines()[idx + i].split(';')
                else:
                    emails = thread.splitlines()[idx + i].split(',')

                emails = self.merge(emails)
            except IndexError:
                break
            if all(validate_email(e) for e in emails) != True or time.time() > timeout:
                break

    def process_headrs(self, thread, mail):
        content = []
        skip_idx = []
        for idx, line in enumerate(thread.splitlines()):
            if idx in skip_idx:
                continue
            to = re.search(self.re_to, line)
            if to:
                self.process_receivers(to, mail, 'To', line, idx, skip_idx, thread)
            cc = re.search(self.re_cc, line)
            if cc:
                self.process_receivers(cc, mail, 'Cc', line, idx,
                                       skip_idx, thread)
            bcc = re.search(self.re_bcc, line)
            if bcc:
                self.process_receivers(bcc, mail, 'Bcc', line, idx,
                                       skip_idx, thread)
            hfrom = re.search(self.re_from, line)
            if hfrom:
                mail['From'] = line[hfrom.start() + len('From: ')]
            subject = re.search(self.re_subject, line)
            if subject:
                mail['Subject'] = line[subject.start() + len('Subject: '):]
            else:
                content.append(line)
        return mail, content

    def process_threads(self, threads):
        result = []
        for thread in threads:
            mail = {}
            headers = self.get_headers(thread)
            if not headers.keys():
                try:
                    mail, content = self.process_headrs(thread, mail)
                except Exception as e:
                    continue
                mail['body'] = '\n'.join(content)
                result.append(mail)
            else:
                mail.update(headers)
                content = self.get_body(thread)
                mail['body'] = content
                result.append(mail)
        return result
