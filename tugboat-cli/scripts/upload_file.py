#!/usr/bin/env python3
"""Preview or execute one reviewed file upload to a Tugboat service.

File content is encoded into the remote argv, so use only sanitized public data.
No persistent command file is created. Existing destination files are preserved
unless --overwrite is explicitly selected after human review.
"""
import argparse
import base64
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys


def build_command(data: bytes, destination: str, overwrite: bool = False) -> list[str]:
    path = PurePosixPath(destination)
    if not path.is_absolute() or '..' in path.parts or any(ord(char) < 32 for char in destination):
        raise ValueError('destination must be an absolute service file path without traversal or control characters')
    encoded = base64.b64encode(data).decode('ascii')
    # Quote the destination as shell syntax; JSON alone is not shell escaping.
    protect = '' if overwrite else 'set -C; '
    script = f"set -eu; set -o pipefail; {protect}printf %s {shlex.quote(encoded)} | base64 -d > {shlex.quote(destination)}"
    return ['bash', '-c', script]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--service', required=True, help='Exact reviewed destination service ID')
    parser.add_argument('--destination', required=True, help='Absolute file path inside the reviewed service')
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting the exact destination after review')
    parser.add_argument('--execute', action='store_true', help='Perform the external write; default only reports its scope')
    args = parser.parse_args(argv)
    if not re.fullmatch(r'[A-Za-z0-9_-]+', args.service):
        parser.error('service must be an ID, without whitespace or shell syntax')
    try:
        data = args.source.read_bytes()
        command = build_command(data, args.destination, args.overwrite)
        print(f'{"Upload" if args.execute else "Preview only"}: {args.source} ({len(data)} bytes) to service {args.service}, {args.destination}; overwrite={args.overwrite}')
        if not args.execute:
            print('No service was contacted. Review contents, destination, and exposure before using --execute.')
            return 0
        result = subprocess.run(['tugboat', 'shell', args.service, 'command=' + json.dumps(command)], check=False)
        return result.returncode
    except (OSError, ValueError) as error:
        # Do not print subprocess argv: it contains the encoded file content.
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
