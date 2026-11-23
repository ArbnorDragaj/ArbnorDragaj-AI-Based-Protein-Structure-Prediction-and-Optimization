import csv
import tempfile
import unittest
from pathlib import Path
from eksportimi import eksporto_koordinatat
from proteina import beam_search


class TestEksportimi(unittest.TestCase):
    def test_koordinatat_ruhen_pa_ndryshim(self):
        r=beam_search('AAAA',1,200,30)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'struktura.csv'
            eksporto_koordinatat(p,[r])
            with p.open(encoding='utf-8',newline='') as f:
                rows=list(csv.DictReader(f))
            self.assertEqual([tuple(int(row[k]) for k in ('x','y','z')) for row in rows],r.pikat)
            self.assertEqual(''.join(row['aminoacidi'] for row in rows),r.sekuenca)

    def test_struktura_invalide_nuk_mbivendos_skedarin(self):
        r=beam_search('AAAA',1,200,30)
        r.pikat[1]=r.pikat[0]
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'struktura.csv';p.write_text('ekzistues',encoding='utf-8')
            with self.assertRaises(ValueError):
                eksporto_koordinatat(p,[r])
            self.assertEqual(p.read_text(encoding='utf-8'),'ekzistues')
