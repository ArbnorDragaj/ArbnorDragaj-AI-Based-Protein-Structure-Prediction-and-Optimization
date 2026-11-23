"""Kontrolle algoritmike me enumerim ekzakt dhe energji të pavarur."""
import math
import unittest
from proteina import energjia, beam_search, simulated_annealing, valide, ploteso_drejt
from referenca import strukturat_ekzakte, energjia_e_pavarur, analizo_ekzakt
from matja import mat_memorien


class TestSaktesia(unittest.TestCase):
    def test_overflow_dhe_inputet_numerike(self):
        kubi = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,1,1),(1,1,1),(1,0,1),(0,0,1)]
        with self.assertRaises(ValueError):
            energjia('AAAAAAAA', kubi, 1e308)
        for pesha in (True, 0, -1, math.inf, math.nan, 10**1000):
            with self.subTest(pesha=str(pesha)[:20]), self.assertRaises(ValueError):
                energjia('AAAA', kubi[:4], pesha)
        self.assertEqual(energjia(' aaaa ', kubi[:4], 1e308), -1e308)

    def test_numri_i_strukturave(self):
        for n, total in ((1,1),(2,1),(3,5),(4,25),(6,589),(8,13565)):
            self.assertEqual(sum(1 for _ in strukturat_ekzakte(n)), total)

    def test_energjia_kunder_oracle(self):
        for p in strukturat_ekzakte(6):
            self.assertTrue(valide(p,6))
            for s in ('AAAAAA','ADADAA','DDDDDD'):
                self.assertEqual(energjia(s,p), energjia_e_pavarur(s,p))

    def test_beam_pa_heqje_gjen_optimumin(self):
        for s in ('A','AA','AAAA','ADAAAA','AAAAAA'):
            r = beam_search(s,1,100000,30,10000)
            self.assertEqual(r.hequr,0)
            self.assertEqual(r.energjia,analizo_ekzakt(s)['optimumi'])
            self.assertFalse(r.rezerve)

    def test_pruning_global_partition(self):
        s='AAAAAAAA'
        r=beam_search(s,1,100000,30,10,gjurmo_pruning=True)
        ref=analizo_ekzakt(s,r.prefikse_te_hequra)
        self.assertEqual(ref['struktura_valide'],ref['hequr_globale']+r.plota_te_gjeneruara)
        self.assertGreater(ref['hequr_globale'],0)
        self.assertGreaterEqual(r.energjia,ref['optimumi'])

    def test_algoritmet_historia_dhe_buxheti(self):
        for s in ('AAAAAAAA','ADADAAAA','DDDDDDDD'):
            optimumi=analizo_ekzakt(s)['optimumi']
            for kufiri in (1,7,100,500):
                for solver in (simulated_annealing,beam_search):
                    r=solver(s,1,kufiri,30)
                    self.assertTrue(valide(r.pikat,len(s)))
                    self.assertEqual(r.energjia,energjia_e_pavarur(s,r.pikat))
                    self.assertGreaterEqual(r.energjia,optimumi)
                    self.assertLessEqual(r.gjeneruar,kufiri)
                    self.assertEqual(r.gjeneruar,r.valide+r.invalide)
                    self.assertEqual(r.historia[-1],(r.gjeneruar,r.energjia))
                    self.assertTrue(all(a[0]<=b[0] and a[1]>=b[1]
                                        for a,b in zip(r.historia,r.historia[1:])))

    def test_plotesimi_nuk_prish_prefiksin(self):
        for prefiksi in strukturat_ekzakte(4):
            p=ploteso_drejt(list(prefiksi),12)
            if p is not None:
                self.assertEqual(p[:4],list(prefiksi))
                self.assertTrue(valide(p,12))

    def test_matja_e_memories_ruan_seed(self):
        r=simulated_annealing('AAAAAAAA',1,200,30,7)
        memory=mat_memorien('SA','AAAAAAAA',1,200,30,20,7)
        self.assertEqual(memory['seed'],7)
        self.assertEqual(memory['kandidate'],r.gjeneruar)
        self.assertEqual(memory['energjia'],r.energjia)
        self.assertGreater(memory['bajte'],0)

    def test_plotesimet_raportohen_vecmas(self):
        r=beam_search('AAAAAAAA',1,200,30,10)
        self.assertGreater(r.plotesime_te_vleresuara,0)
        self.assertLessEqual(r.gjeneruar,200)
        self.assertEqual(r.gjeneruar,r.valide+r.invalide)

    def test_gabimi_i_procesit_te_memories_shpjegohet(self):
        with self.assertRaisesRegex(RuntimeError,'Pesha'):
            mat_memorien('SA','AAAA',0,100,1,20)


if __name__ == '__main__':
    unittest.main()
