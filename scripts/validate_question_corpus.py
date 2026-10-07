"""Validate corpus CSV against the documented schema subset, using stdlib only.

This is not a general JSON Schema engine. It covers all keywords used in our
schema, plus corpus review gates; it does not verify the truth of source claims.
"""
import argparse
import csv
import datetime
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / 'schemas/user-question.schema.json'
DEFAULT_FILES = [ROOT / 'data/research/user_questions.csv',
                 ROOT / 'data/research/user_questions.example.csv']


def valid_url(value):
    try:
        parsed = urlsplit(value)
        port = parsed.port
        return (parsed.scheme in ('https', 'http') and bool(parsed.hostname)
                and not parsed.username and not parsed.password
                and not re.search(r'\s', value)
                and (port is None or 0 < port < 65536))
    except ValueError:
        return False


def check_value(value, spec, path):
    errors = []
    kind = spec['type']
    matches = {'string': isinstance(value, str),
               'integer': type(value) is int,
               'number': type(value) in (int, float),
               'array': isinstance(value, list),
               'object': isinstance(value, dict)}
    if not matches[kind]:
        return [f'{path}: expected {kind}']
    if 'enum' in spec and value not in spec['enum']:
        errors.append(f'{path}: invalid enum {value!r}')
    if kind == 'string':
        if not value.strip():
            errors.append(f'{path}: empty value; omit optional JSON keys')
        if value.startswith(('=', '+', '-', '@')):
            errors.append(f'{path}: spreadsheet formula prefix forbidden')
        if 'pattern' in spec and not re.fullmatch(spec['pattern'], value):
            errors.append(f'{path}: invalid pattern')
        if spec.get('format') == 'date':
            try:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                    raise ValueError()
                datetime.date.fromisoformat(value)
            except ValueError:
                errors.append(f'{path}: invalid date (YYYY-MM-DD)')
        if spec.get('format') == 'uri' and not valid_url(value):
            errors.append(f'{path}: invalid public HTTP(S) URL')
    elif kind in ('integer', 'number'):
        if not math.isfinite(value):
            errors.append(f'{path}: non-finite number')
        if 'minimum' in spec and value < spec['minimum']:
            errors.append(f'{path}: below minimum')
        if 'exclusiveMinimum' in spec and value <= spec['exclusiveMinimum']:
            errors.append(f'{path}: must exceed minimum')
    elif kind == 'array':
        for index, item in enumerate(value):
            errors.extend(check_value(item, spec['items'], f'{path}[{index}]'))
    elif kind == 'object':
        props = spec['properties']
        for key in spec.get('required', []):
            if key not in value:
                errors.append(f'{path}.{key}: required value missing')
        for key, item in value.items():
            if key not in props:
                errors.append(f'{path}.{key}: unknown field')
            else:
                errors.extend(check_value(item, props[key], f'{path}.{key}'))
    return errors


def check_review(row):
    errors = []
    if row.get('reliability_grade') == 'X':
        errors.append('reliability_grade: source-free AI data forbidden')
    if row.get('official_alignment') == 'CONFLICT' and (
            row.get('conflict_status') != 'CONFLICT'
            or row.get('review_status') != 'NEEDS_REVIEW'):
        errors.append('conflict_status: official conflict requires CONFLICT/NEEDS_REVIEW')
    if row.get('official_alignment') in ('MATCH', 'CONFLICT') and not row.get('official_source_urls'):
        errors.append('official_source_urls: comparison requires official references')
    count = row.get('independent_case_count')
    urls = row.get('independent_case_urls', [])
    valid_urls = isinstance(urls, list) and all(isinstance(url, str) for url in urls)
    if type(count) is int and valid_urls and count != 1 + len(set(urls)):
        errors.append('independent_case_count: must equal own case plus unique additional URLs')
    if row.get('usable_for_compatibility') == 'YES':
        if (row.get('review_status') != 'REVIEWED'
                or row.get('official_alignment') != 'MATCH'
                or row.get('conflict_status') != 'NONE'
                or row.get('reliability_grade') not in ('A', 'B')
                or type(count) is not int or count < 2
                or row.get('source_identity_certainty') != 'EXACT'
                or row.get('missing_fields')):
            errors.append('usable_for_compatibility: review/evidence gates not satisfied')
    return errors


def validate_file(path, schema=None):
    schema = schema or json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    props = schema['properties']
    errors, ids = [], set()
    try:
        with Path(path).open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.reader(stream, strict=True)
            header = next(reader, None)
            if header is None:
                return [f'{path}: row 1: missing header']
            if header != list(props):
                missing = sorted(set(props) - set(header))
                return [f'{path}: row 1: invalid header/order; missing columns: {missing}']
            for row_number, cells in enumerate(reader, 2):
                prefix = f'{path}: row {row_number} (ending physical line {reader.line_num})'
                if len(cells) != len(header):
                    errors.append(f'{prefix}: expected {len(header)} cells, got {len(cells)}')
                    continue
                row = {}
                for key, cell in zip(header, cells):
                    if cell == '':
                        continue
                    spec = props[key]
                    if spec['type'] == 'string':
                        row[key] = cell
                    else:
                        try:
                            row[key] = json.loads(cell)
                        except (ValueError, RecursionError):
                            errors.append(f'{prefix}: {key}: invalid JSON/numeric cell')
                local = check_value(row, schema, 'record')
                local.extend(check_review(row))
                identifier = row.get('id')
                if identifier in ids:
                    local.append('id: duplicate ID')
                if identifier is not None:
                    ids.add(identifier)
                errors.extend(f'{prefix}: {error}' for error in local)
    except (OSError, UnicodeError, csv.Error, RecursionError) as exc:
        errors.append(f'{path}: file/CSV error: {exc}')
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='*', type=Path)
    args = parser.parse_args(argv)
    failed = False
    for path in args.files or DEFAULT_FILES:
        errors = validate_file(path)
        if errors:
            failed = True
            for error in errors:
                print(error, file=sys.stderr)
        else:
            print(f'PASS: {path}')
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
