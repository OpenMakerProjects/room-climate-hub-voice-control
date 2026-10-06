"""BCM17 PIR, BCM27 active-high 3.3V-compatible relay; INA219 bus 1 @ 0x40."""
class Hardware:
    def __init__(self):
        from gpiozero import DigitalInputDevice,DigitalOutputDevice
        from smbus2 import SMBus
        self.output=DigitalOutputDevice(27,active_high=True,initial_value=False)
        self.pir=DigitalInputDevice(17,pull_up=False)
        self.bus=SMBus(1)
        # 32V range, +/-320mV shunt, 12-bit conversions, continuous shunt+bus.
        self.write(0,0x399f);self.write(5,4096) # 0.1 ohm shunt, current LSB 100uA.
    def write(self,reg,value):self.bus.write_i2c_block_data(0x40,reg,[(value>>8)&255,value&255])
    def read(self,reg):
        b=self.bus.read_i2c_block_data(0x40,reg,2);return (b[0]<<8)|b[1]
    def current_ma(self):
        calibration=self.read(5);bus=self.read(2)
        if calibration!=4096 or bus&1:raise ValueError('INA219 reset or overflow')
        raw=self.read(4);raw=raw-65536 if raw&0x8000 else raw
        return raw*0.1
    def motion(self):return self.pir.value
    def relay(self,on):self.output.value=bool(on)
    def close(self):self.output.off();self.output.close();self.pir.close();self.bus.close()
