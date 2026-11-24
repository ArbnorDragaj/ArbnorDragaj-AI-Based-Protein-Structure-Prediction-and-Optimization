import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from krahaso import krahaso
from referenca import energjia_e_pavarur


class TestCli(unittest.TestCase):
    def test_cli_ruan_rezultatin_pa_gui(self):
        script=Path(__file__).with_name('krahaso.py')
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary)/'dalja'
            run=subprocess.run([sys.executable,'-B',str(script),'AAAA','--dalja',str(folder),
                                '--buxheti','100','--pa-memorie'],capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stderr)
            data=json.loads((folder/'rezultatet.json').read_text(encoding='utf-8'))
            self.assertEqual(data['memoria_python'],[None,None])
            for r in data['rezultatet']:
                self.assertEqual(r['energjia'],energjia_e_pavarur(r['sekuenca'],r['pikat']))
            self.assertTrue((folder/'koordinatat.csv').exists())
            with self.assertRaises(FileExistsError):
                krahaso('AAAA',folder)

    def test_cli_nuk_importon_biblioteka_grafike(self):
        run=subprocess.run([sys.executable,'-B','-c',
            "import krahaso,sys; assert 'tkinter' not in sys.modules and 'matplotlib' not in sys.modules"],
            cwd=Path(__file__).resolve().parent,capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
