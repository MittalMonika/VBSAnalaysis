import array as ar
import numpy as np

def get_binning(n_min_max):
    binning = np.linspace(n_min_max[1], n_min_max[2], n_min_max[0] + 1) 
    return ar.array('d', binning)


binning = {
    'CJV_Pt_Sum': 
        ['CJV_Pt_Sum', get_binning([15, 0, 300])],
    'abs_delta_phi_j_met': 
        ['#Delta#phi(jet, MET)', get_binning([35, 0, 3.5])],
    'abs(delta_phi_j_met)': 
        ['#Delta#phi(jet, MET)', get_binning([35, 0, 3.5])],
    'delta_phi_j_met/pi': 
        ['#Delta#phi(jet, MET) / #pi', get_binning([10, -1, 1])],
    'delta_phi_j_met': 
        ['#Delta#phi(jet, MET)', get_binning([10, -3.14, 3.14])],        
    'abs_delta_phi_ZMet': 
        ['#Delta#phi(Z, MET)', get_binning([35, 0, 3.5])],
    'abs(delta_phi_ZMet)': 
        ['#Delta#phi(Z, MET)', get_binning([35, 0, 3.5])],
    'delta_phi_ZMet/pi': 
        ['#Delta#phi(Z, MET) / #pi', get_binning([20, -1, 1])],
    'abs(delta_phi_ZMet)/pi': 
        ['|#Delta#phi(Z, MET)| / #pi', get_binning([20, 0, 1])],        
#        ['#Delta#phi(Z, MET) / #pi', get_binning([20, -1, 1])],
    'delta_phi_ll/pi': 
        ['delta_phi_ll/pi', get_binning([20, -1, 1])],
    'delta_R_ll': 
        ['#DeltaR_{ll}', get_binning([10, 0.5, 2.5])],
    'dijet_abs_delta_eta': 
        ['#Delta#eta_{jj}', get_binning([20, 0, 10])],
    'dijet_abs_delta_eta/dijet_Mjj': 
        ['#Delta#eta_{jj}/M_{jj}', get_binning([20, 0, 0.01])],
    '(sqrt(dijet_Mjj)-10)/dijet_abs_delta_eta': 
        ['(sqrt(dijet_Mjj)-10)/dijet_abs_delta_eta', get_binning([20, 0, 20])],
    'dijet_centrality_gg': 
        ['Dijet Centrality', get_binning([20, 0, 1])],
    'dijet_Mjj': 
        ['dijet_Mjj', get_binning([14, 100, 1500]), ],
#         ['M_{jj} [GeV]', ar.array('d', [100, 200, 300, 400, 500, 600, 700, 900, 1100, 1500, 2000])],
         #['dijet_Mjj', get_binning([12, 200, 500])],
    'dijet_Zep': 
        ['dijet_Zep', get_binning([50, -5, 5])],
    'emulatedMET': 
        ['Emulated MET [GeV]', ar.array('d', [50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600])],
    'emulatedMT': 
        ['Emulated M_{T} [GeV]', ar.array('d', [100, 200, 250, 300, 350, 400, 500, 600, 700, 800, 1000, 1200])],
    '(emulatedMET_phi-Z_phi)/pi': 
        ['#Delta#phi(jet, emulatedMET) / #pi', get_binning([10, -1, 1])],
    'EtaM_ratio': 
        ['ln(#Delta#eta_{jj}) / M_{jj}', get_binning([20, 0, 0.004])],
    'H_T': 
        ['H_T', get_binning([50, 0, 1000])],
    'HT_F': 
        ['HT_F', get_binning([20, 0.3, 1.1])],
    'Jet_etas_multiplied': 
        ['Jet_etas_multiplied', get_binning([10, -10, 0])],
    'Jet_pt_Ratio': 
        ['Jet_pt_Ratio', get_binning([20, 0, 1])],
    'lep_category': 
        ['lep_category', get_binning([10, 0, 10])],
    'abs(lead_jet_eta)': 
        ['|leading jet #eta|', get_binning([12, 0, 4])],
    'lead_jet_pt': 
        # ['lead_jet_pt', get_binning([50, 0, 500])],
        ['lead_jet_pt', ar.array('d', [0, 25, 50, 75, 100, 125, 150, 200, 300, 500])],
    'lead_jet_pt/trail_jet_pt': 
        ['lead_jet_pt/trail_jet_pt', get_binning([25, 0, 25])],
    'ngood_bjets': 
        ['Number of b-jets', get_binning([10, 0, 10])],
    'MT': 
        ['MT', ar.array('d', [100, 200, 250, 300, 350, 400, 500, 600, 700, 800, 1000, 1200])],
    'MET_significance': 
        ['MET_significance', get_binning([50, 0, 50])],
    'met_significance': 
        ['met_significance', get_binning([50, 0, 50])],
    'met_pt': 
        # ['met_pt', ar.array('d', [50, 60, 70, 80, 90, 100])],
        # ['met_pt', ar.array('d', [50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600])],
        ['MET [GeV]', get_binning([20, 0, 800])],
    'met_pt/Z_pt': 
        ['met_pt/Z_pt', get_binning([40, 0, 2])],
    'ngood_jets': 
        ['ngood_jets', get_binning([10, 0, 10])],
    'sca_balance': 
        ['balance', get_binning([25, 0, 5])],
    'score': 
        ['score', get_binning([11 * 2, -0.05, 1.05])],
    'S_T_jets': 
        ['S_T_jets', get_binning([20, 0, 1])],
    'S_T_hard': 
        ['S_T_hard', get_binning([20, 0, 1])],
    'S_T_all': 
        ['S_T_all', get_binning([20, 0, 1])],
    'trail_jet_eta': 
        ['trail_jet_eta', get_binning([100, 5, 5])],
    'trail_jet_pt': 
        # ['trail_jet_pt', get_binning([15, 0, 300])],
        ['trail_jet_pt', ar.array('d', [0, 25, 50, 75, 100, 125, 150, 200, 300, 500])],
    'x_Z': 
        ['x_Z', get_binning([20, 0, 1])],
    'x_jet20': 
        ['x_jet20', get_binning([20, 0, 1])],
    'x_jet30': 
        ['x_jet30', get_binning([20, 0, 1])],
    'Z_pt': 
        # ['Z_pt', ar.array('d', [50, 60, 70, 80, 90, 100])],
        # ['Z_pt', ar.array('d', [50, 100, 125, 150, 175, 200, 250, 300, 350, 400, 500, 600])],
        ['Dilepton pT [GeV]', get_binning([10, 0, 1050])],
    'Z_eta': 
        ['Z_eta', get_binning([12, -3, 3])],
    'Z_mass': 
        ['M_Z [GeV]', get_binning([30, 60, 120])],
}
