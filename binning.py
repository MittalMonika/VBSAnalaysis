binning_={"Z_mass":[40,0,200],
          "Z_pt":[100,0,1000],
          "Z_eta":[50,-2.5,2.5],
          "Z_phi":[35,0,3.5],
          "met_pt":[80,0,800],
          "met_phi":[40,0,3.14],
          "lead_jet_pt":[100,0,1000],
          "lead_jet_phi":[35,0,3.5],
          "lead_jet_eta":[50,-2.5,2.5], 
          "trail_jet_pt":[100,0,1000],
          "trail_jet_phi":[35,0,3.5],
          "trail_jet_eta":[50,-2.5,2.5] ,
          "ngood_jets":[5,0,5],
          "ngood_bjets":[5,0,5],
          "nhad_taus":[5,0,5],
          "lep_category":[5,0,5],
          "delta_R_ll":[35,0,3.5],
          "dijet_Mjj":[15,0,1500],
          "dijet_abs_dEta":[20,0,10],
          "Jet_etas_multiplied":[11,-5,5],
          "delta_phi_ZMet":[35,0,3.5],
          "delta_phi_ZMet_bst":[35,0,3.5],
          "delta_phi_ZMet_cal":[35,0,3.5],
          "deltaPhiClosestJetMet":[35,0,3.5],
          "deltaPhiFarthestJetMet":[35,0,3.5], 
          "delta_phi_j_met":[35,0,3.5],


          
           "dijet_Zep":[50, -5, 5],
           "met_significance":[50, 0, 50],
          
           "Jet_genJetIdx":[17,-2,15],
           "Jet_partonFlavour":[31,-5,25],
           "Jet_hadronFlavour":[10,1,10],
           "ngood_jets":[11,0,10],
           "Jet_qgl":[20,0,1]
}


binning_cr_=binning_.copy()
binning_cr_["dijet_Mjj"] = [12,200,500]
