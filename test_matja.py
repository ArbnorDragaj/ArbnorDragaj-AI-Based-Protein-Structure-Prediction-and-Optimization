import threading
import unittest
from matja import mat_memorien


class TestMatja(unittest.TestCase):
    def test_matja_nuk_nis_pas_ndalimit(self):
        event=threading.Event();event.set()
        with self.assertRaises(InterruptedError):
            mat_memorien('SA','AAAA',1,100,30,20,ndalo=event)

    def test_ndalimi_mbyll_procesin_e_matjes(self):
        event=threading.Event()
        timer=threading.Timer(.2,event.set)
        timer.start()
        try:
            with self.assertRaises(InterruptedError):
                mat_memorien('SA','A'*100,1,10000000,30,20,ndalo=event)
        finally:
            timer.cancel();timer.join()
