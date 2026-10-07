import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_question_corpus.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class CorpusValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'corpus.csv'
        self.schema = json.loads(validator.SCHEMA_PATH.read_text())
        self.header = list(self.schema['properties'])
        with validator.DEFAULT_FILES[1].open(encoding='utf-8', newline='') as f:
            self.row = next(csv.DictReader(f))

    def write(self, rows=None, header=None):
        with self.path.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=header or self.header, extrasaction='ignore')
            writer.writeheader()
            writer.writerows([self.row] if rows is None else rows)
        return validator.validate_file(self.path)

    def assert_error(self, field):
        errors = self.write()
        self.assertTrue(any(field in error for error in errors), errors)
        self.assertTrue(all('row 2' in error for error in errors), errors)

    def test_valid_csv(self):
        self.assertEqual(self.write(), [])

    def test_missing_column(self):
        self.assertIn('missing columns', self.write(header=self.header[1:])[0])

    def test_invalid_enum(self):
        self.row['outcome'] = 'MAYBE'
        self.assert_error('outcome')

    def test_invalid_date(self):
        for date in ['2026-02-30', '2026-2-01', 'yesterday']:
            self.row['checked_at'] = date
            self.assert_error('checked_at')

    def test_duplicate_id(self):
        errors = self.write(rows=[self.row, self.row])
        self.assertTrue(any('row 3' in e and 'duplicate ID' in e for e in errors))

    def test_invalid_url(self):
        for url in ['example.com/thread', 'ftp://example.com', 'https://',
                    'https://user:secret@127.0.0.1', 'https://example.com:bad', 'https://exa mple.com']:
            self.row['source_url'] = url
            self.assert_error('source_url')

    def test_optional_blank_allowed(self):
        self.row['published_at'] = ''
        self.assertEqual(self.write(), [])

    def test_required_blank_forbidden(self):
        self.row['source_url'] = ''
        self.assert_error('source_url')

    def test_whitespace_forbidden(self):
        self.row['site_name'] = '   '
        self.assert_error('site_name')

    def test_empty_template(self):
        self.assertEqual(self.write(rows=[]), [])

    def test_actual_files(self):
        for path in validator.DEFAULT_FILES:
            self.assertEqual(validator.validate_file(path), [])

    def test_nested_enum(self):
        self.row['connection_devices'] = '[{"kind":"HUB","driver_used":"UNKNOWN","power_supplied":"UNKNOWN"}]'
        self.assert_error('connection_devices[0].kind')

    def test_nested_required(self):
        self.row['displays'] = '[{}]'
        self.assert_error('displays[0].identity_certainty')

    def test_array_and_numeric_types(self):
        for field, value in [('displays', '{}'), ('independent_case_count', 'true'),
                             ('source_release_year', '"2020"'), ('pd_watts', 'NaN')]:
            with self.subTest(field=field):
                old = self.row[field]
                self.row[field] = value
                self.assert_error(field)
                self.row[field] = old

    def test_malformed_json(self):
        self.row['displays'] = '[broken'
        self.assert_error('displays')

    def test_header_order(self):
        self.assertTrue(self.write(header=list(reversed(self.header))))

    def test_wrong_width(self):
        self.path.write_text(','.join(self.header) + '\nUQ-0001\n')
        self.assertIn('cells', validator.validate_file(self.path)[0])

    def test_no_header(self):
        self.path.write_text('')
        self.assertIn('missing header', validator.validate_file(self.path)[0])

    def test_bom(self):
        self.write()
        self.path.write_text('\ufeff' + self.path.read_text())
        self.assertEqual(validator.validate_file(self.path), [])

    def test_conflict_gate(self):
        self.row['official_alignment'] = 'CONFLICT'
        self.assert_error('conflict_status')

    def test_usage_gate(self):
        self.row['usable_for_compatibility'] = 'YES'
        self.assert_error('usable_for_compatibility')

    def test_ai_data_rejected(self):
        self.row['reliability_grade'] = 'X'
        self.assert_error('reliability_grade')

    def test_spreadsheet_formula_rejected(self):
        self.row['symptoms'] = '=HYPERLINK("https://example.com")'
        self.assert_error('symptoms')

    def test_malformed_evidence_does_not_crash(self):
        self.row['independent_case_urls'] = '[{}]'
        self.assert_error('independent_case_urls')

    def test_schema_enum_examples_are_valid(self):
        def visit(node):
            if isinstance(node, dict):
                if 'enum' in node:
                    for example in node.get('examples', []):
                        self.assertIn(example, node['enum'])
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)
        visit(self.schema)

    def test_cli_default_checks_both(self):
        self.assertEqual(validator.main([]), 0)


if __name__ == '__main__':
    unittest.main()
