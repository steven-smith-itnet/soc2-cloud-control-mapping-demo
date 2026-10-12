#!/usr/bin/env python3
"""Recompute a local manifest. This does not authenticate the manifest's origin."""
import argparse
import hashlib
import json
from pathlib import Path

def verify(directory):
    manifest=json.loads((directory/'manifest.json').read_text())
    if not isinstance(manifest,dict) or not manifest:
        raise ValueError('Manifest must be a nonempty mapping')
    found={p.name for p in directory.iterdir() if p.is_file() and p.name!='manifest.json'}
    if found != set(manifest):
        raise ValueError('Evidence file set differs from manifest')
    for name, expected in manifest.items():
        if Path(name).name != name or name in ('.','..','manifest.json'):
            raise ValueError('Invalid manifest path')
        file=directory/name
        if file.is_symlink() or hashlib.sha256(file.read_bytes()).hexdigest()!=expected:
            raise ValueError('Hash mismatch or symbolic link: '+name)
    return len(manifest)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path)
    try:
        print(f'Validated {verify(p.parse_args().directory)} files against the supplied manifest')
    except (ValueError,OSError) as error:
        p.exit(1,str(error)+'\n')
