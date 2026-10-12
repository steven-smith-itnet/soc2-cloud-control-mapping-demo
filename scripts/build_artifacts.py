#!/usr/bin/env python3
"""Rebuild only synthetic baseline, inline guides and public learning-kit ZIP."""
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def build():
    subprocess.run([sys.executable,'-m','unittest','discover','-s','tests'],cwd=ROOT,check=True)
    with tempfile.TemporaryDirectory() as temp:
        generated=Path(temp)/'baseline'
        subprocess.run([sys.executable,'scripts/evaluate.py','--as-of','2026-09-30T15:00:00Z','--out',str(generated)],cwd=ROOT,check=True)
        shutil.copytree(generated,ROOT/'evidence/examples/baseline',dirs_exist_ok=True)
    subprocess.run([sys.executable,'scripts/verify_evidence.py','evidence/examples/baseline'],cwd=ROOT,check=True)
    path=ROOT/'data/program.json'
    program=json.loads(path.read_text())
    program['guides']=[dict(id=f.name[:2],title=f.read_text().splitlines()[0].removeprefix('# '),content=f.read_text()) for f in sorted((ROOT/'docs').glob('*.md'))]
    path.write_text(json.dumps(program,indent=2,ensure_ascii=False)+'\n')
    downloads=ROOT/'downloads';downloads.mkdir(exist_ok=True)
    files=[ROOT/'README.md',ROOT/'requirements-live.txt',ROOT/'index.html']
    for folder in ('docs','data','web','scripts','tests','evidence/examples'):
        files.extend(p for p in sorted((ROOT/folder).rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and not p.name.endswith('.local.json'))
    with zipfile.ZipFile(downloads/'soc2-learning-kit.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            # Deterministic timestamps for reviewable binary changes.
            info=zipfile.ZipInfo('soc2-learning-kit/'+file.relative_to(ROOT).as_posix(),(2026,10,3,12,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,file.read_bytes())
    print(f'Embedded {len(program["guides"])} guides and packaged {len(files)} files')

if __name__=='__main__':build()
