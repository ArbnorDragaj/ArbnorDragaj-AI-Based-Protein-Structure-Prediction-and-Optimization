"""Mat memorien e secilit algoritëm në proces të veçantë pa ndërfaqe."""
import json
import subprocess
import sys
import tracemalloc
from pathlib import Path
from proteina import simulated_annealing, beam_search

def ekzekuto_procesin(command, ndalo=None):
    if ndalo is not None and ndalo.is_set():
        raise InterruptedError('Matja e memories u ndalua.')
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        try:
            while True:
                try:
                    out, err = process.communicate(timeout=.1 if ndalo is not None else None)
                    break
                except subprocess.TimeoutExpired:
                    if ndalo.is_set():
                        process.terminate()
                        try:
                            process.communicate(timeout=2)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.communicate()
                        raise InterruptedError('Matja e memories u ndalua.')
        except BaseException:
            if process.poll() is None:
                process.kill()
                process.communicate()
            raise
        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode,command,out,err)
        return out


def mat_memorien(emri, sekuenca, pesha, tentativa, sekonda, gjeresia, seed=42, *, ndalo=None):
    if emri not in ('SA', 'Beam'):
        raise ValueError('Algoritmi duhet të jetë SA ose Beam.')
    kerkesa = json.dumps([emri, sekuenca, pesha, tentativa, sekonda, gjeresia, seed])
    try:
        output = ekzekuto_procesin([sys.executable, str(Path(__file__).resolve()), kerkesa],ndalo)
    except subprocess.CalledProcessError as error:
        lines = (error.stderr or '').strip().splitlines()
        detail = lines[-1] if lines else f'Procesi u mbyll me kodin {error.returncode}.'
        raise RuntimeError(f'Matja e memories për {emri} dështoi: {detail}') from error
    try:
        return json.loads(output)
    except json.JSONDecodeError as error:
        raise RuntimeError(f'Matja e memories për {emri} nuk ktheu rezultat të lexueshëm.') from error

if __name__ == '__main__':
    emri, sekuenca, pesha, tentativa, sekonda, gjeresia, seed = json.loads(sys.argv[1])
    tracemalloc.start()
    if emri == 'SA':
        rezultat = simulated_annealing(sekuenca, pesha, tentativa, sekonda, seed)
    else:
        rezultat = beam_search(sekuenca, pesha, tentativa, sekonda, gjeresia)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(json.dumps({'bajte': peak, 'kandidate': rezultat.gjeneruar,
                      'seed': seed if emri == 'SA' else None,
                      'energjia': rezultat.energjia}))
