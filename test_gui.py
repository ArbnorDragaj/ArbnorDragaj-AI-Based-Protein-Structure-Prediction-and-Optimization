"""Kontrolle integrimi për importin, eksportin dhe parametrat e rezultateve."""
import json
import tempfile
import time
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch
from main import Aplikacioni
from grafiket import hap_konvergjencen


class TestGui(unittest.TestCase):
    def setUp(self):
        try:
            self.root=tk.Tk()
        except tk.TclError as error:
            self.skipTest(f'GUI kërkon ekran: {error}')
        self.root.withdraw()
        self.app=Aplikacioni(self.root)

    def tearDown(self):
        if hasattr(self,'root'):
            self.root.after_cancel(self.app.poll_id)
            self.root.update_idletasks()
            self.root.destroy()

    def test_importi_dhe_ndryshimi_manual_i_burimit(self):
        record={'id':'shembull','sekuenca':'AAAA','skedari':'input.fa'}
        with patch('main.zgjidh_sekuencen',return_value=record):
            self.app.importo()
        self.assertEqual(self.app.fushat['gjatesia'].get(),'4')
        self.assertEqual(self.app.burimi,record)
        self.app.fushat['sekuenca'].set('AAAD')
        self.assertIsNone(self.app.burimi)

    def test_importi_i_pavlefshem_ruan_sekuencen(self):
        original=self.app.fushat['sekuenca'].get()
        with patch('main.zgjidh_sekuencen',side_effect=ValueError('prove')), patch('main.messagebox.showerror') as error:
            self.app.importo()
            error.assert_called_once()
        self.assertEqual(self.app.fushat['sekuenca'].get(),original)

    def test_eksporti_perdor_parametrat_e_ekzekutimit(self):
        self.app.fushat['sekuenca'].set('AAAA')
        self.app.fushat['tentativa'].set('100')
        with patch('main.messagebox.showerror') as error:
            self.app.nis()
            self.app.fushat['pesha'].set('2')
            deadline=time.monotonic()+15
            while not self.app.rezultatet and time.monotonic()<deadline:
                self.root.update();time.sleep(.01)
            error.assert_not_called()
        self.assertEqual(len(self.app.rezultatet),2)
        with tempfile.TemporaryDirectory() as temporary:
            p=Path(temporary)/'rezultatet.json'
            with patch('main.filedialog.asksaveasfilename',return_value=str(p)):
                self.app.eksporto()
            data=json.loads(p.read_text(encoding='utf-8'))
            self.assertEqual(data['parametrat']['pesha'],1)
            self.assertEqual(data['rezultatet'][0]['sekuenca'],'AAAA')
        window=hap_konvergjencen(self.root,self.app.rezultatet)
        self.root.update()
        self.assertTrue(window.winfo_exists())
        window.destroy()
