#!/usr/bin/env python3
"""Check the public package; does not validate geometry or printing behavior."""

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


def public_files(root):
    files = [root / name for name in (
        '.gitignore', 'SKILL.md', 'README.md', 'README.en.md',
        'CONTRIBUTING.md', 'CHANGELOG.md', 'LICENSE',
        'agents/openai.yaml', 'tools/validate.py',
        '.github/PULL_REQUEST_TEMPLATE.md',
    )]
    files += sorted((root / 'references').glob('*.md'))
    files += sorted((root / '.github/ISSUE_TEMPLATE').glob('*.md'))
    return files


def unfenced(text):
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text,
                  flags=re.MULTILINE | re.DOTALL)


def anchors(text):
    seen = {}
    result = set()
    for heading in re.findall(r'^#{1,6}\s+(.+)$', unfenced(text), re.MULTILINE):
        slug = ''.join(c for c in heading.lower()
                       if c in '-_ ' or unicodedata.category(c)[0] not in 'PS')
        slug = slug.replace(' ', '-')
        count = seen.get(slug, 0)
        result.add(slug if count == 0 else f'{slug}-{count}')
        seen[slug] = count + 1
    return result


def validate(root):
    errors = []
    files = public_files(root)
    allowed = {p.resolve() for p in files}
    for path in files:
        if not path.is_file():
            errors.append(f'Missing public file: {path.relative_to(root)}')
    if errors:
        return errors, len(files), 0

    entry = (root / 'SKILL.md').read_text(encoding='utf-8')
    frontmatter = re.match(r'^---\n(.*?)\n---\n', entry, re.DOTALL)
    if not frontmatter:
        errors.append('SKILL.md requires YAML frontmatter')
    else:
        for key in ('name', 'description'):
            if not re.search(rf'^{key}:\s*\S.+$', frontmatter[1], re.MULTILINE):
                errors.append(f'Missing skill field: {key}')
        if not re.search(r'^name: print-aware-modeling$', frontmatter[1], re.MULTILINE):
            errors.append('Skill name must be print-aware-modeling')
    ui = (root / 'agents/openai.yaml').read_text(encoding='utf-8')
    if '$print-aware-modeling' not in ui:
        errors.append('UI prompt must name the skill')

    links = 0
    for path in files:
        if path.suffix not in ('.md', '.yaml'):
            continue
        text = path.read_text(encoding='utf-8')
        for pattern in (r'/Users/', r'/private/(?:tmp|var)/', r'file://',
                        r'用户已持续授权', r'gh[pousr]_[A-Za-z0-9]{20,}',
                        r'github_pat_[A-Za-z0-9_]{20,}'):
            if re.search(pattern, text):
                errors.append(f'{path.relative_to(root)}: local/private pattern {pattern}')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', unfenced(text)):
            target = target.strip().strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
            links += 1
            if dest not in allowed or not dest.is_file():
                errors.append(f'{path.relative_to(root)}: unpublished or missing link {target}')
            elif parsed.fragment and dest.suffix == '.md':
                if unquote(parsed.fragment) not in anchors(dest.read_text(encoding='utf-8')):
                    errors.append(f'{path.relative_to(root)}: missing heading {target}')

    if (root / '.git').exists():
        tracked = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z'])
        for name in tracked.decode().split('\0'):
            if name and (root / name).resolve() not in allowed:
                errors.append(f'Unexpected tracked file: {name}')
    return errors, len(files), links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, count, links = validate(args.root.resolve())
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    if errors:
        return 1
    print(f'PASS: {count} public files; {links} local links; metadata and publication checks.')
    print('Geometry, slicer paths, print results and external URLs were not tested.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
