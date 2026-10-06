import hashlib,json,pathlib,re,subprocess,sys,xml.etree.ElementTree as ET
from decode_project_image import validate_png
ROOT=pathlib.Path(__file__).resolve().parents[1]
for path in ['README.md','LICENSE','docs/circuit-diagram.svg','docs/images/project-overview.png','requirements.txt','src/controller.py','src/hardware.py','src/main.py','tests/test_controller.py','tests/test_hardware.py']:assert (ROOT/path).is_file(),path
readme=(ROOT/'README.md').read_text(encoding='utf-8')
for heading in ['Objectives','Architecture','BOM','Prerequisites','Exact pin','Assembly','Setup','Configuration','Telemetry','Validation','Troubleshooting','Limitations','Future work','Contributing']:assert heading.lower() in readme.lower(),heading
for target in re.findall(r'\]\(([^)]+)\)',readme):
    if not target.startswith(('https://','http://','#')):assert (ROOT/target.split('#')[0]).exists(),target
svg=(ROOT/'docs/circuit-diagram.svg').read_text(encoding='utf-8');ET.fromstring(svg)
assert not re.search(r'<(?:script|foreignObject)|(?:href|src)=["\']https?://',svg)
for label in ['BCM17','BCM27','BCM2','BCM3','0x40','3.3V','VIN+','VIN−']:assert label in svg,label
png=(ROOT/'docs/images/project-overview.png').read_bytes();dimensions=validate_png(png);manifest=json.loads((ROOT/'docs/images/project-overview.manifest.json').read_text(encoding='utf-8'))
assert hashlib.sha256(png).hexdigest()==manifest['sha256'] and len(png)==manifest['bytes'] and list(dimensions)==manifest['dimensions']
assert not list((ROOT/'docs/images').glob('*.b64.*'))
assert 'MIT License' in (ROOT/'LICENSE').read_text(encoding='utf-8')
for p in ROOT.rglob('*'):
    if not p.is_file() or any(x in p.parts for x in ['.git','.venv','__pycache__','models']):continue
    if p.suffix!='.png':assert not re.search(r'(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-proj-[A-Za-z0-9_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY)',p.read_text(encoding='utf-8',errors='ignore')),p
subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'-m','compileall','-q','src','tools','tests'],cwd=ROOT,check=True)
subprocess.run([sys.executable,'-m','src.main','--simulate','lamp on','status','lamp off'],cwd=ROOT,check=True)
print('PASS: controller/I2C adapter/transport tests; Python build and simulation; SVG; PNG; links; license; credential patterns')
