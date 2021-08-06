import numpy as np
import pandas as pd
import math
from ROOT import TH1F, TFile
import pandas as pd

def SetHist(HISTNAME, binning):
    h = TH1F()
    if len(binning) == 3:
        h = TH1F(HISTNAME, HISTNAME, binning[0], binning[1], binning[2])
    else:
        nBins = len(binning) - 1
        #h = TH1F(HISTNAME, HISTNAME, binning[0], binning[1], binning[2])  ## make it variable binning histogram                                                                 \
                                                                                                                                                                                  
        h = TH1F(HISTNAME, HISTNAME, nBins, array('d', binning))
    return h



import  matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

def VarToHist(df_var, df_weight, HISTNAME, binning):
    df_var = pd.Series(df_var)

    h_var = SetHist(HISTNAME, binning)
    weight = df_weight

    if len(binning) >3:
        binning.append(10000) ## to take care of overflow                                                                                                                         
        n, bins, patches = plt.hist(df_var, binning, histtype='step', weights=weight)


    if len(binning)==3:
        binning.append(binning[-1]*3) ## to take care of overflow                                                                                                                 
        n, bins, patches = plt.hist(df_var, binning[0], range=(binning[1], binning[2]), histtype='step', weights=weight)
    ## this is outside if                                                                                                                                                       
                                                                                                                                                                                  
    n=list(n)
    #n_last = n[-1]
    #n.remove(n_last)
    #n[-1]  = n[-1]  + n_last
    for ibin in range(len((n))):
        h_var.SetBinContent(ibin+1, n[ibin])
    return h_var


