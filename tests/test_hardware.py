import unittest
from src.hardware import Hardware
class Bus:
    def __init__(self,values):self.values=values;self.written=[]
    def read_i2c_block_data(self,address,reg,n):assert address==0x40 and n==2;v=self.values[reg];return [v>>8,v&255]
    def write_i2c_block_data(self,address,reg,data):self.written.append((address,reg,data))
class Tests(unittest.TestCase):
    def fixture(self,raw,cal=4096,flags=0):
        h=Hardware.__new__(Hardware);h.bus=Bus({5:cal,2:flags,4:raw});return h
    def test_signed_scale(self):self.assertEqual(self.fixture(800).current_ma(),80);self.assertEqual(self.fixture(65536-100).current_ma(),-10)
    def test_fail_calibration_or_overflow(self):
        for h in [self.fixture(0,cal=0),self.fixture(0,flags=1)]:
            with self.assertRaises(ValueError):h.current_ma()
    def test_write_endian(self):
        h=self.fixture(0);h.write(5,4096);self.assertEqual(h.bus.written,[(0x40,5,[16,0])])
if __name__=='__main__':unittest.main()
