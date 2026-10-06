"""Fully local Vosk voice controller; deterministic simulation also available."""
import argparse,json,pathlib,queue,time
from .controller import Controller
class Simulation:
    def __init__(self):self.on=False
    def relay(self,on):self.on=on
    def current_ma(self):return 80.0 if self.on else 0.0
    def motion(self):return True
    def close(self):pass
def simulated(commands):
    h=Simulation();c=Controller(h)
    try:
        for command in commands:print(json.dumps(c.command(command)))
    finally:c.close();h.close()
def voice(model_path,device):
    import sounddevice as sd
    from vosk import Model,KaldiRecognizer
    from .hardware import Hardware
    if not pathlib.Path(model_path).is_dir():raise ValueError('Supply an unpacked local Vosk model directory')
    model=Model(model_path);recognizer=KaldiRecognizer(model,16000,json.dumps(['lamp on','lamp off','status','[unk]']))
    q=queue.Queue(maxsize=8)
    def audio(data,frames,timing,status):
        if status:print('Audio overrun/underflow; recognition may be incomplete',flush=True)
        try:q.put_nowait(bytes(data))
        except queue.Full:pass # Drop new blocks rather than blocking audio callback.
    hardware=Hardware();controller=Controller(hardware)
    try:
        with sd.RawInputStream(samplerate=16000,blocksize=1600,device=device,dtype='int16',channels=1,callback=audio):
            while True:
                # Safety/current poll each 100ms audio block; recognition/network-free.
                print(json.dumps(controller.tick()),flush=True)
                try:data=q.get(timeout=.1)
                except queue.Empty:continue
                if recognizer.AcceptWaveform(data):
                    text=json.loads(recognizer.Result()).get('text','')
                    if text:print(json.dumps(controller.command(text)),flush=True)
    finally:controller.close();hardware.close()
def main():
    p=argparse.ArgumentParser();p.add_argument('--simulate',nargs='*');p.add_argument('--model');p.add_argument('--device');a=p.parse_args()
    if a.simulate is not None:simulated(a.simulate)
    elif a.model:voice(a.model,a.device)
    else:p.error('Use --simulate "lamp on" status "lamp off" or --model PATH')
if __name__=='__main__':main()
