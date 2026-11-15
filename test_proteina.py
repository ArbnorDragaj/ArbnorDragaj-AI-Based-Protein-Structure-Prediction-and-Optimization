import unittest
from proteina import sekuenca_e_sakte, valide, energjia, zinxhiri, rrotullo, simulated_annealing, beam_search

class TestProteina(unittest.TestCase):
    def test_sekuenca(self):
        self.assertEqual(sekuenca_e_sakte(' avh '),'AVH')
        for s in ('','AB','ß'):
            with self.assertRaises(ValueError): sekuenca_e_sakte(s)
    def test_vlefshmeria(self):
        self.assertTrue(valide([(0,0,0),(1,0,0),(1,-1,0)],3))
        self.assertFalse(valide([(0,0,0),(1,0,0),(0,0,0)],3))
        self.assertFalse(valide([(0,0,0),(2,0,0)],2))

    def test_koordinatat_e_pavlefshme(self):
        for pikat, n in (([], 0), ([(0,0,0)], 2),
                         ([(0,0)], 1), ([(0,0,1.0)], 1),
                         ([(0,0,True)], 1), ([[0,0,0]], 1)):
            with self.subTest(pikat=pikat, n=n):
                self.assertFalse(valide(pikat, n))

    def test_energjia_refuzon_strukture_te_pavlefshme(self):
        for pikat in ([(0,0,0)], [(0,0,0),(2,0,0)],
                      [(0,0,0),(0,0,0)]):
            with self.subTest(pikat=pikat):
                with self.assertRaises(ValueError):
                    energjia('AA', pikat)
    def test_energjia(self):
        katror = [(0,0,0),(1,0,0),(1,1,0),(0,1,0)]
        self.assertEqual(energjia('AAAA',katror),-1)
        self.assertEqual(energjia('HHHH',katror),0)
        self.assertEqual(energjia('AAAA',zinxhiri(4)),0)
    def test_rrotullimi(self):
        burimi = zinxhiri(6); kopja = burimi.copy()
        for boshti in range(3):
            for shenja in (-1,1):
                self.assertTrue(valide(rrotullo(burimi,2,boshti,shenja),6))
        self.assertEqual(burimi,kopja)
    def test_algoritmet(self):
        for s in ('A','AA','AAAA','AVILMFWYACDE'):
            for f in (simulated_annealing, beam_search):
                for buxheti in (1,300):
                    r=f(s,1, buxheti, 10)
                    self.assertTrue(valide(r.pikat,len(s)))
                    self.assertEqual(r.energjia,energjia(s,r.pikat,1))
                    self.assertEqual(r.gjeneruar,r.valide+r.invalide)
                    self.assertLessEqual(r.hequr,r.valide)
    def test_seed(self):
        a=simulated_annealing('AVILMFWYACDE',1,500,30,7)
        b=simulated_annealing('AVILMFWYACDE',1,500,30,7)
        self.assertEqual((a.pikat,a.energjia),(b.pikat,b.energjia))

    def test_koha_e_rezultatit_me_te_mire(self):
        for funksioni in (simulated_annealing, beam_search):
            rezultat = funksioni('AVILMFWYACDE', 1, 1000, 10)
            self.assertGreaterEqual(rezultat.koha_me_e_mire, 0)
            self.assertLessEqual(rezultat.koha_me_e_mire, rezultat.koha)
            self.assertLessEqual(rezultat.tentativa_me_e_mire, rezultat.gjeneruar)
    def test_beam_katrori(self):
        self.assertEqual(beam_search('AAAA',1,200,10).energjia,-1)

    def test_algoritmet_pranojne_shkronja_te_vogla(self):
        for funksioni in (simulated_annealing, beam_search):
            rezultat = funksioni(' aaaa ', 1, 200, 10)
            self.assertEqual(rezultat.sekuenca, 'AAAA')
            self.assertEqual(rezultat.energjia, energjia('AAAA', rezultat.pikat))

    def test_parametrat_e_pavlefshem(self):
        for funksioni in (simulated_annealing, beam_search):
            for args in (('', 1, 10, 1), ('AB', 1, 10, 1),
                         ('AAAA', 0, 10, 1), ('AAAA', float('nan'), 10, 1),
                         ('AAAA', 1, 0, 1), ('AAAA', 1, 1.5, 1),
                         ('AAAA', 1, 10, float('inf'))):
                with self.subTest(funksioni=funksioni.__name__, args=args):
                    with self.assertRaises(ValueError):
                        funksioni(*args)
        with self.assertRaises(ValueError):
            beam_search('AAAA', 1, 20, 1, 0)
        with self.assertRaises(ValueError):
            simulated_annealing('AAAA', 1, 20, 1, seed=1.5)

if __name__ == '__main__': unittest.main()
