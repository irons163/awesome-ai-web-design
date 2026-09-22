#!/usr/bin/env python3
"""Stage only public website files for static hosting, after build.py."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dist'


def main():
    if OUTPUT.is_symlink():
        raise RuntimeError('dist must be a regular build directory')
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    for name in ('index.html', 'README.md', 'ATTRIBUTION.md', 'LICENSE', 'CONTRIBUTING.md'):
        shutil.copy2(ROOT / name, OUTPUT / name)
    for name in ('assets', 'design-md', 'prompts'):
        shutil.copytree(ROOT / name, OUTPUT / name)
    print(f'Staged public website in {OUTPUT}')


if __name__ == '__main__':
    main()
