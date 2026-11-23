import tempfile
import unittest
from pathlib import Path
from te_dhenat import lexo_fasta


class TestTeDhenat(unittest.TestCase):
    def shkruaj(self, text, suffix='.fa'):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        p = Path(folder.name)/('input'+suffix)
        p.write_text(text, encoding='utf-8-sig')
        return p

    def test_fasta_me_shume_rreshta(self):
        records = list(lexo_fasta(self.shkruaj('>p1\nacde\nFG\n>p2\nAAAA\n')))
        self.assertEqual(records, [{'id':'p1','sekuenca':'ACDEFG'}, {'id':'p2','sekuenca':'AAAA'}])

    def test_fasta_refuzon_te_dhena_te_pasakta(self):
        for text in ('', 'AAAA', '>\nAAAA', '>p1\n>p2\nAA', '>p1\nAAXA'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                list(lexo_fasta(self.shkruaj(text)))
