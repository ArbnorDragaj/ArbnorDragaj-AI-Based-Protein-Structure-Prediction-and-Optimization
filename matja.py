"""Mat memorien e secilit algoritëm në proces të veçantë pa ndërfaqe."""
import json
import subprocess
import sys
import tracemalloc
from pathlib import Path
from proteina import simulated_annealing, beam_search

def mat_memorien(emri, sekuenca, pesha, tentativa, sekonda, gjeresia):
    kerkesa = json.dumps([emri, sekuenca, pesha, tentativa, sekonda, gjeresia])
    output = subprocess.run([sys.executable, str(Path(__file__).resolve()), kerkesa],
                            capture_output=True, text=True, check=True)
    return json.loads(output.stdout)

if __name__ == '__main__':
    emri, sekuenca, pesha, tentativa, sekonda, gjeresia = json.loads(sys.argv[1])
    tracemalloc.start()
    if emri == 'SA':
        rezultat = simulated_annealing(sekuenca, pesha, tentativa, sekonda)
    else:
        rezultat = beam_search(sekuenca, pesha, tentativa, sekonda, gjeresia)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(json.dumps({'bajte': peak, 'kandidate': rezultat.gjeneruar}))
