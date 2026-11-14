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
    def test_beam_katrori(self):
        self.assertEqual(beam_search('AAAA',1,200,10).energjia,-1)

if __name__ == '__main__': unittest.main()
