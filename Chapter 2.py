#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''R-2.4 Write a Python class, Flower, that has three instance variables of type str,
int, and float, that respectively represent the name of the flower, its number
of petals, and its price. Your class must include a constructor method
that initializes each variable to an appropriate value, and your class should
include methods for setting the value of each type, and retrieving the value
of each type.'''

class Flower:
    
    def __init__(self,name,petal,price):
        self._name = name
        self._petal = petal
        self._price = price
    
    def set_name(self,name):
        self._name = name
    
    def set_petal(self,petal):
        self._petal = petal
    
    def set_price(self,price):
        self._price = price
    
    def get_name(self):
        return self._name
    
    def get_petal(self):
        return self._petal
    
    def get_price(self):
        return self._price

if __name__ == '__main__':
    rose = Flower('rose',16,10)
    print(rose.get_petal())
    print(rose.get_name())
    print(rose.get_price())
    rose.set_price(20)
    print(rose.get_price())


# In[9]:


'''R-2.5 Use the techniques of Section 1.7 to revise the charge and make payment
methods of the CreditCard class to ensure that the caller sends a number
as a parameter.'''

'''R-2.6 If the parameter to the make payment method of the CreditCard class
were a negative number, that would have the effect of raising the balance
on the account. Revise the implementation so that it raises a ValueError if
a negative value is sent.'''

'''R-2.7 The CreditCard class of Section 2.3 initializes the balance of a new account
to zero. Modify that class so that a new account can be given a
nonzero balance using an optional fifth parameter to the constructor. The
four-parameter constructor syntax should continue to produce an account
with zero balance.'''

class CreditCard:
    
    def __init__(self,customer,bank,account,limit,balance=0):
        self._customer = customer
        self._bank = bank
        self._account = account
        self._limit = limit
        self._balance = balance
    
    def get_customer(self):
        return self._customer
    
    def get_bank(self):
        return self._bank
    
    def get_account(self):
        return self._account
    
    def get_limit(self):
        return self._limit
    
    def get_balance(self):
        return self._balance
    
    def charge(self,price):
        if not isinstance(price,(int,float)):
            raise TypeError('what you enter should be numeric')
        else:
            if self._balance + price > self._limit:
                print('charge denied')
                return False
            else:
                self._balance =+ price
                print('chaege approved')
                return True
    
    def make_payment(self,amount):
        if not isinstance(amount,(int,float)):
            raise TypeError('what you enter should be numeric')
        else:
            if amount < 0:
                raise ValueError("the amount of payment shouldn't be negtive")
            else:
                self._balance -= amount

if __name__ == '__main__':
    card_one = CreditCard('Alan','BOA','20190820',1000)
    print('The card is issued by:',card_one.get_bank())
    print('The current balance is:',card_one.get_balance())
    card_one.charge(200)
    print('The current balance is:',card_one.get_balance())
    card_one.make_payment(100)
    print('The current balance is:',card_one.get_balance())


# In[27]:


'''R-2.9 Implement the sub method for the Vector class of Section 2.3.3, so
that the expression u−v returns a new vector instance representing the
difference between two vectors.'''

'''R-2.10 Implement the neg method for the Vector class of Section 2.3.3, so
that the expression −v returns a new vector instance whose coordinates
are all the negated values of the respective coordinates of v.'''

'''R-2.11 In Section 2.3.3, we note that our Vector class supports a syntax such as
v = u + [5, 3, 10, −2, 1], in which the sum of a vector and list returns
a new vector. However, the syntax v = [5, 3, 10, −2, 1] + u is illegal.
Explain how the Vector class definition can be revised so that this syntax
generates a new vector.'''

'''R-2.12 Implement the mul method for the Vector class of Section 2.3.3, so
that the expression v*3 returns a new vector with coordinates that are 3
times the respective coordinates of v.'''

'''R-2.13 Exercise R-2.12 asks for an implementation of mul , for the Vector
class of Section 2.3.3, to provide support for the syntax v*3. Implement
the rmul method, to provide additional support for syntax 3*v.'''

'''R-2.14 Implement the mul method for the Vector class of Section 2.3.3, so
that the expression u v returns a scalar that represents the dot product of
the vectors'''

'''R-2.15 The Vector class of Section 2.3.3 provides a constructor that takes an integer
d, and produces a d-dimensional vector with all coordinates equal to
0. Another convenient form for creating a new vector would be to send the
constructor a parameter that is some iterable type representing a sequence
of numbers, and to create a vector with dimension equal to the length of
that sequence and coordinates equal to the sequence values. For example,
Vector([4, 7, 5]) would produce a three-dimensional vector with coordinates
<4, 7, 5>. Modify the constructor so that either of these forms is
acceptable; that is, if a single integer is sent, it produces a vector of that
dimension with all zeros, but if a sequence of numbers is provided, it produces
a vector with coordinates based on that sequence.'''

class Vector:
    
    def __init__(self,n):
        if isinstance(n,int):
            self._coords = [0] * n
        if isinstance(n,(list,set,str,tuple)):
            self._coords = []
            for i in range(len(n)):
                self._coords.append(float(n[i]))
    
    def __len__(self):
        return len(self._coords)
    
    def __getitem__(self,i):
        return self._coords[i]
    
    def __setitem__(self,i,value):
        self._coords[i] = value
    
    def __add__(self,b):
        if len(self) != len(b):
            raise ValueError('dimensions must agree')
        result = Vector(len(self))
        for i in range(len(self)):
            result[i] = self[i] + b[i]
        return result
    
    def __radd__(self,b):
        if len(self) != len(b):
            raise ValueError('dimensions must agree')
        result = Vector(len(self))
        for i in range(len(self)):
            result[i] = self[i] + b[i]
        return result
    
    def __sub__(self,b):
        if len(self) != len(b):
            raise ValueError('dimensions must agree')
        result = Vector(len(self))
        for i in range(len(self)):
            result[i] = self[i] - b[i]
        return result
    
    def __neg__(self):
        result = Vector(len(self))
        for i in range(len(self)):
            result[i] = - self[i]
        return result
    
    def __mul__(self,factor):
        if isinstance(factor,(int,float)):
            result = Vector(len(self))
            result._coords = [self[i] * factor for i in range(len(self))]
            return result
        else:
            if len(self) != len(factor):
                raise ValueError('dimensions must agree')
            dot = 0
            for i in range(len(self)):
                dot += self[i] * factor[i]
            return dot
    
    def __rmul__(self,factor):
        if isinstance(factor,(int,float)):
            result = Vector(len(self))
            result._coords = [self[i] * factor for i in range(len(self))]
            return result
        else:
            if len(self) != len(factor):
                raise ValueError('dimensions must agree')
            dot = 0
            for i in range(len(self)):
                dot += self[i] * factor[i]
            return dot
    
    def __str__(self):
        return '<' + str(self._coords)[1:-1] + '>'

if __name__ == '__main__':
    a = Vector(5)
    b = Vector(5)
    a = a + [1,2,3,4,5]
    b = b + [-1,-2,3,4,5]
    print('vector a is',str(a))
    print('vector a+b is',str(a+b))
    print('vector b-a is',str(b-a))
    print('vector -a is',str(-a))
    c = Vector(5)
    c = [4,5,6,7,8] + c
    print('vector c is',str(c))
    d = c * 3
    print('vector d is',d)  
    e = 3 * c
    print('vector e is',e)
    print('vector a*c is',a*c)
    f = e * [1,2,3,4,5]
    print('vector e*[1,2,3,4,5] is',f)
    g = [1,2,3,4,5] * e
    print('vector [1,2,3,4,5]*e is',g)
    h = Vector('12345')
    i = Vector([3,4,1,-1,2.3])
    print('vector h is',h)
    print('vector i is',i)


# In[53]:


class Progression:
    
    def __init__(self,start=0):
        self._current = start
    
    def _advance(self):
        self._current = self._current + 1
    
    def __next__(self):
        if self._current is None:
            raise StopIteration()
        else:
            get_result = self._current
            self._advance()
            return get_result
    
    def __iter__(self):
        return self
    
    def print_progression(self,n):
        print([next(self) for i in range(n)])
    
    def get_nth(self,n):
        return [next(self) for i in range(n)][-1]

class ArithmeticProgression(Progression):
    
    def __init__(self,start=0,increment=1):
        super().__init__(start)
        self._increment = increment
    
    def _advance(self):
        self._current = self._current + self._increment

class GeometricProgression(Progression):
    
    def __init__(self,start=1,base=2):
        super().__init__(start)
        self._base = base
    
    def _advance(self):
        self._current = self._current * self._base

class FibonacciProgression(Progression):
    
    def __init__(self,start=0,second=1):
        super().__init__(start)
        self._difference = second - self._current
    
    def _advance(self):
        self._current,self._difference = self._difference + self._current,self._current

'''R-2.18 Give a short fragment of Python code that uses the progression classes
from Section 2.4.2 to find the 8th value of a Fibonacci progression that
starts with 2 and 2 as its first two values.'''

a = FibonacciProgression(2,2)
print(a.get_nth(8))

'''R-2.19 When using the ArithmeticProgression class of Section 2.4.2 with an increment
of 128 and a start of 0, how many calls to next can we make
before we reach an integer of 2**63 or larger?'''

# 2**56-1 times


# In[58]:


'''C-2.26 The SequenceIterator class of Section 2.3.4 provides what is known as a
forward iterator. Implement a class named ReversedSequenceIterator that
serves as a reverse iterator for any Python sequence type. The first call to
next should return the last element of the sequence, the second call to next
should return the second-to-last element, and so forth.'''

class SequenceIterator:
    
    def __init__(self,seq):
        self._seq = seq
        self._k = -1
    
    def __next__(self):
        self._k = self._k + 1
        if self._k < len(self._seq):
            return (self._seq[self._k])
        else:
            raise StopIteration()
    
    def __iter__(self):
        return self


class ReversedSequenceIterator_1:
    
    def __init__(self,seq):
        self._seq = seq
        self._k = 0
    
    def __next__(self):
        self._k = self._k - 1
        if self._k >= -len(self._seq):
            return (self._seq[self._k])
        else:
            raise StopIteration()
    
    def __iter__(self):
        return self
    
class ReversedSequenceIterator_2(SequenceIterator):
    
    def __init__(self,seq):
        super().__init__(seq)
        
    def __next__(self):
        self._k = self._k - 1
        if self._k +1 >= -len(self._seq):
            return (self._seq[self._k+1])
        else:
            raise StopIteration()

a = ReversedSequenceIterator_1([1,2,3,4,5])
print([num for num in a])

b = ReversedSequenceIterator_2([1,2,3,4,5])
print([num for num in b])

