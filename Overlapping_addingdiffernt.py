# In this at the end of filevector I am putting the dirname
# so loop over n-1 files and n will give the name of the output dir.

# In legend also the n element will give the name for the ratio plot y axis label.
#edited by Monika Mittal 
#Script for ratio plot 
import sys

import ROOT 
ROOT.gROOT.SetBatch(True)
sys.argv.append( '-b-' )


from ROOT import TFile, TH1F, gDirectory, TCanvas, TPad, TProfile,TGraph, TGraphAsymmErrors
from ROOT import TH1D, TH1, TH1I
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TStyle
from ROOT import TLegend
from ROOT import TMath
from ROOT import TPaveText
from ROOT import TLatex

import os
colors=[1,2,3,4,5,6,7,15,46,40,8,9,11,41,46,30,12,28,20,32]
markerStyle=[23,21,22,20,24,25,26,27,28,29,20,21,22,23]            
linestyle=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


def DrawOverlap(fileVec, histVec, titleVec,legendtext,pngname,logstatus=[0,0],xRange=[-99999,99999,1]):

    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    gStyle.SetTitleOffset(1.1,"Y");
    gStyle.SetTitleOffset(0.9,"X");
    gStyle.SetLineWidth(3)
    gStyle.SetFrameLineWidth(3); 

    i=0

    histList_=[]
    histList=[]
    histList1=[]
    maximum=[]
    
    ## Legend    
    leg = TLegend(0.350, 0.550, 0.89, 0.89)#,NULL,"brNDC");
    leg.SetBorderSize(0)
#    leg.SetNColumns(2)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(22)
    leg.SetTextSize(0.035)
     
    c = TCanvas("c1", "c1",0,0,500,500)
    #c.SetBottomMargin(0.01)
    #c.SetLeftMargin(0.15)
    #c.SetLogy(0)
    #c.SetLogx(0)
    c1_2 = TPad("c1_2","newpad",0.04,0.05,1,0.994)
    c1_2.Draw()

    
    print ("you have provided "+str(len(fileVec))+" files and "+str(len(histVec))+" histograms to make a overlapping plot" )
    print "opening rootfiles"
    c.cd()
   # c1_2.SetBottomMargin(0.0003)
    c1_2.SetLogy(logstatus[1])
    c1_2.SetLogx(logstatus[0])
    
    
    c1_2.cd()
    ii=0    
    inputfile={}

    for ifile_ in range(len(fileVec)):
        print ("opening file  "+fileVec[ifile_])
        inputfile[ifile_] = TFile( fileVec[ifile_] )
        name_hist= (fileVec[ifile_].split(".")[1]).split("/")[-1]+"_SR"
        print "fetching histograms"
        for ihisto_ in range(len(histVec)):

            histoname___ = histVec[ihisto_]
            
            print histoname___
            if ((histoname___ == "met_pt_") | (histoname___ == "delta_phi_ZMet_bst_") | (histoname___ == "delta_phi_j_met_") | (histoname___ == "deltaPhiClosestJetMet_") |(histoname___ == "deltaPhiFarthestJetMet_")):
                histoname___ = histoname___ +name_hist 
            histo = inputfile[ifile_].Get(histoname___)
            print(histo)
            histList.append(histo)

            # for ratio plot as they should nt be normalize 
            histList1.append(histo)
            print(histList[ii] , " with Integral   ", histList[ii].Integral() )
            histList[ii].Rebin(xRange[2])
            histList[ii].Scale(1.0/histList[ii].Integral())
            maximum.append(histList[ii].GetMaximum())
            ii=ii+1
    maximum.sort()


    for ih in range(len(histList)):
        tt = type(histList[ih])
        if logstatus[1] is 1 :
            histList[ih].SetMaximum(100) #1.4 for log
            histList[ih].SetMinimum(0.01) #1.4 for log
        if logstatus[1] is 0 :
            max_ = maximum[3] +(maximum[0]/2)
            histList[ih].SetMaximum(max_) #1.4 for log
            histList[ih].SetMinimum(0.0) #1.4 for log
#        print "graph_status =" ,(tt is TGraphAsymmErrors)
#        print "hist status =", (tt is TH1D) or (tt is TH1F)
        if ih == 0 :      
            if tt is TGraphAsymmErrors : 
                histList[ih].Draw("APL")
            if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
                histList[ih].Draw("hist")   
        if ih > 0 :
            #histList[ih].SetLineWidth(2)
            if tt is TGraphAsymmErrors : 
                histList[ih].Draw("PL same")
            if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
                histList[ih].Draw("hist same")   

        if tt is TGraphAsymmErrors :
            histList[ih].SetMaximum(100) 
            histList[ih].SetMarkerColor(colors[ih])
            histList[ih].SetLineColor(colors[ih])
            histList[ih].SetMarkerStyle(markerStyle[ih])
            histList[ih].SetMarkerSize(1)
            leg.AddEntry(histList[ih],legendtext[ih],"PL")
        if (tt is TH1D) or (tt is TH1F) or (tt is TH1) or (tt is TH1I) :
            histList[ih].SetLineStyle(linestyle[ih])
            histList[ih].SetLineColor(colors[ih])
            histList[ih].SetLineWidth(3)
            leg.AddEntry(histList[ih],legendtext[ih],"L")
        histList[ih].GetYaxis().SetTitle(titleVec[1])
        histList[ih].GetYaxis().SetTitleSize(0.052)
        histList[ih].GetYaxis().SetTitleOffset(0.98)
        histList[ih].GetYaxis().SetTitleFont(22)
        histList[ih].GetYaxis().SetLabelFont(22)
        histList[ih].GetYaxis().SetLabelSize(.052)
        histList[ih].GetXaxis().SetRangeUser(xRange[0],xRange[1])
        histList[ih].GetXaxis().SetLabelSize(0.0000);
        histList[ih].GetXaxis().SetTitle(titleVec[0])
        histList[ih].GetXaxis().SetLabelSize(0.052)
        histList[ih].GetXaxis().SetTitleSize(0.052)
#        histList[ih].GetXaxis().SetTitleOffset(1.02)
        histList[ih].GetXaxis().SetTitleFont(22)
        histList[ih].GetXaxis().SetTickLength(0.07)
        histList[ih].GetXaxis().SetLabelFont(22)
        histList[ih].GetYaxis().SetLabelFont(22) 
        histList[ih].GetXaxis().SetNdivisions(508)
        #histList[ih].GetXaxis().SetMoreLogLabels(); 
        #histList[ih].GetXaxis().SetNoExponent();
        #histList[ih].GetTGaxis().SetMaxDigits(3);

        i=i+1
    pt = TPaveText(0.0877181,0.9,0.9580537,0.96,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(22)
    pt.SetTextSize(0.046)
    text = pt.AddText(0.01,0.5,"CMS Internal")
    text = pt.AddText(0.70,0.5,"#sqrt{s} = 13 TeV ")
    pt.Draw()
   
    

#    t2a = TPaveText(0.0877181,0.81,0.9580537,0.89,"brNDC")
#    t2a.SetBorderSize(0)
#    t2a.SetFillStyle(0)
#    t2a.SetTextSize(0.040) 
#    t2a.SetTextAlign(12)
#    t2a.SetTextFont(62)
#    histolabel1= str(fileVec[(len(fileVec)-1)])
#    text1 = t2a.AddText(0.06,0.5,"CMS Internal") 
#    t2a.Draw()
    leg.Draw()
#
#    c.cd()
    outputdirname = 'plots/'
    histname=outputdirname+pngname 
    c.SaveAs(histname+'.png')
    c.SaveAs(histname+'.pdf')
    outputname = 'cp  -r '  +    outputdirname   + '    '+  '/eos/user/m/mmittal/www/VBSZZ2l2nu/'

    os.system(outputname) 
    

file_s="/afs/cern.ch/work/m/mmittal/private/VBS2l2nu/Plotting/CMSSW_11_0_2/src/WFH2016/merged/"

files=[file_s+'DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
       file_s+'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
       file_s+'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
       file_s+'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
       file_s+'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
       file_s+'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root',
       file_s+'ZZJJ_ZZTo2L2Nu_EWK_13TeV-madgraph-pythia8.root']
legend=['DYJetsToLL_M-50_HT-70to100','DYJetsToLL_M-50_HT-100to200','DYJetsToLL_M-50_HT-200to400','DYJetsToLL_M-50_HT-400to600','DYJetsToLL_M-50_HT-600to800','DYJetsToLL_M-50_HT-800to1200','ZZJJ_ZZTo2L2Nu_EWK']
ytitle='Events Normalized to 1'

DrawOverlap(files,['jet_parton_SR'],['jet_parton',ytitle],legend,'jet_parton_SR',xRange=[-5,25,1])
DrawOverlap(files,['Jet_qgl_SR'],['jet_qgl',ytitle],legend,'jet_qgl',xRange=[0,1,1])
DrawOverlap(files,['Jet_parton_mask_SR'],['jet_parton',ytitle],legend,'Jet_parton_mask_SR',xRange=[-5,25,1])
DrawOverlap(files,['met_pt_'],['E_{T}^{miss}',ytitle],legend,'met_pt_SR_norebin',xRange=[0,400,2])
DrawOverlap(files,['delta_phi_ZMet_bst_'],['#Delta#Phi(Z,E_{T}^{miss}',ytitle],legend,'delta_phi_ZMet_bst_SR',xRange=[0,3.5,1])
DrawOverlap(files,['delta_phi_j_met_'],['#Delta#Phi(Jet,E_{T}^{miss}',ytitle],legend,'delta_phi_j_met_SR',xRange=[0,3.5,1])
DrawOverlap(files,['deltaPhiClosestJetMet_'],['#Delta#Phi(closetJet,E_{T}^{miss}',ytitle],legend,'deltaPhiClosestJetMet_SR',xRange=[0,3.5,1])
DrawOverlap(files,['deltaPhiFarthestJetMet_'],['#Delta#Phi(farthestJet,E_{T}^{miss}',ytitle],legend,'deltaPhiFarthestJetMet_SR',xRange=[0,3.5,1])


#met_pt_WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8_SR
'''
#DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/ditaus_BDT'],['Ditau BDT score',ytitle],legend,'hm_DitauBDTscore')


DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/n_muons'],["muons",ytitle],legend,'hm_NMuons',xRange=[0,6,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/n_electrons'],['# electrons',ytitle],legend,'hm_NElectrons',xRange=[0,6,1])
#DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/'],['# subjets',ytitle],legend,'hm_DitauNsubjets')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/n_ditau'],['# Ditau',ytitle],legend,'hm_NDitau',xRange=[0,6,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/n_Bjet'],['# b-jets',ytitle],legend,'hm_Nbjets',xRange=[0,6,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/n_tau'],['# taus',ytitle],legend,'hm_taus',xRange=[0,6,1])

#DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/DitauPhi'],['#Phi(Ditau)',ytitle],legend,'hm_DitauPhi')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/MET'],['MET',ytitle],legend,'hm_MET',xRange=[0,400,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_pre/n_jet'],['# jets',ytitle],legend,'hm_Njets',xRange=[0,6,1])


DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/DitauNsubjets'],['# of subjet in ditau',ytitle],legend,'Boosted_DitauNsubjets',xRange=[0,6,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/DitauBDTscore'],['Ditau BDT score',ytitle],legend,'Boosted_DitauBDTscore',xRange=[0,1,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/DitauCharge'],['ditau charge',ytitle],legend,'Boosted_DitauCharge',xRange=[-5,5,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/BjetsPt_sublead'],['sublead b-jet pT',ytitle],legend,'Boosted_BjetsPt_sublead',xRange=[0,400,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/BjetsPt_lead'],['lead b-jet pT',ytitle],legend,'Boosted_BjetsPt_lead',xRange=[0,400,1])
#DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/n_Bjet'],['# b-jets',ytitle],legend,'Boosted_Nbjets')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/Njets_signal'],['# jets(signal)',ytitle],legend,'Boosted_Njets_signal',xRange=[0,10,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/DitauPt'],['Pt(Ditau)',ytitle],legend,'Boosted_DitauPt',xRange=[0,600,1])
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/DitauEta'],['#eta (ditau)',ytitle],legend,'Boosted_DitauEta')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/DeltaPhiDitauMET'],['#phi(ditau, MET)',ytitle],legend,'Boosted_DeltaPhiDitauMET')
'''
'''
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/'],['',ytitle],legend,'Boosted_')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/'],['',ytitle],legend,'Boosted_')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/'],['',ytitle],legend,'Boosted_')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/'],['',ytitle],legend,'Boosted_')
DrawOverlap(files,['0ptag0pjet_0ptv_SR_boosted/'],['',ytitle],legend,'Boosted_')

'''




