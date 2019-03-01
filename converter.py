from numpy import *
from skgrid import sk_id_zmax, sk_id_zmin, sk_id_rad
import pandas as pd

c_water = 21.58

def read_pmt_file(filename):
    f = genfromtxt(filename, skip_header = 50, dtype = int)
    f = f[:, (0, 14, 16, 17, 18)]
    p = pd.DataFrame(f, columns = ['cable', 'status', 'x', 'y', 'z'])
    return p

def cables_to_positions(hits, cables):
    positions = pd.merge(hits, cables, on=['cable'])
    positions = positions[positions['status'].isin([3,4])]
    return positions

def tof_subtract(positions, vertex):
    positions['tof'] = sqrt(sum((positions[xyz] - vertex[i])**2 for i, xyz in enumerate(['x', 'y', 'z'])))/c_water
    positions['tofsub'] = positions['time'] - positions['tof']
    return positions

def convert_xyz(pos):
    # Top
    if pos['z'] == sk_id_zmax:
        r = sqrt(pos['x']**2 + pos['y']**2)
        theta = arccos(pos['x']/r)
        if pos['y'] < 0: theta = -theta
        return (0, theta, r/sk_id_rad)
    # Bottom
    if pos['z'] == sk_id_zmin:
        r = sqrt(pos['x']**2 + pos['y']**2)
        theta = arccos(pos['x']/r)
        if pos['y'] < 0: theta = -theta
        return (2, theta, r/sk_id_rad)
    # Barrel
    if pos['z'] < sk_id_zmin or pos['z'] > sk_id_zmax:
        raise ValueError("PMT outside the detector, z = {}...Maybe OD?".format(pos['z']))
    theta = arctan(pos['x']/pos['y']) if pos['y'] != 0 else pi/2
    if pos['y'] < 0 and theta > 0: theta -= pi
    elif pos['y'] < 0 and theta < 0: theta += pi
    return (1, (theta + pi)/(2 * pi), (pos['z'] - sk_id_zmin)/(sk_id_zmax - sk_id_zmin))

def convert_positions_xyz(hits):
    converted_pos = hits.apply(lambda x: pd.Series(convert_xyz(x)), axis = 1)
    hits[['index', 'x2d', 'y2d']] = converted_pos
    return hits

def xmuon_to_xyzt(xmu, entry, direction):
    xyz = array(entry)[:3] + array(direction)/sqrt(sum(array(direction)**2)) * xmu
    return {'x': xyz[0], 'y': xyz[1], 'z': xyz[2], 'time': entry[3] + xmu/21.5}
