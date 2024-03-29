from numpy import *
from matplotlib.pyplot import *
import matplotlib.gridspec as gridspec
from itertools import groupby

sk_id_zmax = 1810
sk_id_zmin = -1810
sk_id_rad = 1690

def sk_mesh(rbin = 0.1, thetabin = pi/6, xbin = 0.1, ybin = 0.1):
    gs0 = gridspec.GridSpec(1, 2, width_ratios = [1, 0.3])
    gs = gridspec.GridSpecFromSubplotSpec(3, 1, height_ratios = [1, (sk_id_zmax - sk_id_zmin)/(2 * sk_id_rad), 1], subplot_spec = gs0[0], hspace = 0)
    gs2 = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec = gs0[1], wspace = 0.5)
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
    #gcf().subplots_adjust(hspace = 0)
    hx1 = subplot(gs2[0])
    hx2 = subplot(gs2[1])
    return gcf(), ax1, ax2, ax3, hx1, hx2

def grid_redraw(mesh, rbin = 0.1, thetabin = pi/6, xbin = 0.1, ybin = 0.1):
    fig, ax1, ax2, ax3, hx1, hx2 = mesh
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

def convert_xyz(pos):
    # Top
    if pos[2] == sk_id_zmax:
        r = sqrt(pos[0]**2 + pos[1]**2)
        theta = arccos(pos[0]/r)
        if pos[1] < 0: theta = -theta
        return (0, theta * 180/pi, r/sk_id_rad) + tuple(pos[3:])
    # Bottom
    if pos[2] == sk_id_zmin:
        r = sqrt(pos[0]**2 + pos[1]**2)
        theta = arccos(pos[0]/r)
        if pos[1] < 0: theta = -theta
        return (2, theta * 180/pi, r/sk_id_rad) + tuple(pos[3:])
    # Barrel
    if pos[2] < sk_id_zmin or pos[2] > sk_id_zmax:
        raise ValueError("PMT outside the detector, z = {}...Maybe OD?".format(pos[2]))
    theta = arctan(pos[0]/pos[1]) if pos[1] != 0 else pi/2
    if pos[1] < 0 and theta > 0: theta -= pi
    elif pos[1] < 0 and theta < 0: theta += pi
    return (1, (theta + pi)/(2 * pi), (pos[2] - sk_id_zmin)/(sk_id_zmax - sk_id_zmin)) + tuple(pos[3:])

def plot_positions(converted_pos, mesh, emax = 15, cmap = cm.viridis, iscolor = True):
    converted_pos = sorted(array(converted_pos), key = lambda x: x[0])
    points = [None, None, None]
    for k, g in groupby(converted_pos, lambda x: x[0]):
        g = array(list(g))
        if k == 0 or k == 2:
            print(g[:, 2])
        points[int(k)] = mesh[int(k) + 1].scatter(g[:, 1], g[:, 2], cmap = cmap, c = None if g.shape[1] < 3  or not iscolor else g[:, 3]/emax, vmin = 0, vmax = 1)
        mesh[int(k) + 1].grid(True)
    grid_redraw(mesh)
    return points

def read_pmt_file(filename):
    f = genfromtxt(filename, skip_header = 50, dtype = int)
    f = f[:, (0, 14, 16, 17, 18)]
    return f

def cables_to_positions(hits, cables):
    hits = array(hits)
    cable_hits = array([cables[cables[:, 0] == (int(c) & (2**16 - 1))][0, 1:] for c in hits[:, 0]])
    hits = hits[(cable_hits[:, 0] == 3) | (cable_hits[:, 0] == 4)]
    cable_hits = cable_hits[(cable_hits[:, 0] == 3) | (cable_hits[:, 0] == 4)][:, 1:]
    return column_stack((cable_hits[:, 0], cable_hits[:, 1], cable_hits[:, 2], hits[:, 1], hits[:, 2]))

def get_root_tree(rootfile):
    import ROOT as r
    from glob import glob
    libs = glob("/home/elhedri/skofl/lib/*.so")
    for ll in libs:
        r.gSystem.Load(ll)
    f = r.TFile.Open(rootfile)
    tr = f.Get("data")
    return tr

def event_to_cables(event):
    cables = event.TQREAL.cables
    times = event.TQREAL.T
    charges = event.TQREAL.Q
    nhits = event.TQREAL.nhits
    res = [[cables[i], charges[i], times[i]] for i in range(nhits)]
    return res

def anim_time(converted_pos, mesh, time_bin, tmin = None, tmax = None, emax = 15, cmap = cm.viridis, iscolor = True):
    bins = arange(tmin if tmin else converted_pos[:, -1].min(), tmax if tmax else converted_pos[:, -1].max(), time_bin)
    bin_indices = digitize(converted_pos[:, -1], bins)
    cv_times = [converted_pos[bin_indices == i + 1] for i in range(bin_indices.max())]
    for cv in cv_times:
        if cv is not None:
            points = plot_positions(cv, mesh, emax = emax, cmap = cmap, iscolor = iscolor)
            pause(0.05)
            input("Press Enter to continue...")
            for i in range(3): 
                if points[i] is not None: points[i].remove()
