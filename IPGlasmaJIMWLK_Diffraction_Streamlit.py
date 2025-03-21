import pickle

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from os import path
import subprocess


def parse_model_parameter_file(parfile):
    pardict = {}
    f = open(parfile, 'r')
    for line in f:
        par = line.split("#")[0]
        if par != "":
            par = par.split(":")[1].split(",")
            key = par[0].strip()
            val = [float(ival.strip()) for ival in par[1:]]
            pardict.update({key: val})
    return pardict


@st.cache_resource
def loadEmulators():
    result = subprocess.run(['./downloadEmulators.sh'])
    emulatorList = [
        "emulator_PCGP_set1_closure.pkl",
        "emulator_PCGP_set2_closure.pkl",
        "emulator_PCGP_set3_closure.pkl",
        "emulator_PCGP_set4_closure.pkl",
    ]
    emus = []
    for emu_i in emulatorList:
        with open(path.join("emulators", emu_i), 'rb') as f:
            emus.append(pickle.load(f))
    return emus

def main():
    emuList = loadEmulators()

    with open("exp_data_JIMWLK.pkl", 'rb') as f:
        expData = pickle.load(f)['000']['obs']

    # Define model parameters in the sidebar
    modelParamFile = "IP_DIFF_JIMWLK_prior_range"
    paraDict = parse_model_parameter_file(modelParamFile)
    st.sidebar.header('Model Parameters:')
    params = []     # record the model parameter values
    Kfactors = np.array([1., 1., 1., 1.])
    for ikey in paraDict.keys():
        parMin = paraDict[ikey][0]
        parMax = paraDict[ikey][1]
        parInit = (parMax + parMin) / 2
        parVal = st.sidebar.slider(label=ikey,
                                   min_value=parMin, max_value=parMax,
                                   value=parInit,
                                   step=(parMax - parMin)/1000.,
                                   format='%f')
        if ikey not in ['KP', 'KPb']:
            params.append(parVal)
        elif ikey == 'KP':
            Kfactors[2:] = parVal
        elif ikey == 'KPb':
            Kfactors[:2] = parVal
    params = np.array([params,])

    pred = np.array([])
    predErr = np.array([])
    for i, emu_i in enumerate(emuList):
        modelPred, modelPredCov = emu_i.predict(params, return_cov=True)
        if i == 0:
            predLoc = modelPred[0, :]*Kfactors[i]   
            predErrLoc = (np.sqrt(np.diagonal(modelPredCov[0, :, :]))
                          *Kfactors[i])
            pred = np.concatenate((pred, predLoc))
            predErr = np.concatenate((predErr, predErrLoc))
        else:
            predLoc = np.exp(modelPred[0, :])*Kfactors[i]
            predErrLoc = (np.sqrt(np.diagonal(modelPredCov[0, :, :]))
                          *np.exp(modelPred[0, :])*Kfactors[i])
            pred = np.concatenate((pred, predLoc))
            predErr = np.concatenate((predErr, predErrLoc))

    idx0 = 0
    idx = idx0 + 13
    x = range(idx0, idx)
    fig, ax = plt.subplots(nrows=2, ncols=2)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9,
                        wspace=0.2, hspace=0.35)
    ax[0, 0].errorbar(x, expData[0, idx0:idx],
                      yerr=expData[1, idx0:idx], fmt="ob")
    ax[0, 0].errorbar(x, pred[idx0:idx], yerr=predErr[idx0:idx], fmt="or")

    idx0 = idx
    idx = idx0 + 11
    x = range(idx0, idx)
    ax[0, 1].errorbar(x, np.exp(expData[0, idx0:idx]),
                 yerr=np.exp(expData[0, idx0:idx])*expData[1, idx0:idx],
                 fmt="ob")
    ax[0, 1].errorbar(x, pred[idx0:idx], yerr=predErr[idx0:idx], fmt="or")

    idx0 = idx
    idx = idx0 + 45
    x = range(idx0, idx)
    ax[1, 0].errorbar(x, np.exp(expData[0, idx0:idx]),
                 yerr=np.exp(expData[0, idx0:idx])*expData[1, idx0:idx],
                 fmt="ob")
    ax[1, 0].errorbar(x, pred[idx0:idx], yerr=predErr[idx0:idx], fmt="or")


    idx0 = idx
    idx = idx0 + 17
    x = range(idx0, idx)
    ax[1, 1].errorbar(x, np.exp(expData[0, idx0:idx]),
                      yerr=np.exp(expData[0, idx0:idx])*expData[1, idx0:idx],
                      fmt="ob")
    ax[1, 1].errorbar(x, pred[idx0:idx], yerr=predErr[idx0:idx], fmt="or")

    ax[0, 1].legend(["data", "model"], loc=3)
    ax[0, 0].set_title(r"$\gamma +$ Pb Int")
    ax[0, 1].set_title(r"$\gamma +$ Pb $t$-diff")
    ax[1, 0].set_title(r"$\gamma + p$ Int")
    ax[1, 1].set_title(r"$\gamma + p$ $t$-diff")
    ax[0, 0].set_yscale("log")
    ax[0, 1].set_yscale("log")
    ax[1, 0].set_yscale("log")
    ax[1, 1].set_yscale("log")
    st.pyplot(fig)


if __name__ == '__main__':
    main()
