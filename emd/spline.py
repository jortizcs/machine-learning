class Curve(object):
    def __init__(self, coeffs, y):
        self.coeffs = coeffs
        self.y = y
        return

    def derivative(self):
        new_curve=None
        order = len(self.coeffs)
        
        d_coeffs = [
        return new_curve 
