import unittest
from indi.message import GetProperties
from indi.message import IndiMessage
from ddt import ddt, data, unpack


@ddt
class TestIndiMessage(unittest.TestCase):

    messages = [
        (
            bytes('<getProperties device="CAMERA" version="2.0" />', encoding='ascii'),
            GetProperties(version='2.0', device='CAMERA'),
        ),
        (
            bytes('<getProperties version="2.0" />', encoding='ascii'),
            GetProperties(version='2.0'),
        ),
    ]

    @data(*messages)
    @unpack
    def test_from_string(self, in_xml, in_msg):
        msg = IndiMessage.from_string(in_xml)
        self.assertDictEqual(in_msg.__dict__, msg.__dict__)

    @data(*messages)
    @unpack
    def test_to_string(self, in_xml, in_msg):
        xml = in_msg.to_string()
        self.assertEqual(in_xml, xml)
