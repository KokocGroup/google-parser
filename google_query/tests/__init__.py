# -*- coding: utf-8 -*-
import unittest
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(TESTS_DIR , 'data')


class GoogleQueryTests(unittest.TestCase):

    def setUp(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().discover(TESTS_DIR)
    unittest.TextTestRunner(verbosity=2).run(suite)