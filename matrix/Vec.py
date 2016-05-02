class Vec:
    def __init__(self, labels, function):
        self.D= labels
        self.f = function
    
    def setitem(self, d, val):
        self.f[d]=val

    def getitem(self,d):
        if d in self.f:
            return self.f[d]
        return 0

    def scalar_mul(self, alpha):
        for d in self.D:
            self.f[d] = self.getitem(d)*alpha

    def add(self, u):
        return Vec(self.D,{d:self.getitem(d)+u.getitem(d) for d in self.D})
