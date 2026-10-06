"""Fail-off low-voltage lamp control; hardware-independent policy."""
import math
class Controller:
    def __init__(self, hardware, limit_ma=300):
        self.hardware=hardware;self.limit_ma=limit_ma;self.on=False;self.fault=False
        hardware.relay(False)
    def tick(self):
        try:
            current=self.hardware.current_ma();motion=bool(self.hardware.motion())
            valid=isinstance(current,(int,float)) and not isinstance(current,bool) and math.isfinite(current) and abs(current)<=self.limit_ma
        except (OSError,ValueError):current=None;motion=False;valid=False
        if not valid:self.on=False;self.fault=True;self.hardware.relay(False)
        else:self.fault=False
        return dict(project_id=3,relay_on=self.on,motion=motion,current_ma=current if valid else None,fault=self.fault)
    def command(self,text):
        status=self.tick();text=text.strip().lower()
        if text=='lamp off':self.on=False
        elif text=='lamp on' and not self.fault:self.on=True
        elif text!='status':return dict(status,command_accepted=False)
        self.hardware.relay(self.on)
        return dict(self.tick(),command_accepted=True)
    def close(self):self.on=False;self.hardware.relay(False)
