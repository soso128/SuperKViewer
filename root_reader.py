from numpy import *
import pandas as pd
import ROOT as r
from glob import glob
from event_classes import Muon, Track, Bonsai

# Load libraries
libs = glob("/home/elhedri/skofl/lib/*.so")
for ll in libs:
    r.gSystem.Load(ll)

def get_root_tree(rootfile):
    f = r.TFile.Open(rootfile)
    tr = f.Get("data")
    return tr

def get_cct(event):
    cables = event.TQREAL.cables
    times = event.TQREAL.T
    charges = event.TQREAL.Q
    nhits = event.TQREAL.nhits
    res = pd.DataFrame(array([array([cables[i] & (2**16 - 1), charges[i], times[i]]) for i in range(nhits)]), columns = ['cable', 'charge', 'time'])
    res.astype({'cable': 'int64'}, copy = False)
    return res

def get_mu_info(event):
    mu = event.MU
    muon = Muon()
    muon.muboy_status = mu.muboy_status
    muon.muboy_ntracks = mu.muboy_ntrack
    muon.muboy_dir = [mu.muboy_dir[j] for j in range(3)]
    muon.muboy_goodness = mu.muboy_goodness
    muon.muboy_length = mu.muboy_length
    muon.muboy_dedx = [mu.muboy_dedx[j] for j in range(int(muon.muboy_length/50) + 1)]
    for i in range(muon.muboy_ntracks):
        t = Track()
        t.muboy_entpos = [mu.muboy_entpos[i * 4 + j] for j in range(4)]
        t.muboy_entpos[3] /= 21.58333
        muon.tracks.append(t)
    return muon

def get_bonsai_vertex(event):
    lowe = event.LOWE
    bonsai = Bonsai()
    bonsai.vertex = [lowe.bsvertex[i] for i in range(3)]
    bonsai.dir = [lowe.bsdir[i] for i in range(3)]
    bonsai.good = [lowe.bsgood[i] for i in range(3)]
    bonsai.dirks = lowe.bsdirks
    bonsai.energy = lowe.bsenergy
    bonsai.cossun = lowe.bscossun
    return bonsai
