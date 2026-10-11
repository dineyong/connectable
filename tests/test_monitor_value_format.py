import json
import subprocess
import unittest
from pathlib import Path
from scripts.monitor_value_format import formatted, fact_text

ROOT = Path(__file__).resolve().parents[1]

class MonitorValueFormatTests(unittest.TestCase):
    def test_port_direction_and_qualifying_note_are_not_inferred(self):
        value = {'version': '1.4', 'count': 2, 'note': 'direction unspecified'}
        self.assertEqual(formatted(value), '버전: 1.4\n개수: 2\n조건 메모: direction unspecified')
        self.assertNotIn('입력', formatted(value))

    def test_zero_false_null_and_unknown_keys_survive(self):
        self.assertEqual(formatted({'future_key': [0, False, None]}), 'future_key: [0, 미지원, 미확인]')
        self.assertEqual(formatted({}), '{}')
        self.assertEqual(formatted([]), '[]')

    def test_units_axes_and_estimate_survive(self):
        text = formatted({'unit': 'cm', 'axes': 'W,H,D', 'with_stand': [61.22, 53.81, 21.5], 'estimate_status': 'MANUFACTURER_ESTIMATE'})
        for token in ['cm', 'W,H,D', '61.22', '53.81', '21.5', '스탠드 포함', '제조사 추정', 'MANUFACTURER_ESTIMATE']:
            self.assertIn(token, text)

    def test_browser_and_static_formatter_agree_for_all_real_values(self):
        data = json.loads((ROOT/'data/research/monitor-expansion/official_specs.json').read_text())
        values = [f['value'] for p in data['products'] for f in p['facts']]
        values += [None, False, 0, {}, [], {'future_key': '<img src=x onerror=alert(1)>', 'constructor': 'literal'}]
        code = "const fs=require('fs');const f=require('./web/monitor-value-format.js').format;process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(f)));"
        result = subprocess.run(['node', '-e', code], input=json.dumps(values), text=True, capture_output=True, check=True, cwd=ROOT)
        self.assertEqual(json.loads(result.stdout), [formatted(v) for v in values])

    def test_outer_unit_is_group_label_not_attached_to_last_number(self):
        self.assertEqual(fact_text({'horizontal': 596.73, 'vertical': 335.66}, 'mm'), '가로: 596.73\n세로: 335.66\n단위: mm')
        self.assertEqual(fact_text(96, 'W'), '96 W')

    def test_fact_text_matches_browser_including_units(self):
        data = json.loads((ROOT/'data/research/monitor-expansion/official_specs.json').read_text())
        facts = [f for p in data['products'] for f in p['facts']]
        code = "const fs=require('fs');const f=require('./web/monitor-value-format.js').factText;process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>f(x.value,x.unit))));"
        result = subprocess.run(['node', '-e', code], input=json.dumps(facts), text=True, capture_output=True, check=True, cwd=ROOT)
        self.assertEqual(json.loads(result.stdout), [fact_text(f['value'], f['unit']) for f in facts])
