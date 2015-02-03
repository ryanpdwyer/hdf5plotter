
import StringIO
import unittest
from collections import OrderedDict
from numpy.testing import assert_array_almost_equal_nulp
import numpy as np
from hdf5plotter.csvutil import parse_csv



class TestParseCsv(unittest.TestCase):
    def setUp(self):
        self.csv = StringIO.StringIO("""\
#; Example INI Comment
#[Example]
#a=1
col1,col2
1.0,2.0
2.0,3.1
3.0,4.2
""")
        self.col1 = np.array([1.0, 2.0, 3.0])
        self.col2 = np.array([2.0, 3.1, 4.2])

    def test_parse_csv(self):
        csv = parse_csv(self.csv)
        assert_array_almost_equal_nulp(csv.col1, self.col1)
        assert_array_almost_equal_nulp(csv.col2, self.col2)

    def test_parse_ini(self):
        csv = parse_csv(self.csv)
        # Note: This is not necessarily the behavior we want, but it works
        # for now.
        # Conversion to actual numbers would be nice.
        od = OrderedDict([('Example', OrderedDict([('a', '1')]))])
        self.assertEquals(csv.metadata, od)