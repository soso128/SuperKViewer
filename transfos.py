from numpy import *

def time_integrate(cut_pos):
    new_pos = cut_pos.drop_duplicates(subset = ['cable']).reset_index(drop = True)
    del new_pos['time']
    new_pos['charge'] = cut_pos.groupby(['cable'], sort = False)['charge'].sum().reset_index(drop = True)
    return new_pos
