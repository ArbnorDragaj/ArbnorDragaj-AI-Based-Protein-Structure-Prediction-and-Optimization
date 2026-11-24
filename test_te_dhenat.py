import tempfile
import unittest
from pathlib import Path
from te_dhenat import lexo_fasta, lexo_csv, lexo_sekuencat


class TestTeDhenat(unittest.TestCase):
    def test_shembujt_e_repos_perputhen(self):
        folder=Path(__file__).resolve().parent/'shembuj'
        csv_records=list(lexo_sekuencat(folder/'sekuenca.csv'))
        fasta_records=list(lexo_sekuencat(folder/'sekuenca.fasta'))
        self.assertEqual(csv_records,fasta_records)
        self.assertEqual([len(r['sekuenca']) for r in csv_records],[4,8,6])
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

    def test_csv_kolonat_dhe_identifikuesit(self):
        p=self.shkruaj('pdb_id,sequence\np1,acde\np2,AAAA\n','.csv')
        self.assertEqual(list(lexo_sekuencat(p)),
                         [{'id':'p1','sekuenca':'ACDE'},{'id':'p2','sekuenca':'AAAA'}])
        p=self.shkruaj('protein\nAAAA\n','.csv')
        self.assertEqual(list(lexo_csv(p,'protein'))[0]['sekuenca'],'AAAA')

    def test_csv_refuzon_gabimet(self):
        for text in ('sequence\n', 'sequence,seq\nAA,AA', 'sequence\nAAXA',
                     'id,sequence\np1', 'sequence,sequence\nAA,AA', 'sequence\nAA,AA'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                list(lexo_csv(self.shkruaj(text,'.csv')))
