import json
import tempfile
import unittest
from pathlib import Path
from dataset import ekzekuto_dataset, sha256
from referenca import energjia_e_pavarur


class TestDataset(unittest.TestCase):
    def test_dataset_ruan_burimin_dhe_strukturat(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary)
            p=folder/'input.fa';p.write_text('>shembull sintetik\nAAAA\n',encoding='utf-8')
            out=folder/'dalja'
            rows=ekzekuto_dataset(p,out,'test sintetik',numri=1,buxheti=100,sekonda=30,seeds=(7,))
            self.assertEqual(len(rows),2)
            metadata=json.loads((out/'burimi.json').read_text(encoding='utf-8'))
            self.assertEqual(metadata['sha256'],sha256(p))
            self.assertEqual(metadata['statusi'],'përfunduar')
            data=json.loads((out/'0001.json').read_text(encoding='utf-8'))
            for r in data['rezultatet']:
                self.assertEqual(r['energjia'],energjia_e_pavarur(r['sekuenca'],r['pikat']))
            with self.assertRaises(FileExistsError):
                ekzekuto_dataset(p,out,'test sintetik',numri=1)
