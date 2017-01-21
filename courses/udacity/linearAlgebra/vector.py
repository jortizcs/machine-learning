import math
from decimal import Decimal, getcontext
getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates myst be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        if self.dimension != v.dimension:
            raise ValueError('Vector must be the same length')
        #sum_ = []
        #for i in range(self.dimension):
        #    sum_.append(self.coordinates[i]+v.coordinates[i])
        sum_ = [x+y for x,y in zip(self.coordinates,v.coordinates)]
        return Vector(sum_)

    def __sub__(self, v):
        if self.dimension != v.dimension:
            raise ValueError('Vector must be the same length')
        m = v*-1
        return m+self

    def __mul__(self, f):
        #s_ = []
        #for i in range(self.dimension):
        #    s_.append(f*self.coordinates[i])
        s_ = [f*x for x in self.coordinates]
        return Vector(s_)

    def magnitude(self):
        #for x in self.coordinates:
        #    print x
        return math.sqrt(sum([float(x)**2 for x in self.coordinates]))

    def normalize(self):
        if self.magnitude()==0:
            return 0
        return self*(1/self.magnitude())

    def dot(self, x):
        return sum([float(x)*float(y) for x,y in zip(x.coordinates, self.coordinates)])

    def angle_rads(self, x):
        mag_x = x.magnitude()
        mag_y = self.magnitude()
        if mag_x == 0 or mag_y==0:
            raise ValueError('magnitude or x or self is 0')
        #print type(self.dot(x))
        #print type(mag_x)
        #print type(mag_y)
        #print self.dot(x)/(mag_x*mag_y)
        v = self.dot(x)/(mag_x*mag_y)
        v = float("{0:.3f}".format(v))
        return math.acos(v)

    def angle_deg(self, x):
        return math.degrees(self.angle_rads(x))
    
    def is_zero(self):
        return self.magnitude()<1e-10

    def is_parallel(self, x):
        if x.magnitude()==0 or self.magnitude()==0:
            return True
        res = self.angle_deg(x)
        #print res
        if res==180 or res==0 or res<=1e-10:
            return True
        return False

    def is_orthogonal(self, x):
        if x.magnitude()==0 or self.magnitude()==0:
            return True
        res = self.dot(x)
        #print "ortho:" + str(res)
        if res==0 or abs(res)<1e-10:
            return True
        return False

    def proj(self,b):
        b_norm = b.normalize()
        return b_norm*self.dot(b_norm)

    def perp(self, b):
        v_parallel = self.proj(b)
        return self-v_parallel

    def cross(self, w):
        if self.dimension ==3 and w.dimension==3:
            v=self
            new_vec = Vector([(v.coordinates[1]*w.coordinates[2])-(v.coordinates[2]*w.coordinates[1]),\
                        -1*((v.coordinates[0]*w.coordinates[2])-(v.coordinates[2]*w.coordinates[0])),\
                        (v.coordinates[0]*w.coordinates[1])-(v.coordinates[1]*w.coordinates[0])])
            return new_vec
        return None

    def parallelogram_area(self, w):
        theta = self.angle_rads(w)
        if abs(theta)<1e-10:
            theta=0
        return (self.magnitude()*w.magnitude())*math.sin(theta)

    def parallelogram_area2(self, w):
        return self.cross(w).magnitude()

    def triangle_area(self, w):
        return 0.5*self.parallelogram_area(w)
'''
# Quiz
v1 = Vector([8.218,-9.341])
v2 = Vector([-1.129,2.111])
print v1+v2
v3 = Vector([7.119,8.215])
v4 = Vector([-8.223,0.878])
print v3-v4

f = 7.41
v5=Vector([1.671, -1.012, -0.318])
print v5*f

print '\nMagnitude and normalization'
v6 = Vector([-0.221,7.437])
print v6
print 'magnitude: ' + str(v6.magnitude())

v7=Vector([8.813,-1.331,-6.247])
print v7
print 'magnitude: ' + str(v7.magnitude())

v8 = Vector([5.581,-2.136])
print v8
print v8.normalize()
v9=Vector([1.996,3.108,-4.554])
print v9
print v9.normalize()


# Coding Dot product and angle
print '\n\nCoding Dot product and angle'
v10=Vector([7.887,4.138])
v11=Vector([-8.802,6.776])
print v10
print v11
print 'dot: ' + str(v10.dot(v11))

v12 = Vector([-5.955,-4.904, -1.874])
v13 = Vector([-4.496,-8.755, 7.103])
print '\n'
print v12
print v13
print 'dot: ' + str(v12.dot(v13))

v14=Vector([3.183,-7.627])
v15=Vector([-2.668, 5.319])
print '\n'
print v14
print v15
print v14.angle_rads(v15)

v16=Vector([7.35,0.221, 5.188])
v17=Vector([2.751,8.259, 3.985])
print '\n'
print v16
print v17
print v16.angle_deg(v17)

# Parellelism and Orthogonality
print '\n\n\n############# Parellelism and Orthogonality'

v18=Vector([-7.579,-7.88])
v19=Vector([22.737,23.64])
print v18
print v19
print 'parallel? ' + str(v18.is_parallel(v19))
print 'orthogonal? ' + str(v18.is_orthogonal(v19)) + '\n'

v20=Vector([-2.029,9.97, 4.172])
v21=Vector([-9.231, -6.639, -7.245])
print v20
print v21
print 'parallel? ' + str(v20.is_parallel(v21))
print 'orthogonal? ' + str(v20.is_orthogonal(v21)) + '\n'

v22=Vector([-2.328, -7.284, -1.214])
v23=Vector([-1.821, 1.072, -2.94])
print v22
print v23
print 'parallel? ' + str(v22.is_parallel(v23))
print 'orthogonal? ' + str(v22.is_orthogonal(v23)) + '\n'

v24=Vector([2.118,4.827])
v25=Vector([0.0,0.0])
print v24
print v25
print 'parallel? ' + str(v24.is_parallel(v25))
print 'orthogonal? ' + str(v24.is_orthogonal(v25)) + '\n'

print '\n\n#####  Projections  #####'
v26 = Vector([3.039, 1.879])
v27 = Vector([0.825, 2.036])
print v26
print v27
print v26.proj(v27)

v28=Vector([-9.88, -3.264, -8.159])
v29=Vector([-2.155, -9.353, -9.473])
print ''
print v28
print v29
print v28.perp(v29)

v30=Vector([3.009, -6.172, 3.692, -2.51])
v31=Vector([6.404, -9.144, 2.759, 8.718])
print ''
print v30
print v31
print v30.proj(v31)
print v30.perp(v31)
print v30.proj(v31)+v30.perp(v31)
print v30.proj(v31).is_parallel(v31)
print v30.perp(v31).is_orthogonal(v31)

# Cross product
print ''
print  '########### Cross product #######\n'
v32=Vector([8.462, 7.893, -8.187])
v33=Vector([6.984, -5.975, 4.778])
print v32.cross(v33)
print v32.cross(v33).is_orthogonal(v32)
print v32.cross(v33).is_orthogonal(v33)
print v32.parallelogram_area(v33)
print v32.parallelogram_area2(v33)

print ''
v34 = Vector([-8.987, -9.838, 5.031])
v35 = Vector([-4.268, -1.861, -8.866])
print v34.parallelogram_area(v35)

print ''
v36 = Vector([1.5, 9.547, 3.691])
v37 = Vector([-6.007, 0.124, 5.772])
print v36.triangle_area(v37)
'''
