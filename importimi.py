"""Zgjedhje e një sekuence nga skedar lokal; pa nisur kërkimin automatikisht."""
from itertools import islice
import tkinter as tk
from tkinter import ttk, filedialog
from te_dhenat import lexo_sekuencat


def zgjidh_sekuencen(parent):
    path = filedialog.askopenfilename(parent=parent, title='Importo sekuenca',
        filetypes=[('CSV / FASTA','*.csv *.fa *.fasta *.faa'),('Të gjithë skedarët','*.*')])
    if not path:
        return None
    records = list(islice(lexo_sekuencat(path), 501))
    truncated = len(records) > 500
    records = records[:500]
    window = tk.Toplevel(parent)
    window.title('Zgjidh sekuencën')
    window.transient(parent)
    frame = ttk.Frame(window, padding=15)
    frame.pack(fill='both', expand=True)
    message = 'Shfaqen 500 të parat; dataset-i ka më shumë.' if truncated else f'{len(records)} sekuenca të lexuara.'
    ttk.Label(frame, text=message).pack(anchor='w', pady=5)
    combo = ttk.Combobox(frame, state='readonly', width=65,
        values=[f'{i+1}. {r["id"]} — {len(r["sekuenca"])} aminoacide' for i,r in enumerate(records)])
    combo.pack(fill='x', pady=5)
    combo.current(0)
    result = []
    def prano():
        result.append({**records[combo.current()], 'skedari':path})
        window.destroy()
    ttk.Button(frame, text='Përdor sekuencën', command=prano).pack(side='left', pady=10)
    ttk.Button(frame, text='Anulo', command=window.destroy).pack(side='right', pady=10)
    window.grab_set()
    parent.wait_window(window)
    return result[0] if result else None
