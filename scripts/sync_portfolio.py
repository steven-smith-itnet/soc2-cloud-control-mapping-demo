#!/usr/bin/env python3
"""Copy the reviewed SOC 2 experience and synthetic resources into Bright Ridge."""
import argparse
import shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sync(portfolio):
    if not (portfolio/'src/Soc2CloudPage.jsx').is_file() or not (portfolio/'package.json').is_file():
        raise ValueError('Expected the existing Bright Ridge portfolio project')
    target=portfolio/'src/soc2';target.mkdir(exist_ok=True)
    for source,name in [('web/experience.js','experience.js'),('web/experience.css','experience.css'),('data/program.json','program.json'),('evidence/examples/baseline/results.json','baseline.json')]:
        shutil.copy2(ROOT/source,target/name)
    public=portfolio/'public/soc2-cloud-resources'
    for folder in ('data','downloads','evidence/examples'):
        source=ROOT/folder
        for file in source.rglob('*'):
            if file.is_file() and not file.name.endswith('.local.json'):
                dest=public/file.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(file,dest)
    print('Updated SOC 2 renderer, bundled data and synthetic public downloads in '+str(portfolio))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--portfolio',type=Path,required=True)
    sync(parser.parse_args().portfolio.resolve())
