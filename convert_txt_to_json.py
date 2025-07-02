import argparse
import json
import os
import re
from pathlib import Path

def parse_content(text: str):
    """Attempt to parse text as JSON or simple key:value pairs."""
    text = text.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    data = {}
    for line in text.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    if data:
        return data
    raise ValueError('Content is neither JSON nor key:value pairs')

def convert_file(path: Path, output_dir: Path, force: bool = False):
    with path.open('r', encoding='utf-8') as f:
        content = f.read()
    try:
        data = parse_content(content)
    except Exception as e:
        print(f'Skipping {path}: {e}')
        return
    output_path = output_dir / (path.stem + '.json')
    if output_path.exists() and not force:
        print(f'Skipping {path}: {output_path} already exists')
        return
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Converted {path} -> {output_path}')

def main():
    parser = argparse.ArgumentParser(description='Convert .txt files to .json')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to search for .txt files')
    parser.add_argument('-o', '--output', default=None, help='Output directory (defaults to same as input)')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing .json files')
    args = parser.parse_args()

    base_dir = Path(args.directory)
    output_dir = Path(args.output) if args.output else base_dir
    for path in base_dir.rglob('*.txt'):
        convert_file(path, output_dir, force=args.force)

if __name__ == '__main__':
    main()
