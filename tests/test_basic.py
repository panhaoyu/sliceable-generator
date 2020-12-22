from unittest import TestCase

from sliceable_generator import SliceableGenerator


class TestSliceableGenerator(TestCase):
    def setUp(self) -> None:
        self.g1d = SliceableGenerator(range(10, 20))
        # Below are some wrong writings!
        # self.g2d = SliceableGenerator((((i, j) for j in range(20, 30)) for i in range(10, 20)), depth=2)
        # self.g3d = SliceableGenerator(
        #     ((((i, j, k) for k in range(30, 40)) for j in range(20, 30)) for i in range(10, 20)), depth=3)
        # Builtin iterators do not support nested call, or it may behave unexpected.
        # The correct usages are shown below:
        self.g2d = SliceableGenerator((
            (lambda i: ((i, j) for j in range(20, 30)))(i)
            for i in range(10, 20)), depth=2)
        self.g3d = SliceableGenerator((
            (lambda i: (
                (lambda j: ((i, j, k) for k in range(30, 40)))(j)
                for j in range(20, 30)))(i)
            for i in range(10, 20)), depth=3)

    # Firstly, test if the class can be used as builtin generators.

    def test_is_1d_iterable(self):
        self.assertListEqual(list(self.g1d), list(range(10, 20)))

    def test_is_2d_iterable(self):
        for x, i in zip(self.g2d, range(10, 20)):
            for y, j in zip(x, range(20, 30)):
                self.assertEqual(y, (i, j))

    def test_is_3d_iterable(self):
        for i, x in zip(range(10, 20), self.g3d):
            for j, y in zip(range(20, 30), x):
                for k, z in zip(range(30, 40), y):
                    self.assertTupleEqual((i, j, k), z)

    # Test if the function len runs correctly.

    def test_1d_length(self):
        self.assertEqual(len(self.g1d), 10)

    def test_2d_length(self):
        self.assertEqual(len(self.g2d), 10)
        for i in self.g2d:
            self.assertEqual(len(i), 10)

    def test_3d_length(self):
        self.assertEqual(len(self.g3d), 10)
        for i in self.g3d:
            self.assertEqual(len(i), 10)
            for j in i:
                self.assertEqual(len(j), 10)

    # Test if it is reusable.

    def test_is_reusable(self):
        self.assertListEqual(list(self.g1d), list(range(10, 20)))
        self.assertListEqual(list(self.g1d), list(range(10, 20)))

    # Test integer subscripts, for this is the easiest subscript.

    def test_1d_subscript(self):
        self.assertEqual(self.g1d[3], 13)
        self.assertEqual(self.g1d[5], 15)

    def test_2d_subscript(self):
        self.assertListEqual(self.g2d[3].to_list(), [(13, i) for i in range(20, 30)])
        self.assertTupleEqual(self.g2d[3][6], (13, 26))
        self.assertTupleEqual(self.g2d[4, 5], (14, 25))

    def test_3d_subscript(self):
        self.assertListEqual(list(self.g3d[3, 5]), [(13, 25, i) for i in range(30, 40)])
        self.assertTupleEqual(self.g3d[3, 4, 5], (13, 24, 35))

    def test_negative_subscript(self):
        self.assertEqual(self.g1d[-3], 17)
        self.assertEqual(self.g2d[-3, -4], (17, 26))
        self.assertEqual(self.g3d[-4, -5, -6], (16, 25, 34))

    def test_non_exists_subscript(self):
        with self.assertRaisesRegex(IndexError, '13'):
            _ = self.g1d[13]
        with self.assertRaisesRegex(IndexError, '-15'):
            _ = self.g1d[-15]

    # Test to list.
    # In slice testcases, we need to use to list frequently.

    def test_1d_to_list(self):
        self.assertListEqual(self.g1d.to_list(), [i for i in range(10, 20)])

    def test_2d_to_list(self):
        self.assertListEqual(self.g2d.to_list(), [
            [(i, j) for j in range(20, 30)] for i in range(10, 20)])

    def test_3d_to_list(self):
        self.assertListEqual(self.g3d.to_list(), [
            [[(i, j, k) for k in range(30, 40)] for j in range(20, 30)] for i in range(10, 20)])

    # Test slice.

    def test_1d_slice(self):
        self.assertListEqual(self.g1d[3:5].to_list(), [13, 14])
        self.assertListEqual(self.g1d[3:-5].to_list(), [13, 14])
        self.assertListEqual(self.g1d[-7:5].to_list(), [13, 14])
        self.assertListEqual(self.g1d[-7:-5].to_list(), [13, 14])

    def test_2d_slice(self):
        self.assertListEqual(self.g2d[3:5].to_list(), [[(i, j) for j in range(20, 30)] for i in (13, 14)])
        self.assertListEqual(self.g2d[3:5, 5:7].to_list(), [[(13, 25), (13, 26)], [(14, 25), (14, 26)]])
        self.assertListEqual(self.g2d[:, 5:7].to_list(), [[(i, 25), (i, 26)] for i in range(10, 20)])

    def test_3d_slice(self):
        self.assertListEqual(self.g3d[3:5].to_list(), [
            [[(i, j, k) for k in range(30, 40)] for j in range(20, 30)] for i in (13, 14)])
        self.assertListEqual(self.g3d[3:5, 4:6].to_list(), [
            [[(i, j, k) for k in range(30, 40)] for j in range(24, 26)] for i in (13, 14)])
        self.assertListEqual(self.g3d[3:5, 4:6, 5:8].to_list(), [
            [[(i, j, k) for k in (35, 36, 37)] for j in (24, 25)] for i in (13, 14)])

    # Test slice and subscript make effect simultaneously

    def test_2d_combined_subscript_slice(self):
        self.assertListEqual(self.g2d[3:5, 4].to_list(), [(13, 24), (14, 24)])
        self.assertListEqual(self.g2d[3, 4:6].to_list(), [(13, 24), (13, 25)])

    def test_3d_combined_subscript_slice(self):
        self.assertListEqual(self.g3d[3, 4, 5:7].to_list(), [(13, 24, 35), (13, 24, 36)])
        self.assertListEqual(self.g3d[3, 4:6, 5].to_list(), [(13, 24, 35), (13, 25, 35)])
        self.assertListEqual(self.g3d[3:5, 4, 5].to_list(), [(13, 24, 35), (14, 24, 35)])
        self.assertListEqual(self.g3d[3, 4:6, 5:7].to_list(),
                             [[(13, 24, 35), (13, 24, 36)], [(13, 25, 35), (13, 25, 36)]])
        self.assertListEqual(self.g3d[3:5, 4, 5:7].to_list(),
                             [[(13, 24, 35), (13, 24, 36)], [(14, 24, 35), (14, 24, 36)]])
        self.assertListEqual(self.g3d[3:5, 4:6, 5].to_list(),
                             [[(13, 24, 35), (13, 25, 35)], [(14, 24, 35), (14, 25, 35)]])
