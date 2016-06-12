# -*- coding: utf-8 -*-
import unittest

import simple


class TestSimple(unittest.TestCase):

    def test_foobar(self):
        self.assertEqual(simple.foobar(), 42)
