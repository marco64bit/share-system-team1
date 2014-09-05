#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import shutil
import json
import os

import cron_remove_tmp as cron


class TestEnvironment(object):
    def __init__(self):
        self.test_main_path = os.path.join(os.path.expanduser('~'), 'test_cron_folder')
        os.makedirs(self.test_main_path)
        self.tmp_file_path = os.path.join(self.test_main_path, 'tmp_upload_files.json')
        self.tmp_path = os.path.join(self.test_main_path, 'tmp_folder')
        os.makedirs(self.tmp_path)
        self.tmp1 = os.path.join(self.tmp_path, 'tmp_path1')
        self.tmp2 = os.path.join(self.tmp_path, 'tmp_path2')
        self.tmp3 = os.path.join(self.tmp_path, 'tmp_path3')
        self.tmp4 = os.path.join(self.tmp_path, 'tmp_path4')
        self.tmp5 = os.path.join(self.tmp_path, 'tmp_path5')
        json.dump({
            "user1": {
                "path1": {
                    "timestamp": 1000000000000.0,
                    "path": self.tmp1
                }
            },
            "user2": {
                "path2": {
                    "timestamp": 1.0,
                    "file_name": self.tmp2
                },
                "path3": {
                    "timestamp": 2.0,
                    "file_name": self.tmp3
                }
            },
            "user3": {
                "path2": {
                    "timestamp": 1000000000000.0,
                    "file_name": self.tmp4
                },
                "path3": {
                    "timestamp": 1.0,
                    "file_name": self.tmp5
                }
            }
        }, open(self.tmp_file_path, 'w'))
        # create some tmp
        open(os.path.join(self.tmp_path, self.tmp1), 'w').write('i like tests')
        open(os.path.join(self.tmp_path, self.tmp2), 'w').write('i like tests')
        open(os.path.join(self.tmp_path, self.tmp3), 'w').write('i like tests')
        open(os.path.join(self.tmp_path, self.tmp4), 'w').write('i like tests')
        open(os.path.join(self.tmp_path, self.tmp5), 'w').write('i like tests')

    def remove(self):
        shutil.rmtree(self.test_main_path)


class CronTest(unittest.TestCase):
    def setUp(self):
        #Generate tmp file and json to test
        self.environment = TestEnvironment()

    def tearDown(self):
        self.environment.remove()

    def test_cron(self):
        cron.TMP_FILE_PATH = self.environment.tmp_file_path
        cron.main()
        tmp_file = json.load(open(self.environment.tmp_file_path, 'r'))
        # check if cron remove all old file from json
        self.assertEqual(tmp_file, {
            'user3': {
                'path2': {
                    'timestamp': 1000000000000.0,
                    'file_name': self.environment.tmp4
                }
            },
            'user1': {
                'path1': {
                    'timestamp': 1000000000000.0,
                    'path': self.environment.tmp1
                }
            }
        })
        # check if corn remove all tmp file from hard disk
        self.assertFalse(os.path.exists(self.environment.tmp2))
        self.assertFalse(os.path.exists(self.environment.tmp3))
        self.assertFalse(os.path.exists(self.environment.tmp5))

        self.assertTrue(os.path.exists(self.environment.tmp1))
        self.assertTrue(os.path.exists(self.environment.tmp4))


if __name__ == '__main__':
    unittest.main()
