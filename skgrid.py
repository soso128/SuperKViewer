from numpy import *
from matplotlib.pyplot import *
import matplotlib.gridspec as gridspec

sk_id_zmax = 1810
sk_id_zmin = -1810
sk_id_rad = 1690
height = sk_id_zmax - sk_id_zmin

def sk_mesh(rbin = 0.1, thetabin = pi/6, xbin = 0.1, ybin = 0.1, Nhist = 0, wratios = 0.3, hratios = 0.5):
    hx = 2 * sk_id_rad/1.15
    Ncol = 2 if Nhist > 0 else 1
    gs0 = gridspec.GridSpec(1, Ncol, width_ratios = [1, wratios] if Nhist else [1])
    gs = gridspec.GridSpecFromSubplotSpec(5, 3, height_ratios = [hx/height, 0.15 * hx/height, 1, 0.15 * hx/height, hx/height], width_ratios = [pi/2-0.5, 1, pi/2-0.5],subplot_spec = gs0[0], hspace = 0, wspace = 0.1)
    histos = None
    if Nhist > 0:
        gs2 = gridspec.GridSpecFromSubplotSpec(Nhist, 1, subplot_spec = gs0[1], wspace = hratios)
        histos = [subplot(g) for g in gs2]
    ax1 = subplot(gs[0:2, 1], projection = 'polar')
    ax1.set_rmax(1)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.set_thetagrids(arange(0, 2 * pi, thetabin) * 180/pi)
    ax1.set_rgrids(arange(0, 1, rbin))
    ax1.set_facecolor('black')
    ax3 = subplot(gs[3:, 1], projection = 'polar')
    ax3.set_rmax(1)
    ax3.set_xticklabels([])
    ax3.set_yticklabels([])
    ax3.set_thetagrids(arange(0, 2 * pi, thetabin) * 180/pi)
    ax3.set_rgrids(arange(0, 1, rbin))
    ax3.set_facecolor('black')
    ax2 = subplot(gs[2, :])
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
    histo_time = subplot(gs[4, -1])
    histo_charge = subplot(gs[4, 0])
    info = subplot(gs[0, 0])
    info.axis('off')
    info.text(0.5,0.5, 'SK run info')
    return {'figure': gcf(), 'top': ax1, 'barrel': ax2, 'bottom': ax3, 'time_histo': histo_time, 'charge_histo': histo_charge, 'info': info, 'histos': histos}

def grid_redraw(mesh, rbin = 0.1, thetabin = pi/6, xbin = 0.1, ybin = 0.1):
    ax1, ax2, ax3 = mesh['top'], mesh['barrel'], mesh['bottom']
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
    mesh['top'] = ax1
    mesh['barrel'] = ax2
    mesh['bottom'] = ax3
    return mesh
