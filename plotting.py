from numpy import *
from matplotlib.pyplot import *
import skgrid as sk
import transfos

def plot_positions(converted_pos, mesh, emax = 15, cmap = cm.viridis, iscolor = True):
    grouped = converted_pos.groupby('index')
    points = []
    for i, b in enumerate(['top', 'barrel', 'bottom']):
        part = grouped.get_index(i)
        points.append(part.scatter(x = 'x2d', y = 'y2d', ax = mesh['b'], cmap = cmap, c = None if g.shape[1] < 3  or not iscolor else g[:, 3]/emax, vmin = 0, vmax = 1))
    grid_redraw(mesh)
    return points

def plot_time_slice(converted_pos, mesh, tmin, tmax, thist_min = 0, thist_max = 1300, tbin = 5, emax = 15, cmap = cm.viridis, iscolor = True):
    converted_pos = converted_pos[(converted_pos['time'] > tmin) & (converted_pos['time'] < tmax)]
    integrated_pos = tf.time_integrate(converted_pos)
    points = plot_positions(integrated_pos, mesh, emax = emax, cmap = cmap, iscolor = True)
    hist = converted_pos.hist(column = 'time', weights = converted_pos['charge'], bins = arange(thist_min, thist_max + tbin, tbin), ax = mesh['time_histo'])
    mesh['time_histo'].xlabel('Time (ns)')
    mesh['time_histo'].ylabel('Q')
    tslice = mesh['time_histo'].axvspan(tmin, tmax, alpha = 0.5, color = 'r')
    return points, hist, tslice
