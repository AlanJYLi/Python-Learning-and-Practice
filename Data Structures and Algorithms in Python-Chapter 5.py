#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''R-5.1 Execute the experiment from Code Fragment 5.1 and compare the results
on your system to those we report in Code Fragment 5.2.'''

import sys

data = []

for i in range(30):
    l = len(data)
    s = sys.getsizeof(data)
    print('length: {0:3d};  size: {1:4d}\n'.format(l,s))
    data.append(None)    


# In[4]:


'''R-5.2 In Code Fragment 5.1, we perform an experiment to compare the length of
a Python list to its underlying memory usage. Determining the sequence
of array sizes requires a manual inspection of the output of that program.
Redesign the experiment so that the program outputs only those values of
k at which the existing capacity is exhausted. For example, on a system
consistent with the results of Code Fragment 5.2, your program should
output that the sequence of array capacities are 0, 4, 8, 16, 25, . . . .'''



data=[]

s_store = sys.getsizeof(data)

for i in range(1,30):
    data.append(None)
    s = sys.getsizeof(data)
    if s > s_store:
        print(i-1)
        s_store = s


# In[5]:


'''R-5.3 Modify the experiment from Code Fragment 5.1 in order to demonstrate
that Python’s list class occasionally shrinks the size of its underlying array
when elements are popped from a list.'''

data = [None]*30

for i in range(30):
    l = len(data)
    s = sys.getsizeof(data)
    print('length: {0:3d}; size: {1:4d}\n'.format(l,s))
    data.pop()


# In[22]:


'''R-5.4 Our DynamicArray class, as given in Code Fragment 5.3, does not support
use of negative indices with getitem . Update that method to better
match the semantics of a Python list.'''

'''R-5.6 Our implementation of insert for the DynamicArray class, as given in
Code Fragment 5.5, has the following inefficiency. In the case when a resize
occurs, the resize operation takes time to copy all the elements from
an old array to a new array, and then the subsequent loop in the body of
insert shifts many of those elements. Give an improved implementation
of the insert method, so that, in the case of a resize, the elements are
shifted into their final position during that operation, thereby avoiding the
subsequent shifting.'''

import ctypes

class DynamicArray:

    def __init__ (self):
        '''Create an empty array.'''
        self._n = 0
        self._capacity = 1
        self._A = self._make_array(self._capacity)

    def _make_array(self, c):
        '''Return new array with capacity c.'''
        return (c*ctypes.py_object)( )

    def __len__(self):
        '''Return number of elements stored in the array.'''
        return self._n

    def __getitem__ (self, k):
        '''Return element at index k.'''
        if not (-self._n <= k < self._n):
            raise IndexError('invalid index')
        if k >= 0:
            return self._A[k]
        else:
            return self._A[self._n + k]

    def append(self, obj):
        '''Add object to end of the array.'''
        if self._n == self._capacity: 
            self._resize(2*self._capacity)
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):
        '''Resize internal array to capacity c.'''
        B = self._make_array(c) # new (bigger) array
        for k in range(self._n): # for each existing value
            B[k] = self._A[k]
        self._A = B # use the bigger array
        self._capacity = c
        
    def insert(self, k, value):
        '''Insert value at index k, shifting subsequent values rightward.'''
        if not (-self._n <= k < self._n):
            raise IndexError('invalid index')
        if k < 0:
            k = self._n + k
        if self._n == self._capacity: # not enough room
            B = self._make_array(2*self._capacity) # new (bigger) array
            for j in range(self._n, k, -1):
                B[j] = self._A[j-1]
            B[k] = value
            for j in range(k):
                B[j] = self._A[j]
            self._A = B
            self._capacity = 2*self._capacity
        else:
            for j in range(self._n, k, -1): # shift rightmost first
                self._A[j] = self._A[j-1]
            self._A[k] = value # store newest element
            self._n += 1

    
    
new = DynamicArray()
print(len(new))
new.append(1)
new.append(2)
new.append(3)
new[-1]

new.insert(2, 10)
new.insert(-3, 10)
new.insert(2, 10)
new.insert(2, 10)
new.insert(2, 10)
for i in range(len(new)):
    print(new[i])


# In[27]:


'''R-5.7 Let A be an array of size n ≥ 2 containing integers from 1 to n−1, inclusive,
with exactly one repeated. Describe a fast algorithm for finding the
integer in A that is repeated.'''

def findrepeat(l):
    if len(l) <= 1:
        return 'No repeated number'
    while len(l) >= 2:
        num = l.pop()
        if num in l:
            return num

a=[1]
b=[1,1]
c=[2,1,2]
d=[2,2,3,1]

print(findrepeat(a))
print(findrepeat(b))
print(findrepeat(c))
print(findrepeat(d))


# In[35]:


'''C-5.14 The shuffle method, supported by the random module, takes a Python
list and rearranges it so that every possible ordering is equally likely.
Implement your own version of such a function. You may rely on the
randrange(n) function of the random module, which returns a random
number between 0 and n−1 inclusive.'''

import random

def shufflelist(l):
    if len(l) == 0:
        return "empty list"
    if len(l) == 1:
        return l
    new = []
    while len(l) > 0:
        randindex = random.randrange(len(l))
        new.append(l[randindex])
        l.pop(randindex)
    return new

a=[1]
b=[1,2,3,4,5,6,7]
c=["alan", "mary", "bob", "tom"]
print(shufflelist(a))
print(shufflelist(b))
print(shufflelist(c))

for i in range(10):
    print(shufflelist(c))
    
'''It's not a good solution upon. As when the function is called once, the original list becomes empty.'''

def shufflelist2(l):
    if len(l) == 0:
        return "empty list"
    if len(l) == 1:
        return l
    for i in range(len(l)):
        randindex = random.randrange(len(l)-i)
        value = l[randindex]
        l.pop(randindex)
        l.append(value)
    return l

c=["alan", "mary", "bob", "tom"]

for i in range(10):
    print(shufflelist2(c))


# In[ ]:




