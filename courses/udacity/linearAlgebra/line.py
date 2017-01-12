from decimal import Decimal, getcontext

from vector import Vector

import random

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension
            
            initial_index = Line.first_nonzero_index(n)
            '''
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)
            '''
        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)

    '''
    Two lines are parallel if their normal vectors are parallel.
    '''
    def is_parallel(self, line):
        return Vector(self.normal_vector).is_parallel(Vector(line.normal_vector))

    '''
    To check if two lines are equal, take a point on each line and calculate
    a direction vector.  If that vector is orthogonal to the normal vector for
    each of the two lines, then the vector lies on the line and the two lines
    are equal.
    '''
    def equals(self, line):
        x = random.randint(0,100)
        #dir_vec = [self.normal_vector[1], -1*self.normal_vector[0]]
        k = float(self.constant_term)
        A = self.normal_vector[0]
        B = self.normal_vector[1]
        y = (k-A*x)/B
        pt1 = Vector([x,y])

        x = random.randint(0,100)
        #dir_vec = [line.normal_vector[1], -1*line.normal_vector[0]]
        k = float(line.constant_term)
        A = line.normal_vector[0]
        B = line.normal_vector[1]
        y = (k-A*x)/B
        pt2 = Vector([x,y])

        vec = pt2-pt1

        return (vec.is_orthogonal(Vector(self.normal_vector)) \
                and vec.is_orthogonal(Vector(line.normal_vector)))
        
    '''
    If they are not parallel and not equal, they intersect.  Find the point of intersection
    using the formulas derived in the lecture
    '''
    def intersection(self, line):
        p = self.is_parallel(line)
        e = self.equals(line)
        if not p and not e:
            #calculate x and y using the derived formula in the lecture    
            A = self.normal_vector[0]
            B = self.normal_vector[1]
            C = line.normal_vector[0]
            D = line.normal_vector[1]
            k1 = float(self.constant_term)
            k2 = float(line.constant_term)

            x = (D*k1-B*k2)/(A*D-B*C)
            y = (-1*C*k1 + A*k2)/(A*D-B*C)
            return Vector([x,y]) 
        else:
            if p and e:
                return 'Inf'
            return None


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

# Ax+By=k
# normal_vector = [B,-A]
# constant_term = k
line1 = Line([1.,1.],constant_term=1)
line2 = Line([-3.,-3.], constant_term=-3)
print str(line1.equals(line2))
print line1.intersection(line2)

#Quiz
# 4.046x + 2.836y = 1.21
# 10.115x + 7.09y = 3.025
line1 = Line([4.046, 2.836], 1.21)
line2 = Line([10.115, 7.09], 3.025)
intx = line1.intersection(line2)
if type(intx) is str and intx=='Inf':
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', 'equal'])
elif type(intx) is Vector:
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', str(intx)])
else:
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', 'NO_INTERSECTION'])

print ''
# 7.204x + 3.182y = 8.68
# 8.172x + 4.114y = 9.883
line1 = Line([7.204, 3.182], 8.68)
line2 = Line([8.172, 4.114], 9.883)
intx = line1.intersection(line2)
if type(intx) is str and intx=='Inf':
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', 'equal'])
elif type(intx) is Vector:
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', str(intx)])
else:
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', 'NO_INTERSECTION'])

print ''
# 1.182x + 5.562y = 6.744
# 1.773x + 8.343y = 9.525
line1 = Line([1.182, 5.562], 6.744)
line2 = Line([1.773, 8.343], 9.525)
intx = line1.intersection(line2)
if type(intx) is str and intx=='Inf':
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', 'equal'])
elif type(intx) is Vector:
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', str(intx)])
else:
    print ''.join(['line1:',str(line1), ' line2:', str(line2), '::', 'NO_INTERSECTION'])
