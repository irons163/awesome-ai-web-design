#!/usr/bin/env python3
"""Package the public site and restore its hash-verified media for static hosting."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(file):
    result = hashlib.sha256()
    with file.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def contained(root, relative):
    name = Path(relative)
    if name.is_absolute() or any(part in ('.', '..') for part in relative.split('/')) or '\\' in relative:
        raise ValueError('Unsafe public media path: ' + relative)
    file = (root / name).resolve()
    file.relative_to(root.resolve())
    return file


def package(output):
    source = ROOT / 'public'
    if not (source / 'index.html').is_file():
        raise ValueError('Stage the public site first: node scripts/build_site.mjs --output public')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a new or empty output directory; existing output is preserved')
    if output == ROOT or source == output or source in output.parents or output in source.parents:
        raise ValueError('Output must be outside the source webroot')
    archive = output.parent / (output.name + '.tar.gz')
    if archive.exists():
        raise ValueError('Archive already exists; choose another output name')
    output.mkdir(parents=True, exist_ok=True)
    destination = output / 'www'

    def ignore(directory, names):
        return [name for name in names if name.startswith('.') or name in ('_headers', '_redirects')]

    # Only the already-staged public dependency closure enters the webroot.
    for file in source.rglob('*'):
        if file.is_symlink():
            raise ValueError('Public staging must not contain symlinks: ' + str(file))
    shutil.copytree(source, destination, ignore=ignore)
    restored = []
    groups = [
        ('data/hosting-assets.json', ROOT, destination),
        ('data/hosted-official-media.json', ROOT / '.stitch-work/current-official', destination / 'official-drafts'),
    ]
    for config_name, original_root, public_root in groups:
        config = json.loads((ROOT / config_name).read_text())
        for asset in config['assets']:
            original = contained(original_root, asset['path'])
            if original.stat().st_size != asset['bytes'] or digest(original) != asset['sha256']:
                raise ValueError('Preserved original media changed: ' + asset['path'])
            target = contained(public_root, asset['path'])
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and digest(target) != asset['sha256']:
                raise ValueError('Public media collision: ' + asset['path'])
            shutil.copyfile(original, target)
            restored.append(dict(path=target.relative_to(destination).as_posix(),
                                 bytes=asset['bytes'], sha256=asset['sha256']))

    server_files = ('nginx.conf', 'Caddyfile', 'compose.caddy.yaml', 'README.md')
    for filename in server_files:
        shutil.copyfile(ROOT / 'deploy/vps' / filename, output / filename)
    files = sorted(p for p in destination.rglob('*') if p.is_file())
    manifest = dict(
        format_version=1,
        source_git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        hosting='static', database_required=False, node_runtime_required=False,
        webroot_bytes=sum(file.stat().st_size for file in files), file_count=len(files),
        restored_media_count=len(restored), restored_media_bytes=sum(row['bytes'] for row in restored),
        restored_media=restored,
        files=[dict(path=file.relative_to(destination).as_posix(), bytes=file.stat().st_size, sha256=digest(file)) for file in files],
    )
    (output / 'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

    def portable(info):
        info.uid = info.gid = 0
        info.uname = info.gname = ''
        info.mode = 0o755 if info.isdir() else 0o644
        return info

    with tarfile.open(archive, 'w:gz', compresslevel=6) as bundle:
        for name in ('www', *server_files, 'MANIFEST.json'):
            bundle.add(output / name, arcname=name, filter=portable)
    return dict(archive=str(archive), archive_bytes=archive.stat().st_size,
                archive_sha256=digest(archive), webroot_bytes=manifest['webroot_bytes'],
                file_count=len(files), restored_media_count=len(restored),
                restored_media_bytes=manifest['restored_media_bytes'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '.test-artifacts/vps-ready')
    args = parser.parse_args()
    try:
        result = package(args.output.resolve())
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False))
