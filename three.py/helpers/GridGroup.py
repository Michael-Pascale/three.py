class GridGroup(object):

    def __init__(self, sectors):
  
        super().__init__()
        self.sectors = sectors
        
    def remove_sector(self,key):
        self.sectors.pop(key,None)

    def add_sector(self, key, val):
        if key in self.sectors:
            return
        else:
            self.sectors[key] = val
