'''

File: hopfield_gamma_tune.py
Author: Hadayat Seddiqi
Date: 5.20.14
Description: Problem file called by wrapper script. Runs a particular
             Hopfield instance given by properties read from a JSON file
             and a cmdarg for gamma in an attempt to make a successful
             instance from a failed one by tuning gamma (the bias term).

'''

import os
import scipy as sp
import itertools
import random
import collections
import json

def parameters(cmdargs):
    """
    """

    # The Hopfield parameters
    properties = json.load(open('data/hopfield_gamma_tune/gamma_problem_inputs.json'))
    hparams = {
        'numNeurons': properties['nQubits'],
        'inputState': properties['inputState'],
        'learningRule': properties['learningRule'],
        'numMemories': len(properties['memories'])
        }

    # Construct memories
    memories = properties['memories']

    # Basic simulation params
    nQubits = hparams['numNeurons']
    T = properties['annealTime']
    dt = 0.01*T

    # Output parameters
    binary = 1 # Save output files as binary Numpy format
    progressout = 0 # Output simulation progress over anneal timesteps

    eigspecdat = 0 # Output data for eigspec
    eigspecplot = 0 # Plot eigspec
    eigspecnum = 2**nQubits # Number of eigenvalues to output
    fidelplot = 0 # Plot fidelity
    fideldat = 0 # Output fidelity data
    fidelnumstates = 2**nQubits # Check fidelity with this number of eigenstates
    overlapdat = 0 # Output overlap data
    overlapplot = 0 # Plot overlap

    # Output directory stuff
    # probdir = 'data/hopfield_gamma_tune/n'+str(nQubits)+'p'+\
    #     str(hparams['numMemories'])+hparams['learningRule']
    # if isinstance(T, collections.Iterable):
    #     probdir += 'MultiT'
    # if os.path.isdir(probdir):
    #     outlist = sorted([ int(name) for name in os.listdir(probdir) 
    #                        if name.isdigit() ])
    # else:
    #     outlist = []
    # outnum = outlist[-1] + 1 if outlist else 0
    # outputdir = probdir + '/' + str(outnum) + '/'
    outputdir = 'data/hopfield_gamma_tune'

    probshow = 0 # Print final state probabilities to screen
    probout = 1 # Output probabilities to file
    mingap = 0 # Record the minimum spectral gap

    errchk = 0 # Error-checking on/off (for simulation accuracy)
    eps = 0.01 # Numerical error in normalization condition (1 - norm < eps)

    # Specify a QUBO (convert to Ising = True), or alpha, beta directly 
    # (convert = False), and also specify the signs on the Ising Hamiltonian 
    # terms (you can specify coefficients too for some problems if needed)
    isingConvert = 0
    isingSigns = {'hx': -1, 'hz': -1, 'hzz': -1}

    # Construct network Ising parameters
    neurons = nQubits

    # This is gamma, the appropriate weighting on the input vector
    isingSigns['hz'] *= float(cmdargs['farg'])

    alpha = sp.array(hparams['inputState'])
    beta = sp.zeros((neurons,neurons))
    delta = sp.array([])

    # Construct the memory matrix according to a learning rule
    if hparams['learningRule'] == 'hebb':
        # Construct pattern matrix according to Hebb's rule
        for i in range(neurons):
            for j in range(neurons):
                for p in range(len(memories)):
                    beta[i,j] += ( memories[p][i]*memories[p][j] -
                                   len(memories)*(i == j) )
        beta = sp.triu(beta)/float(neurons)
    elif hparams['learningRule'] == 'stork':
        # Construct the memory matrix according to the Storkey learning rule
        memMat = sp.zeros((neurons,neurons))
        for m, mem in enumerate(memories):
            for i in range(neurons):
                for j in range(neurons):
                    hij = sp.sum([ memMat[i,k]*mem[k] for k in range(neurons) ])
                    hji = sp.sum([ memMat[j,k]*mem[k] for k in range(neurons) ])
                    # Don't forget to make the normalization a float!
                    memMat[i,j] += 1./neurons*(mem[i]*mem[j] - mem[i]*hji - 
                                               hij*mem[j])
        beta = sp.triu(memMat)
    elif hparams['learningRule'] == 'proj':
        # Construct memory matrix according to the Moore-Penrose pseudoinverse rule
        memMat = sp.matrix(memories).T
        beta = sp.triu(memMat * sp.linalg.pinv(memMat))

    # Some outputs
    outputs = {
        'nQubits': nQubits,
        'learningRule': hparams['learningRule'],
        'inputState': hparams['inputState'],
        'memories': memories,
        'answer': memories[0],
        'annealTime': list(T) if isinstance(T, collections.Iterable) else T
               }

    ############################################################################
    ######## All variables must be specified here, do NOT change the keys ######
    ############################################################################

    return {
        'nQubits': nQubits,
        'Q': None,
        'T': T,
        'dt': dt,
        'outputdir': outputdir,
        'errchk': errchk,
        'eps': eps,
        'isingConvert': isingConvert,
        'isingSigns': isingSigns,
        'outputs': outputs,
        'alpha': alpha,
        'beta': beta,
        'delta': delta,
        'eigdat': eigspecdat,
        'eigplot': eigspecplot,
        'eignum': eigspecnum,
        'fiddat': fideldat,
        'fidplot': fidelplot,
        'fidnumstates': fidelnumstates,
        'overlapdat': overlapdat,
        'overlapplot': overlapplot,
        'outdir': outputdir,
        'binary': binary,
        'progressout': progressout,
        'probshow': probshow,
        'probout': probout,
        'mingap': mingap,
        'stateoverlap': None,
        'hzscale': None,
        'hzzscale': None,
        'hxscale': None
        }
