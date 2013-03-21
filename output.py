'''

File: output.py
Author: Hadayat Seddiqi
Date: 3.21.13
Description: Output methods (e.g. fidelity, eigenspectrum, etc.)

'''

import os
import scipy as sp
from scipy import linalg

def ConstructEigData(t, vals, n):
    " Construct proper datapoint for eigenspectrum. "
    datapoint = [t]
    for i in range(0, n): datapoint.append(vals[i].real)

    return datapoint

def RecordEigSpec(eigspec, outdir):
    " Output eigenspectrum to data file. "
    eigpath = os.path.dirname(os.path.realpath(__file__)) + "/" + outdir + "/eigenspectrum.dat"
    sp.savetxt(eigpath, eigspec)

def PlotEigSpec(eigspec, outdir):
    " Plot eigenspectrum. "
    import pylab as pl

    eigpath = os.path.dirname(os.path.realpath(__file__)) + "/" + outdir + "/eigenspectrum.png"

    # Get columns of eigspec to plot
    t = [ row[0] for row in eigspec ]
    for i in range(1,len(eigspec[0])): 
        pl.plot(t, [ row[i] for row in eigspec ])

    pl.xlabel(r'$Time$')
    pl.ylabel(r'$Energy$')
    pl.savefig(eigpath)

def RecordFidelity(Psi, vecs, T, outdir):
    " Output the fidelity for multi-T simulations by calculating \
      the overlap between however many eigenstates we want. "

    data = []

    for i in range(0, len(vecs)):
        overlap = sp.vdot(Psi, vecs[i])
        overlapr = sp.vdot(overlap, overlap).real
        data.append([T, overlapr])

    return data

def PlotFidelity(data, outdir):
    " Plot the fidelity. "
    import pylab as pl

    pl.clf()

    path = os.path.dirname(os.path.realpath(__file__)) + "/" + outdir + "/fidelity.png"

    T = [ row[0] for row in data ]
    for i in range(1, len(data[0])):
        pl.plot(T, [ row[i] for row in data ], marker='o')

    pl.xlabel(r'T (anneal time)')
    pl.ylabel(r'Fidelity $\|\langle \psi \| \phi_0\rangle\|^2$')
    pl.savefig(path)
