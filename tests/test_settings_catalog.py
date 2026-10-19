import importlib.util
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
SPEC = importlib.util.spec_from_file_location("settings_catalog", Path(__file__).resolve().parents[1] / "scripts/settings_catalog.py")
module = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(module)


class CatalogTests(unittest.TestCase):
    def test_flat_formats_comments_and_string_defaults(self):
        rows = module.parse_options('''VERSION = 1,
        // comment
        option Test.A = {type = integer, default = 3, min = 1, max = 9,}
        option Test.B {type = string, default = "Army;Police", page = Test,}
        ''')
        self.assertEqual(rows[0]['max'], '9')
        self.assertEqual(rows[1]['default'], '"Army;Police"')

    def test_duplicate_nested_or_incomplete_fails(self):
        for source in ['option A { type=integer }', 'option A {type=integer, default=1} option A {type=integer, default=2}', 'option A {nested={}}']:
            with self.assertRaises(ValueError): module.parse_options(source)

    def test_html_escapes_data(self):
        result = module.render_html([{'key':'<script>alert(1)</script>'}])
        self.assertIn('&lt;script&gt;', result)
        self.assertNotIn('<td><script>', result)
