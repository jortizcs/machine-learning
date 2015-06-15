import math

'''
experimental code to play with, following this tutorial: http://karpathy.github.io/neuralnets/

@author Jorge Ortiz (jortiz81@gmail.com)
'''

class Unit:
    def __init__(self, val, grad):
        self.value = val
        self.gradient = grad
        return

class multiplyGate:
    def __init__(self) :
        return

    def forward(self, u0, u1):
        self.unit0 = u0
        self.unit1 = u1
        v = self.unit0.value * self.unit1.value
        self.utop = Unit(v,0.0)
        return self.utop

    def backward(self):
        # set the gradients (1)
        new_grad0 = self.unit0.gradient + self.unit0.value * self.unit0.gradient
        self.unit0.gradient = new_grad0
        # set the gradients (2)
        new_grad1 = self.unit1.gradient + self.unit1.value * self.unit1.gradient
        self.unit1.gradient =new_grad1
        return

class addGate:
    def __init__(self):
        return

    def forward(self, u0, u1):
        self.unit0= u0
        self.unit1=u1
        self.utop = Unit(self.unit0.value + self.unit1.value, 0.0)
        return self.utop

    def backward(self):
        new_grad0 = self.unit0.gradient + 1 * self.utop.gradient
        new_grad1 = self.unit1.gradient + 1 * self.utop.gradient
        self.unit0.gradient=new_grad0
        self.unit1.gradient=new_grad1
        return

class sigmoidGate:
    def __init__(self):
        return

    def _sig(self, x):
        return 1 / (1+ math.exp(-x))

    def forward(self, u0):
        self.unit0 = u0
        self.utop = Unit(self._sig(self.unit0.value), 0.0)
        return self.utop

    def backward(self):
        s = self._sig(self.unit0.value)
        new_grad = self.unit0.gradient + (s * (1 - s)) * self.utop.gradient
        self.unit0.gradient=new_grad
        return
       
#define the forward pass
def forwardNeuron(mulg0, mulg1, addg0, addg1, sg0, a, b,c,x,y):
    ax = mulg0.forward(a,x)
    by = mulg1.forward(b,y)
    axpby = addg0.forward(ax,by)
    axpbypc = addg1.forward(axpby,c)
    return sg0.forward(axpbypc)

if __name__ == "__main__":

    # inputs to the nn
    a = Unit(1.0, 0.0)
    b = Unit(2.0, 0.0)
    c = Unit(-3.0, 0.0)
    x = Unit(-1.0, 0.0)
    y = Unit(3.0, 0.0)

    # gates
    mulg0 = multiplyGate()
    mulg1 = multiplyGate()
    addg0 = addGate()
    addg1 = addGate()
    sg0 = sigmoidGate()

    #run a forward pass and print it out
    s = forwardNeuron(mulg0, mulg1, addg0, addg1, sg0, a,b,c,x,y)
    print "circuit output: "  + str(s.value)
    for i in range(0,10):

        #run a backward pass 
        s.gradient = 1.0
        sg0.backward()
        addg1.backward()
        addg0.backward()
        mulg1.backward()
        mulg0.backward()
       
        # update the inputs and go forward 
        step_size = 0.01
        a.value += step_size * a.gradient
        b.value += step_size * b.gradient
        c.value += step_size * c.gradient
        x.value += step_size * x.gradient
        y.value += step_size * y.gradient

        s = forwardNeuron(mulg0, mulg1, addg0, addg1, sg0, a,b,c,x,y)
        print "circuit output: "  + str(s.value)
        print "====="
