from numpy import *
from matplotlib.pyplot import *
import matplotlib.gridspec as gridspec

sk_id_zmax = 1810
sk_id_zmin = -1810
sk_id_rad = 1690

def sk_mesh(rbin = 0.1, thetabin = pi/6, xbin = 0.1, ybin = 0.1, Nhist = 0, wratios = 0.3, hratios = 0.5):
    Ncol = 2 if Nhist > 0 else 1
    gs0 = gridspec.GridSpec(1, Ncol, width_ratios = [1, wratios])
    gs = gridspec.GridSpecFromSubplotSpec(3, 1, height_ratios = [1, (sk_id_zmax - sk_id_zmin)/(2 * sk_id_rad), 1], subplot_spec = gs0[0], hspace = 0)
    histos = None
    if Nhist > 0:
        gs2 = gridspec.GridSpecFromSubplotSpec(Nhist, 1, subplot_spec = gs0[1], wspace = hratios)
        histos = (subplot(g) for g in gs2) 
    ax1 = subplot(gs[0], projection = 'polar')
    ax1.set_rmax(1)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.set_thetagrids(arange(0, 2 * pi, thetabin) * 180/pi)
    ax1.set_rgrids(arange(0, 1, rbin))
    ax1.set_facecolor('black')
    ax3 = subplot(gs[2], projection = 'polar')
    ax3.set_rmax(1)
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_thetagrids(arange(0, 2 * pi, thetabin) * 180/pi)
    ax3.set_rgrids(arange(0, 1, rbin))
    ax3.set_facecolor('black')
    ax2 = subplot(gs[1])
    ax2.set_xlim(0,1)
    ax2.set_ylim(0,1)
    ax2.tick_params(width = 0)
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax2.set_xticks(arange(0, 1, xbin))
    ax2.set_yticks(arange(0, 1, ybin))
    ax2.grid()
    ax2.set_aspect((sk_id_zmax - sk_id_zmin)/(2 * pi * sk_id_rad))
    ax2.set_facecolor('black')
    return (gcf(), ax1, ax2, ax3) + histos

def grid_redraw(mesh, rbin = 0.1, thetabin = pi/6, xbin = 0.1, ybin = 0.1):
    ax1, ax2, ax3 = mesh[1], mesh[2], mesh[3]
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.set_thetagrids(arange(0, 2 * pi, thetabin) * 180/pi)
    ax1.set_rgrids(arange(0, 1, rbin))
    ax1.set_rmax(1)
    ax1.set_facecolor('black')
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_thetagrids(arange(0, 2 * pi, thetabin) * 180/pi)
    ax3.set_rgrids(arange(0, 1, rbin))
    ax3.set_rmax(1)
    ax3.set_facecolor('black')
    ax2.tick_params(width = 0)
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    ax2.set_xticks(arange(0, 1, xbin))
    ax2.set_yticks(arange(0, 1, ybin))
    ax2.set_xlim(0,1)
    ax2.set_ylim(0,1)
    ax2.set_facecolor('black')
    ax2.grid(True)
    return gcf(), ax1, ax2, ax3
