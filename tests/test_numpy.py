# This module is used to test numpy compatability
from unittest import TestCase

import numpy

from sliceable_generator import SliceableGenerator


class TestNumpyCompatability(TestCase):
    def setUp(self) -> None:
        self.data = numpy.ones((3, 4)).cumsum().reshape((3, 4))
        self.g = SliceableGenerator(self.data, depth=2)

    def test_basic(self):
        for i, row in enumerate(self.g):
            for j, cell in enumerate(row):
                self.assertEqual(self.data[i, j], cell)

    def test_slice(self):
        self.assertEqual(self.g[2, 3], self.data[2, 3])
        self.assertListEqual(self.g[2, 3:].to_list(), list(self.data[2, 3:]))
        self.assertListEqual(self.g[1:, 3].to_list(), list(self.data[1:, 3]))
        self.assertListEqual(self.g[1:3, 2:4].to_list(), self.data[1:3, 2:4].tolist())
