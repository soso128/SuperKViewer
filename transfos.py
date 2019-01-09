from numpy import *

def time_integrate(cut_pos):
    new_pos = cut_pos.drop_duplicates(subset = ['cable'])
    del new_pos['time']
    new_pos['charge'] = cut_pos.groupby(['cable'], sort = 'False')['charge'].sum()
    return new_pos
