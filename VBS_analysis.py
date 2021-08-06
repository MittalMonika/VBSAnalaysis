import ROOT
import os 
import sys 
import time
import uproot 
import numpy as np
import multiprocessing as mp
from functools import partial
import glob
from ROOT import TH1F, TFile, TLorentzVector
from utils import SetHist, VarToHist 
from binning import binning_, binning_cr_ 
from math import hypot, pi


s_outputdir = "Re"


#delta phi,eta, R calculation
def deltaphi(phi1,phi2):
#    phi1_unzip, phi2_unzip = phi1.cross(phi2, nested=True).unzip()
    # function taken from https://github.com/cms-nanoAOD/nanoAOD-tools/blob/master/python/postprocessing/tools.py#L7
# 
    phi1_unzip =phi1
    phi2_unzip =phi2
    dphi_unzip = np.subtract(phi1_unzip,phi2_unzip)
    np.place(dphi_unzip, dphi_unzip > pi, dphi_unzip-(2 * pi))
    np.place(dphi_unzip, dphi_unzip < pi, dphi_unzip+(2 * pi))
    
   # while dphi_unzip > pi:
   #     dphi_unzip =dphi_unzip-(2 * pi)
   # while dphi_unzip < -pi:
   #     dphi_unzip =dphi_unzip+(2 * pi)
    return abs(dphi_unzip)

def deltaeta(eta1,eta2):
    eta1_unzip, eta2_unzip = eta1.cross(eta2, nested=True).unzip()
    deta_unzip = eta1_unzip - eta2_unzip
    return deta_unzip

def deltaR(eta1, eta2, phi1, phi2, cut_=0.4):
    deta_unzip = deltaeta(eta1,eta2)
    dphi_unzip = deltaphi(phi1,phi2)

    dr_unzip = numpy.sqrt(deta_unzip**2 + dphi_unzip**2)
    dr_pho_jet_status = (dr_unzip<cut_).any() ## use axis in new version of awkward                                                                                                  return dr_pho_jet_status


#EWK correction
def do_diboson_corr(dataset):
    do_corr = False
    if 'ZZTo' in dataset and 'GluGlu' not in dataset and 'ZZJJ' not in dataset:
        do_corr = True
    if 'WZTo' in dataset and 'GluGlu' not in dataset:
        do_corr = True
    return(do_corr)    



#inputpath_="/eos/cms/store/user/mmittal/VBS/monika_WFH2016/"
#nputpath_="/eos/cms/store/user/mmittal/VBS/copy_for_test/"
#inputpath_="/eos/user/m/mmittal/VBS/copy_for_test"
inputpath_= "/eos/cms/store/group/phys_smp/ZZTo2L2Nu/VBS/WFH2016/"
#inputpath_= "/eos/cms/store/group/phys_smp/ZZTo2L2Nu/VBS/mmittal/PhotonCR2016/"
#inputpath_="/eos/cms/store/group/phys_smp/ZZTo2L2Nu/VBS/mmittal/PhotonCR2016_fixed_/"
trees_ = ['Events','Runs']
start = time.clock()
def runOneFile(trees,filename):
    print("ruuning code for",filename)
    outputpathlist_ = inputpath_.split("/")
    if len(outputpathlist_[-1])>0:
        outputpath_=outputpathlist_[-1]
    else:
        outputpath_=outputpathlist_[-2]
    tree_ = uproot.open(filename)[trees[0]]
    #limitedcache = uproot.cache.MemoryCache(5*1024)
    mycache = uproot.ArrayCache("1000 kB")
#    tree_.arrays("*", cache=mycache)    
    mass_z = 91.1876



    nJet = tree_.array("nJet")
    Jet_pt_nom = tree_.array("Jet_pt_nom")
    lead_jet_pt= tree_.array("lead_jet_pt")
    lead_jet_eta= tree_.array("lead_jet_eta")
    lead_jet_phi= tree_.array("lead_jet_phi")
    trail_jet_pt =tree_.array("trail_jet_pt")
    trail_jet_eta= tree_.array("trail_jet_eta")
    trail_jet_phi= tree_.array("trail_jet_phi")
    lep_category  =tree_.array("lep_category")
    ngood_jets    =tree_.array("ngood_jets")
    ngood_bjets   =tree_.array("ngood_bjets") 
    nhad_taus     =tree_.array("nhad_taus")
    met_pt        =tree_.array("met_pt")
    met_phi        =tree_.array("met_phi")
    delta_R_ll    =tree_.array("delta_R_ll")
    delta_phi_j_met=tree_.array("delta_phi_j_met")
    Jet_etas_multiplied=tree_.array("Jet_etas_multiplied")
    dijet_Mjj          =tree_.array("dijet_Mjj")
    dijet_abs_dEta     =tree_.array("dijet_abs_dEta")
    
    # Get variables from event tree                                                                                                                                           
    Z_pt = tree_.array("Z_pt")
    Z_eta = tree_.array("Z_eta")
    Z_phi = tree_.array("Z_phi")
    Z_mass = tree_.array("Z_mass")
    '''
    Z_p4 = ROOT.TLorentzVector()
    Z_p4.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, Z_mass)
    Z_p4_bst = ROOT.TLorentzVector(Z_p4)
    '''

#    Jet_genJetIdx      =tree_.array("Jet_genJetIdx") #jet and gen jet matching
#    Jet_hadronFlavour = tree_.array("Jet_hadronFlavour")
#    Jet_partonFlavour = tree_.array("Jet_partonFlavour")

    deltaPhiClosestJetMet =tree_.array("deltaPhiClosestJetMet")
    deltaPhiFarthestJetMet =tree_.array("deltaPhiFarthestJetMet")
    delta_phi_ZMet_bst=tree_.array("delta_phi_ZMet_bst")
    delta_phi_ZMet=tree_.array("delta_phi_ZMet")
    delta_phi_ZMet_cal = deltaphi(Z_phi,met_phi)

#    print(len(delta_phi_ZMet_cal))
    datasetname = filename.split('/')[-2]
    #weight 
    data_name=['DoubleEG','DoubleMuon','MuonEG','SingleElectron','SingleMuon']
    InMC = [s for s in data_name if s in datasetname]

    if(len(InMC) == 0):
        weight         =tree_.array("weight")
        puWeight       =tree_.array("puWeight")
        w_muon_SF      =tree_.array("w_muon_SF") 
        w_electron_SF  =tree_.array("w_electron_SF") 
        PrefireWeight  =tree_.array("PrefireWeight")
        nvtxWeight     =tree_.array("nvtxWeight")
        TriggerSFWeight =tree_.array("TriggerSFWeight")
        btagEventWeight =tree_.array("btagEventWeight")
        Jet_partonFlavour = tree_.array("Jet_partonFlavour") 
        Jet_qgl = tree_.array("Jet_qgl")
        corrections= weight*puWeight*w_muon_SF*w_electron_SF*PrefireWeight*nvtxWeight*TriggerSFWeight


        if do_diboson_corr(datasetname):
            print("doing dibodon correction: ",datasetname)
            kEW             =tree_.array("kEW")
            kNNLO           =tree_.array("kNNLO")            
            corrections = corrections*kEW*kNNLO

    else :
        corrections = tree_.array("weight")

    cuts_ =(((lep_category ==1) | (lep_category==3)))     

    cuts_SR = (((lep_category ==1) | (lep_category==3)) &
               (ngood_jets >= 2)  &
               (ngood_bjets == 0 ) &
               (nhad_taus == 0  ) &
               (met_pt > 60.0) & 
               (delta_R_ll < 2.5 )  &
               (np.abs(delta_phi_j_met) > 0.5 ) &
               (np.abs(delta_phi_ZMet_bst) > 1.0 ) &
               (np.abs(Z_mass - mass_z) < 30.0 )&
               (Jet_etas_multiplied < 0 ) &
               (dijet_Mjj > 400.0 ) &
               (dijet_abs_dEta> 2.4))
    
    cuts_CR_DY = (((lep_category==1) | (lep_category==3)) &
               (ngood_jets >= 2)   &
               (ngood_bjets == 0 ) &
               (nhad_taus == 0  ) &
               (met_pt > 60) & 
               (delta_R_ll < 2.5 )  &
               (np.abs(delta_phi_j_met) > 0.5 ) &
               (np.abs(delta_phi_ZMet_bst) > 1.0 ) &
               (np.abs(Z_mass - mass_z) < 30 )&
               (Jet_etas_multiplied < 0 ) &
               (dijet_Mjj < 400 ) &
               (dijet_abs_dEta< 2.4))

    cuts_CR1 = (((lep_category ==1) | (lep_category==3)) &
                  (ngood_jets >= 2)  &
                  (ngood_bjets == 0 ) &
                  (nhad_taus == 0  ) &
                  (met_pt > 60) &
                  (np.abs(delta_phi_j_met) > 0.5 ) &
                  (np.abs(delta_phi_ZMet_bst) > 1.0 ) &
                  (np.abs(Z_mass - mass_z) < 30 ))



    



    
    if(len(InMC) == 0):
        mask_pdgid=((Jet_pt_nom==lead_jet_pt) & (cuts_SR))
        jet_parton_cut =Jet_partonFlavour[mask_pdgid]
        Jet_qgl_cut =Jet_qgl[mask_pdgid]
        mask_qgl = ((Jet_pt_nom==lead_jet_pt) & (Jet_qgl > 0.6) & (cuts_SR))
        jet_parton_mask = Jet_partonFlavour[mask_qgl]


    
    passed_events = len(dijet_Mjj[cuts_SR])
    outfilename = s_outputdir+outputpath_+ '/'+filename.split('/')[-2]+'/'+filename.split('/')[-1]
    fout = TFile(outfilename, "RECREATE")
    print(outfilename)
    tree_runs = uproot.open(filename)[trees[1]]

    if(len(InMC) == 0):
        h_total= TH1F("h_total", "h_total", 2, 0.5,2.5)
        h_total.SetBinContent(1, tree_runs.array("genEventSumw").sum())
        fout.cd()
        h_total.Write()

#    varnames=["dijet_abs_dEta"]

    varnames=["Z_pt","Z_mass","Z_eta","Z_phi",
               "met_pt","met_phi",
               "lead_jet_pt","lead_jet_eta","lead_jet_phi",
               "trail_jet_pt","trail_jet_eta","trail_jet_phi",
               "ngood_jets","ngood_bjets","nhad_taus","lep_category",
               "delta_R_ll",
               "dijet_Mjj","dijet_abs_dEta","Jet_etas_multiplied",
               "delta_phi_ZMet","delta_phi_j_met","delta_phi_ZMet_bst","deltaPhiClosestJetMet","deltaPhiFarthestJetMet"]

    for ihist in varnames:
        ## you need to copy the binning using [:] other wise the binning will be just referenced and to ensure a deep copy make [:]
        histoname = ihist+"_"+filename.split('/')[-2]+"_"
        h1 = VarToHist(tree_.array(ihist)[cuts_SR],corrections[cuts_SR], histoname+"SR", binning_[ihist][:])
        h2 = VarToHist(tree_.array(ihist)[cuts_CR1], corrections[cuts_CR1],histoname+"validation", binning_cr_[ihist][:])
        h3 = VarToHist(tree_.array(ihist)[cuts_CR_DY], corrections[cuts_CR_DY],histoname+"CRDY", binning_[ihist][:])
        h4 = VarToHist(tree_.array(ihist)[cuts_],corrections[cuts_], histoname+"nocuts", binning_[ihist][:])


        

        fout.cd() 
        h1.Write()
        h2.Write()
        h3.Write()
        h4.Write()       


    histoname = "delta_phi_ZMet_cal"+"_"+filename.split('/')[-2]+"_"    
    h6 = VarToHist(delta_phi_ZMet_cal[cuts_SR],corrections[cuts_SR], histoname+"SR", binning_[ihist][:])    
    h7 = VarToHist(delta_phi_ZMet_cal[cuts_CR1],corrections[cuts_CR1], histoname+"validation", binning_[ihist][:])    
    h8 = VarToHist(delta_phi_ZMet_cal[cuts_CR_DY],corrections[cuts_CR_DY], histoname+"CRDY", binning_[ihist][:])    
    h9 = VarToHist(delta_phi_ZMet_cal[cuts_],corrections[cuts_], histoname+"nocuts", binning_[ihist][:])    
    fout.cd()
    h6.Write()
    h7.Write()
    h8.Write()
    h9.Write()

    '''           
    if(len(InMC) == 0):
      print("filename",filename)  
      h4 = VarToHist(jet_parton_cut.flatten(), corrections[cuts_SR],"jet_parton_SR", binning_["Jet_partonFlavour"][:])        
      new_mask = (mask_qgl.sum())
      h6 = VarToHist(jet_parton_mask.flatten(), corrections[(new_mask ==1)],"Jet_parton_mask_SR", binning_["Jet_partonFlavour"][:])        
      h5 = VarToHist(Jet_qgl_cut.flatten(),corrections[cuts_SR], "Jet_qgl_SR", binning_["Jet_qgl"][:])        
      fout.cd()
      h4.Write()
      h5.Write()
      h6.Write()
    '''



def main():
    files_list=[]
    outputpathlist_ = inputpath_.split("/")
    if len(outputpathlist_[-1])>0:
        outputpath__=outputpathlist_[-1]
    else:
        outputpath__=outputpathlist_[-2]


    try:
        print("you can provide the name of the string to be placed before your outputdir name thatvis identical to inputdir",outputpath__)
        outputpath_ =s_outputdir+outputpath__
        print("here output dir name is :", outputpath_)
        os.mkdir(outputpath_)
        print(outputpath_)
    except OSError: 
        print ("The directory {} is already present, please clean up or write another dir name".format(outputpath_))
    else: 
        print(" lesi in for dir ")


    for inputpath, dirs, files  in os.walk(inputpath_):
        
        
        ''' create dir structure similar to the input '''
        print(dirs)
        try:
            for dir_ in dirs:
                outputpath_full_ = os.path.join(outputpath_,dir_)
                os.mkdir (outputpath_full_)
                print ("created directory: {}".format(os.path.join(outputpath_full_)))
        except: 
            print ("the directory need not be created")
        else: 
            print ("{} is aready created, so not creating again".format(outputpath_))
    
        ''' now loop over the files to run the code ''' 
        for ifile in files:
            inputrootfile_ = os.path.join(inputpath, ifile)
            inputrootfile_list_=inputrootfile_.split("/")
            outputdir_fromInput_= "/".join(inputrootfile_list_[-2:])
            outputrootfile_ = os.path.join(outputpath_,outputdir_fromInput_)
            #print ("$$$$$", inputrootfile_, outputrootfile_)
            #will only run on the file that are not in the output dir 
            if ((os.path.exists(outputrootfile_)) & (os.path.getsize(outputrootfile_) <= 30000) ):
                print(outputrootfile_,os.path.getsize(outputrootfile_))
                files_list.append(inputrootfile_)
            #first run without any cindition and after that with above condition     
            #if not (os.path.exists(outputrootfile_) ): 
            #    files_list.append(inputrootfile_)
            #runOneFile(trees_,inputrootfile_)



    print("files_list:",files_list)
    iterable = files_list
    pool = mp.Pool()
#commenting out the only below line
    func = partial(runOneFile,trees_)
#    print("iterable:", iterable)
    pool.map(func, iterable)
    pool.close()
    pool.join()
     #runOneFile(inputrootfile_,trees_)        
 
if __name__ == "__main__":
    main()   
    end = time.clock()
    print("%.4gs" % (end-start))
