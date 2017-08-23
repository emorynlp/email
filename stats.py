import ujson

with open('data/email.all.json') as f:
    all = ujson.load(f)

if __name__ == '__main__':

    thread_count = 0
    non_thread_count = 0
    thread_email_count = 0
    non_thread_email_count = 0
    distribution = {}

    for item in all:
        if item['is_thread']:
            email_count = len(item['emails'])
            thread_count += 1
            thread_email_count += email_count
            if email_count in distribution.keys():
                distribution[email_count] += 1
            else:
                distribution[email_count] = 1
        else:
            non_thread_count += 1
            non_thread_email_count += len(item['emails'])
            distribution[1] = non_thread_count

    print("Number of thread: {}".format(thread_count))
    print("Number of emails with thread: {}".format(thread_email_count))
    print("Number of non-thread emails: {}".format(non_thread_email_count))
    print("Total files: {}".format(thread_count + non_thread_count))
    print("Total emails: {}".format(thread_email_count + non_thread_email_count))
    print("Distribution: {}".format(distribution))

    with open('dis.json', 'w') as out:
        ujson.dump(distribution, out, indent=2, sort_keys=True)
