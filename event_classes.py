class Muon(object):
    def __init__(self):
        self.muboy_status = -1
        self.muboy_ntracks = 0
        self.muboy_goodness = 0
        self.muboy_dir = None
        self.muboy_dedx = None
        self.muboy_length = 0
        self.tracks = []

class Track(object):
    def __init__(self):
        self.muboy_entpos = None

class Bonsai(object):
    def __init__(self):
        self.vertex = None
        self.dir = None
        self.good = 0
        self.dirks = 100
        self.energy = -1
        self.cossun = 10
