"""Shfaq grafikët e ruajtur të eksperimenteve brenda aplikacionit."""
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.image import imread


GRAFIKET = {
    'Energjia': 'energjia.png',
    'Koha': 'koha_s.png',
    'Memoria Python': 'memoria_kib.png',
    'Kandidatët': 'kandidate.png',
    'Konvergjenca': 'konvergjenca.png',
}

SHPJEGIMET = {
    'Energjia': 'Energjia sipas gjatësisë së sekuencës. Vlera më e ulët është më e mirë në modelin HP.',
    'Koha': 'Koha e ekzekutimit në sekonda sipas gjatësisë së sekuencës.',
    'Memoria Python': 'Kulmi i alokimeve Python, matur veçmas me tracemalloc; jo RAM-i i gjithë procesit.',
    'Kandidatët': 'Numri i kandidatëve të gjeneruar; përfshin kandidatët validë dhe invalidë.',
    'Konvergjenca': 'Energjia më e mirë kundrejt kandidatëve, për sekuencën e përzier me gjatësi 18.',
}


def hap_grafiket(parent):
    folder = Path(__file__).resolve().parent / 'rezultate'
    te_pranishem = {emri: folder / skedari for emri, skedari in GRAFIKET.items()
                   if (folder / skedari).is_file()}
    if not te_pranishem:
        messagebox.showinfo('Grafikët mungojnë',
                            'Ekzekuto eksperimente.py për të krijuar grafikët.', parent=parent)
        return

    dritarja = tk.Toplevel(parent)
    dritarja.title('Grafikët e eksperimenteve')
    dritarja.geometry('1100x650')
    dritarja.minsize(650, 400)
    paneli = ttk.Frame(dritarja, padding=10)
    paneli.pack(fill='x')
    ttk.Label(paneli, text='Zgjidh grafikun:').pack(side='left', padx=(0, 10))
    zgjedhja = tk.StringVar(dritarja, value=next(iter(te_pranishem)))
    lista = ttk.Combobox(paneli, textvariable=zgjedhja,
                         values=list(te_pranishem), state='readonly')
    lista.pack(side='left')
    ttk.Label(dritarja, text='Rezultatet e eksperimenteve të ruajtura; jo të simulimit aktual.',
              padding=(10, 0, 10, 5)).pack(anchor='w')
    shpjegimi = tk.StringVar(dritarja)
    ttk.Label(dritarja, textvariable=shpjegimi, wraplength=620,
              padding=(10, 0, 10, 5)).pack(anchor='w')
    figura = Figure(figsize=(10, 5), dpi=100)
    boshti = figura.add_subplot(111)
    figura.subplots_adjust(left=0, right=1, bottom=0, top=1)
    canvas = FigureCanvasTkAgg(figura, master=dritarja)
    NavigationToolbar2Tk(canvas, dritarja).update()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    def shfaq(event=None):
        shpjegimi.set(SHPJEGIMET[zgjedhja.get()])
        try:
            imazhi = imread(te_pranishem[zgjedhja.get()])
        except (OSError, ValueError, SyntaxError) as gabim:
            boshti.clear()
            boshti.set_axis_off()
            boshti.text(0.5, 0.5, 'Grafiku i zgjedhur nuk mund të lexohet.',
                        ha='center', va='center', transform=boshti.transAxes)
            canvas.draw_idle()
            messagebox.showerror('Grafiku nuk hapet', str(gabim), parent=dritarja)
            return
        boshti.clear()
        boshti.imshow(imazhi)
        boshti.set_axis_off()
        canvas.draw_idle()

    lista.bind('<<ComboboxSelected>>', shfaq)
    shfaq()
    return dritarja
