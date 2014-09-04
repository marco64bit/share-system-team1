#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import time
import os

TMP_FILE_PATH = 'tmp_upload_files.json'


def remove(tmp_file_path):
    try:
        os.remove(tmp_file_path)
    except OSError, e:
        print e


def main():
    timeout = 60 * 60 * 12.0  # 12 hours
    tmp_file = json.load(open(TMP_FILE_PATH, 'r'))
    for user in tmp_file.keys():
        for path in tmp_file[user].keys():
            if time.time() - float(tmp_file[user][path]['timestamp']) > timeout:
                tmp_file_path = tmp_file[user][path]['file_name']
                # remove reference from tmp json and save it
                del tmp_file[user][path]
                if len(tmp_file[user]) == 0:
                    del tmp_file[user]
                json.dump(tmp_file, open(TMP_FILE_PATH, 'w'))
                # remove tmp file if exists
                remove(tmp_file_path)

if __name__ == '__main__':
    main()
