"""Dritare e thjeshtë për krahasimin dhe shikimin e proteinës 3D."""
import math
import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from proteina import HIDROFOBIKE, sekuenca_e_sakte, simulated_annealing, beam_search, valide, kontaktet
from matja import mat_memorien
from grafiket import hap_grafiket, hap_konvergjencen
from importimi import zgjidh_sekuencen
from eksportimi import eksporto_koordinatat, eksporto_json

class Aplikacioni:
    def __init__(self, root):
        self.root = root
        root.title('Optimizimi i proteinës 3D')
        root.geometry('1250x780')
        root.minsize(850, 600)
        root.configure(background='#eef3f6')
        stili = ttk.Style(root)
        stili.theme_use('clam')
        stili.configure('Anash.TFrame', background='#132d3a')
        stili.configure('Anash.TLabel', background='#132d3a', foreground='#d8e7e9', font=('Segoe UI', 9))
        stili.configure('Titull.TLabel', background='#132d3a', foreground='white', font=('Segoe UI', 18, 'bold'))
        stili.configure('NenTitull.TLabel', background='#132d3a', foreground='#91b3bb', font=('Segoe UI', 9))
        stili.configure('Gjendje.TLabel', background='#132d3a', foreground='#8ee0ca', font=('Segoe UI', 9))
        stili.configure('Kryesor.TButton', background='#0d887c', foreground='white', font=('Segoe UI', 10, 'bold'), padding=9, borderwidth=0)
        stili.map('Kryesor.TButton', background=[('active', '#0b7067'), ('disabled', '#647b80')], foreground=[('disabled', '#d7e1e1')])
        stili.configure('TButton', font=('Segoe UI', 9), padding=6)
        stili.configure('TEntry', padding=5, fieldbackground='white')
        stili.configure('TCombobox', padding=4, fieldbackground='white')
        stili.configure('Pune.TFrame', background='#eef3f6')
        stili.configure('Pune.TLabel', background='#eef3f6', foreground='#193744', font=('Segoe UI', 10))
        stili.configure('Nendarje.TLabel', background='#eef3f6', foreground='#193744', font=('Segoe UI', 11, 'bold'))
        self.radha = queue.Queue()
        self.rezultatet = []
        self.burimi = None
        self.konfigurimi = None
        self.memoriet = None
        self.sinjali_ndalimit = threading.Event()
        self.worker = None
        self.ne_pune = False
        self.mbyllje = False
        root.protocol('WM_DELETE_WINDOW',self.mbyll)
        self.zoom = 1.0
        self.fushat = {}
        anash = ttk.Frame(root)
        anash.pack(side='left', fill='y')
        paneli = tk.Canvas(anash, width=275, background='#132d3a', highlightthickness=0)
        levizja = ttk.Scrollbar(anash, orient='vertical', command=paneli.yview)
        levizja.pack(side='right', fill='y')
        paneli.pack(side='left', fill='y')
        paneli.configure(yscrollcommand=levizja.set)
        majtas = ttk.Frame(paneli, padding=(20, 18), style='Anash.TFrame')
        paneli.create_window((0, 0), window=majtas, anchor='nw')
        majtas.bind('<Configure>', lambda event: paneli.configure(scrollregion=paneli.bbox('all')))
        djathtas = ttk.Frame(root, padding=(18, 14), style='Pune.TFrame')
        djathtas.pack(side='left', fill='both', expand=True)
        ttk.Label(majtas, text='Proteina 3D', style='Titull.TLabel').pack(anchor='w')
        ttk.Label(majtas, text='Optimizim dhe krahasim', style='NenTitull.TLabel').pack(anchor='w', pady=(1, 15))
        for key, label, value in [('sekuenca','Sekuenca','AVILMFWYACDE'), ('gjatesia','Gjatësia','12'),
                                   ('pesha','Pesha e kontakteve H–H','1'), ('koha','Koha për algoritëm (s)','2'),
                                   ('tentativa','Tentativat maksimale','3000'), ('beam','Gjerësia Beam','30')]:
            ttk.Label(majtas, text=label, style='Anash.TLabel').pack(anchor='w')
            var = tk.StringVar(value=value)
            ttk.Entry(majtas, textvariable=var, width=27,
                      state='readonly' if key == 'gjatesia' else 'normal').pack(fill='x', pady=(3,8), ipady=1)
            self.fushat[key] = var
        self.fushat['sekuenca'].trace_add('write', self.ndrysho_sekuencen)
        self.importo_buton = ttk.Button(majtas, text='Importo CSV / FASTA', command=self.importo)
        self.importo_buton.pack(fill='x', pady=4)
        self.eksporto_buton = ttk.Button(majtas, text='Eksporto rezultatet', command=self.eksporto, state='disabled')
        self.eksporto_buton.pack(fill='x', pady=4)
        self.buton = ttk.Button(majtas, text='Ekzekuto dhe krahaso', command=self.nis, style='Kryesor.TButton')
        self.buton.pack(fill='x', pady=(8, 6))
        self.ndalo_buton = ttk.Button(majtas,text='Ndalo',command=self.ndalo,state='disabled')
        self.ndalo_buton.pack(fill='x',pady=(0,5))
        self.zgjedhja = tk.StringVar(value='Simulated Annealing')
        ttk.Label(majtas, text='Shfaq strukturën', style='Anash.TLabel').pack(anchor='w', pady=(10,4))
        lista = ttk.Combobox(majtas, textvariable=self.zgjedhja, state='readonly',
                             values=('Simulated Annealing','Beam Search'))
        lista.pack(fill='x')
        lista.bind('<<ComboboxSelected>>', lambda _: self.vizato())
        ttk.Button(majtas, text='Rivendos pamjen', command=lambda: self.vizato(True)).pack(fill='x', pady=8)
        ttk.Button(majtas, text='Grafikët e eksperimenteve',
                   command=lambda: hap_grafiket(self.root)).pack(fill='x', pady=(0, 5))
        self.historia_buton = ttk.Button(majtas, text='Konvergjenca e rezultatit', state='disabled',
                                        command=lambda: hap_konvergjencen(self.root,self.rezultatet))
        self.historia_buton.pack(fill='x',pady=(0,5))
        ttk.Label(majtas, text='Mausi: rrotullo  ·  Rrota: zoom\nPortokalli: H  ·  Blu: P', style='NenTitull.TLabel', justify='left').pack(anchor='w', pady=5)
        self.statusi = tk.StringVar(value='Shkruaj sekuencën dhe shtyp Ekzekuto.')
        ttk.Label(majtas, textvariable=self.statusi, style='Gjendje.TLabel', wraplength=220).pack(anchor='w', pady=10)
        kontrollet = ttk.Frame(djathtas, style='Pune.TFrame')
        kontrollet.pack(fill='x', pady=(0, 5))
        ttk.Label(kontrollet, text='Pamja e strukturës', style='Nendarje.TLabel').pack(side='left')
        self.figura = Figure(figsize=(7,5), dpi=100, facecolor='#f8fbfc')
        self.boshti = self.figura.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.figura, master=djathtas)
        self.canvas.mpl_connect('scroll_event', self.zoom_me_maus)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        ttk.Label(djathtas, text='Rezultatet e krahasimit', style='Nendarje.TLabel').pack(anchor='w', pady=(10, 5))
        rezultatet_panel = ttk.Frame(djathtas)
        rezultatet_panel.pack(fill='x')
        self.teksti = tk.Text(rezultatet_panel, height=8, wrap='word', font=('Consolas', 10),
                              background='white', foreground='#193744', relief='flat',
                              padx=10, pady=9, highlightthickness=1, highlightbackground='#dce6e9',state='disabled')
        scroll_rezultatet = ttk.Scrollbar(rezultatet_panel,orient='vertical',command=self.teksti.yview)
        scroll_rezultatet.pack(side='right',fill='y')
        self.teksti.configure(yscrollcommand=scroll_rezultatet.set)
        self.teksti.pack(side='left',fill='both',expand=True)
        self.vizato(True)
        self.poll_id = root.after(100, self.kontrollo)

    def ndrysho_sekuencen(self, *_):
        self.burimi = None
        self.fushat['gjatesia'].set(str(len(self.fushat['sekuenca'].get().strip())))

    def importo(self):
        try:
            record = zgjidh_sekuencen(self.root)
        except (OSError, ValueError, UnicodeError) as error:
            messagebox.showerror('Importimi dështoi', str(error), parent=self.root)
            return
        if record:
            self.fushat['sekuenca'].set(record['sekuenca'])
            self.burimi = record
            self.statusi.set(f'Importuar: {record["id"]}. Shtyp Ekzekuto.')

    def eksporto(self):
        if not self.rezultatet or self.konfigurimi is None:
            return
        path = filedialog.asksaveasfilename(parent=self.root, title='Eksporto rezultatet',
            defaultextension='.json', filetypes=[('Rezultatet dhe parametrat','*.json'),('Koordinatat','*.csv')])
        if not path:
            return
        try:
            if Path(path).suffix.lower() == '.csv':
                eksporto_koordinatat(path,self.rezultatet)
            elif Path(path).suffix.lower() == '.json':
                eksporto_json(path,self.rezultatet,self.konfigurimi,self.memoriet)
            else:
                raise ValueError('Përdor prapashtesën .json ose .csv.')
        except (OSError, ValueError) as error:
            messagebox.showerror('Eksportimi dështoi',str(error),parent=self.root)
        else:
            self.statusi.set('Rezultatet u eksportuan.')

    def nis(self):
        if self.ne_pune or self.mbyllje:
            return
        try:
            s = sekuenca_e_sakte(self.fushat['sekuenca'].get())
            n, tentativa, beam = (int(self.fushat[k].get()) for k in ('gjatesia','tentativa','beam'))
            pesha, koha = (float(self.fushat[k].get()) for k in ('pesha','koha'))
            if n != len(s): raise ValueError('Gjatësia nuk përputhet me sekuencën.')
            if tentativa <= 0 or beam <= 0 or not math.isfinite(koha) or koha <= 0 or not math.isfinite(pesha) or pesha <= 0:
                raise ValueError('Vlerat duhet të jenë numra pozitivë dhe të fundëm.')
        except ValueError as error:
            messagebox.showerror('Input i pavlefshëm', str(error), parent=self.root)
            return
        if self.fushat['sekuenca'].get() != s:
            self.fushat['sekuenca'].set(s)
        self.config_ne_pune = {'pesha':pesha,'koha_s':koha,'buxheti':tentativa,
                              'beam_width':beam,'seed_sa':42,'burimi':self.burimi}
        self.sinjali_ndalimit.clear()
        self.ne_pune = True
        self.ndalo_buton.config(state='normal')
        self.eksporto_buton.config(state='disabled')
        self.importo_buton.config(state='disabled')
        self.buton.config(state='disabled')
        self.statusi.set('Duke llogaritur të dy algoritmet…')
        def puno():
            try:
                sa = simulated_annealing(s, pesha, tentativa, koha,ndalo=self.sinjali_ndalimit)
                bs = beam_search(s, pesha, tentativa, koha, beam,ndalo=self.sinjali_ndalimit)
                memoriet = []
                for k in ('SA','Beam'):
                    try:
                        m=mat_memorien(k,s,pesha,tentativa,koha,beam,ndalo=self.sinjali_ndalimit)
                    except InterruptedError:
                        m=None
                    memoriet.append(m)
                self.radha.put((None, [sa,bs], memoriet))
            except Exception as error:
                self.radha.put((str(error), None, None))
        self.worker = threading.Thread(target=puno,daemon=True)
        self.worker.start()

    def ndalo(self):
        self.sinjali_ndalimit.set()
        self.ndalo_buton.config(state='disabled')
        if self.ne_pune:
            self.statusi.set('Duke ndaluar; ruhet rezultati më i mirë i gjetur.')

    def mbyll(self):
        self.mbyllje = True
        self.ndalo()
        self._mbyll_kur_gati()

    def _mbyll_kur_gati(self):
        if self.worker is not None and self.worker.is_alive():
            self.root.after(50,self._mbyll_kur_gati)
            return
        self.root.after_cancel(self.poll_id)
        self.root.destroy()

    def kontrollo(self):
        try:
            gabim, rezultatet, memoriet = self.radha.get_nowait()
            self.ne_pune = False
            self.ndalo_buton.config(state='disabled')
            self.buton.config(state='normal')
            self.importo_buton.config(state='normal')
            if gabim:
                self.eksporto_buton.config(state='normal' if self.rezultatet else 'disabled')
                self.statusi.set('Gabim gjatë ekzekutimit.')
                if not self.mbyllje:
                    messagebox.showerror('Gabim', gabim, parent=self.root)
            else:
                self.rezultatet = rezultatet
                self.konfigurimi = {**self.config_ne_pune,'ndaluar':self.sinjali_ndalimit.is_set()}
                self.memoriet = memoriet
                self.eksporto_buton.config(state='normal')
                self.historia_buton.config(state='normal')
                self.statusi.set('U ndalua. Rezultatet janë të pjesshme.' if self.sinjali_ndalimit.is_set()
                                else 'Përfundoi. Zgjidh algoritmin për të parë strukturën.')
                self.teksti.config(state='normal')
                self.teksti.delete('1.0', 'end')
                for r,m in zip(rezultatet, memoriet):
                    perqindja = 100*r.hequr/r.valide if r.valide else 0
                    memoria = f'{m["bajte"]/1024:.1f} KiB' if m is not None else 'e pamatur (ndalim)'
                    kandidatet_memories = m['kandidate'] if m is not None else 'të pamatur'
                    self.teksti.insert('end', f'{r.algoritmi}: E={r.energjia:g} | koha={r.koha:.4f}s | memoria={memoria}\n')
                    self.teksti.insert('end', f'  Kontakte H–H jo radhazi: {kontaktet(r.sekuenca, r.pikat)}\n')
                    self.teksti.insert('end', f'  Vlerësime plotësimi: {r.plotesime_te_vleresuara}; kandidatë + plotësime: {r.gjeneruar+r.plotesime_te_vleresuara}\n')
                    self.teksti.insert('end', f'  Kandidatë: {r.gjeneruar}; validë: {r.valide}; invalidë: {r.invalide}; hequr nga Beam: {r.hequr} ({perqindja:.1f}% e validëve)\n')
                    self.teksti.insert('end', f'  E vlefshme: {"Po" if valide(r.pikat,len(r.sekuenca)) else "Jo"}; tentativa më e mirë: {r.tentativa_me_e_mire}; plotësim rezervë: {"Po" if r.rezerve else "Jo"}; matja e memories: {kandidatet_memories} kandidatë.\n')
                    self.teksti.insert('end', f'  Koha e rezultatit më të mirë: {r.koha_me_e_mire:.4f} s; ndalimi: {r.arsyeja}\n')
                self.teksti.insert('end', 'Memoria matet veçmas me tracemalloc; numri i kandidatëve mund të ndryshojë nga kufiri kohor.\n')
                self.teksti.config(state='disabled')
                self.vizato(True)
        except queue.Empty:
            pass
        self.poll_id = self.root.after(100, self.kontrollo)

    def zmadho(self, faktori):
        self.zoom = min(1.8, max(0.6, self.zoom * faktori))
        self.boshti.set_box_aspect((1, 1, 1), zoom=self.zoom)
        self.canvas.draw_idle()

    def zoom_me_maus(self, event):
        if event.inaxes is self.boshti and event.step:
            self.zmadho(1.15 if event.step > 0 else 1/1.15)

    def vizato(self, rivendos=False):
        from proteina import zinxhiri
        if self.rezultatet:
            r = next(x for x in self.rezultatet if x.algoritmi == self.zgjedhja.get())
            s, pikat, titulli = r.sekuenca, r.pikat, f'{r.algoritmi} — Energjia {r.energjia:g}'
        else:
            s = 'AVILMFWYACDE'
            pikat, titulli = zinxhiri(len(s)), 'Struktura fillestare'
        a = self.boshti
        if rivendos:
            self.zoom = 1.0
        elev, azim = (25, -60) if rivendos else (a.elev, a.azim)
        a.clear()
        x,y,z = zip(*pikat)
        a.set_facecolor('#f8fbfc')
        a.set_axis_on()
        for bosht in (a.xaxis, a.yaxis, a.zaxis):
            bosht.set_pane_color((0.95, 0.98, 0.98, 0.30))
        a.tick_params(colors='#667d86', labelsize=8, pad=1)
        # Lidhjet ndjekin saktësisht rendin e pikave në rrjetë.
        a.plot(x, y, z, color='#617d86', linewidth=2.6, alpha=0.85)
        a.scatter(x, y, z, c=['#eea13a' if aa in HIDROFOBIKE else '#398ac3' for aa in s],
                  s=125, edgecolors='white', linewidths=1.3, depthshade=False)
        a.scatter(*pikat[0], marker='s', s=210, facecolors='none', edgecolors='#15816d', linewidths=1.8)
        a.scatter(*pikat[-1], marker='D', s=210, facecolors='none', edgecolors='#8558a2', linewidths=1.8)
        for i,(xx,yy,zz) in enumerate(pikat):
            if len(pikat) <= 25: a.text(xx, yy, zz + 0.12, str(i+1), fontsize=8, color='#294550')
        mijesi = [(min(v)+max(v))/2 for v in (x,y,z)]
        rrezja = max(1, max(max(v)-min(v) for v in (x,y,z))/2+1)
        a.set_xlim(mijesi[0]-rrezja,mijesi[0]+rrezja)
        a.set_ylim(mijesi[1]-rrezja,mijesi[1]+rrezja)
        a.set_zlim(mijesi[2]-rrezja,mijesi[2]+rrezja)
        a.set_box_aspect((1,1,1), zoom=self.zoom)
        a.view_init(elev=elev, azim=azim)
        a.set(xlabel='X', ylabel='Y', zlabel='Z')
        a.set_title(titulli, color='#193744', fontsize=13, fontweight='bold', pad=12)
        legenda = [
            Line2D([0], [0], marker='o', color='none', markerfacecolor='#eea13a', markeredgecolor='white', markersize=9, label='Hidrofob (H)'),
            Line2D([0], [0], marker='o', color='none', markerfacecolor='#398ac3', markeredgecolor='white', markersize=9, label='Polar (P)'),
            Line2D([0], [0], marker='s', color='#15816d', markerfacecolor='none', linestyle='none', markersize=8, label='Fillimi'),
            Line2D([0], [0], marker='D', color='#8558a2', markerfacecolor='none', linestyle='none', markersize=8, label='Fundi'),
        ]
        a.legend(handles=legenda, loc='upper left', frameon=False, fontsize=9)
        self.canvas.draw_idle()

if __name__ == '__main__':
    root = tk.Tk()
    Aplikacioni(root)
    root.mainloop()
