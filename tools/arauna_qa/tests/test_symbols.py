import tempfile
import unittest
from pathlib import Path

from arauna_qa.symbols import SymbolTable


class SymbolTableTests(unittest.TestCase):
    def test_parses_pokeemerald_sym_format(self):
        text = """02000010 g      00000004 gMain
03000020 l      00000001 sLockFieldControls
"""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "game.sym"
            path.write_text(text, encoding="utf-8")
            table = SymbolTable.from_file(path)

        self.assertEqual(table.address("gMain"), 0x02000010)
        self.assertEqual(table.require("gMain").size, 4)
        self.assertEqual(table.address("sLockFieldControls"), 0x03000020)

    def test_missing_symbol_is_actionable(self):
        table = SymbolTable({})
        with self.assertRaisesRegex(KeyError, "make syms"):
            table.require("gMain")


if __name__ == "__main__":
    unittest.main()
