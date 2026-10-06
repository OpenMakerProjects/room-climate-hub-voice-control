import unittest
from src.controller import Controller
class Fake:
    def __init__(self):self.on=False;self.current=10
    def relay(self,on):self.on=on
    def current_ma(self):return self.current
    def motion(self):return True
class Tests(unittest.TestCase):
    def setUp(self):self.h=Fake();self.c=Controller(self.h)
    def test_commands(self):
        self.assertFalse(self.h.on);self.assertTrue(self.c.command('lamp on')['relay_on']);self.assertTrue(self.c.command('status')['relay_on']);self.assertFalse(self.c.command('lamp off')['relay_on'])
    def test_unknown(self):self.assertFalse(self.c.command('turn on everything')['command_accepted']);self.assertFalse(self.h.on)
    def test_fault_and_explicit_recovery(self):
        self.c.command('lamp on');self.h.current=301;self.assertTrue(self.c.tick()['fault']);self.assertFalse(self.h.on)
        self.c.command('lamp on');self.assertFalse(self.h.on);self.h.current=10;self.c.tick();self.assertFalse(self.h.on);self.c.command('lamp on');self.assertTrue(self.h.on)
    def test_invalid(self):
        for current in [float('nan'),float('inf'),True,None,-301]:
            self.h.current=current;self.assertTrue(self.c.tick()['fault']);self.assertFalse(self.h.on)
    def test_cleanup(self):self.c.command('lamp on');self.c.close();self.assertFalse(self.h.on)
if __name__=='__main__':unittest.main()
