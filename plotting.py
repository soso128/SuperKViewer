from numpy import *
from matplotlib.pyplot import *
import skgrid as sk
import transfos as tf

def plot_positions(converted_pos, mesh, emax = 15, cmap = cm.viridis, iscolor = True):
    grouped = converted_pos.groupby('index')
    points = []
    cb = None
    for i, b in enumerate(['top', 'barrel', 'bottom']):
        if i in converted_pos['index'].values:
            part = grouped.get_group(i)
            #print(part[['x2d', 'y2d']])
            points.append(part.plot.scatter(x = 'x2d', y = 'y2d', ax = mesh[b], cmap = cmap, c = None if part.shape[1] < 3  or not iscolor else part['charge'], vmin = 0, vmax = emax, colorbar = False, s = 1))
            if iscolor and b == 'barrel':
                cb = colorbar(points[-1].findobj()[0], ax = mesh['barrel'])
            points[-1].set_xlabel('')
            points[-1].set_ylabel('')
    sk.grid_redraw(mesh)
    return points, cb

def plot_time_slice(converted_pos, mesh, tmin, tmax, thist_min = 0, thist_max = 1300, tbin = 5, emax = 15, cmap = cm.viridis, iscolor = True):
    cut_pos = converted_pos[(converted_pos['time'] > tmin) & (converted_pos['time'] < tmax)]
    print(len(cut_pos))
    integrated_pos = tf.time_integrate(cut_pos)
    hist_time = converted_pos.hist(column = 'time', weights = converted_pos['charge'], bins = arange(thist_min, thist_max + tbin, tbin), ax = mesh['time_histo'])
    hist_charge = integrated_pos.hist(column = 'charge', bins = 40, ax = mesh['charge_histo'])
    points, cb = plot_positions(integrated_pos, mesh, emax = emax, cmap = cmap, iscolor = True)
    mesh['time_histo'].set_xlabel('Time (ns)')
    mesh['time_histo'].set_ylabel('Q')
    mesh['time_histo'].set_title('')
    mesh['charge_histo'].set_xlabel('Q')
    mesh['charge_histo'].set_ylabel('Number of PMTs')
    mesh['charge_histo'].set_title('')
    tslice = mesh['time_histo'].axvspan(tmin, tmax, alpha = 0.5, color = 'r')
    return points, hist_time, tslice, hist_charge, cb

def clear_plots(mesh, cb = None):
    for k in ['top', 'bottom', 'barrel']:
        mesh[k].findobj()[0].remove()
    mesh['time_histo'].clear()
    mesh['charge_histo'].clear()
    mesh['info'].clear()
    mesh['info'].axis('off')
    if cb:
        try: cb.remove()
        except AttributeError: pass
