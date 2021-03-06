#!/usr/bin/env python
# coding: utf-8

# In[2]:


''' R-1.1 Write a short Python function, is_multiple(n, m), 
    that takes two integer values and returns True if n is a multiple of m, 
    that is, n = mi for some integer i, and False otherwise.'''

def is_multiple(n,m):
    return n % m == 0

test1 = is_multiple(10,2)
test2 = is_multiple(10,3)

print(test1)
print(test2)


# In[12]:


'''R-1.2 Write a short Python function, is even(k), that takes an integer value and
returns True if k is even, and False otherwise. However, your function
cannot use the multiplication, modulo, or division operators.'''

# bit operation -->  https://wiki.python.org/moin/BitwiseOperators

def even(k):
    return k & 1 == 0

test1 = even(50)
test2 = even(101)

print(test1)
print(test2)


# In[6]:


'''R-1.3 Write a short Python function, minmax(data), that takes a sequence of
one or more numbers, and returns the smallest and largest numbers, in the
form of a tuple of length two. Do not use the built-in functions min or
max in implementing your solution.'''

def minmax(data):
    small = data[0]
    large = data[0]
    if len(data) == 1:
        return small,large
    for num in data[1:]:
        if num < small:
            small = num
        if num > large:
            large = num
    return small,large

test1 = minmax([2])
test2 = minmax([2,3,4,5,1,3,2,7,10,7])

print(test1)
print(test2)


# In[13]:


'''R-1.4 Write a short Python function that takes a positive integer n and returns
the sum of the squares of all the positive integers smaller than n.'''

def sum_squares_1(n):
    total = 0
    for i in range(1,n):
        total = total + i ** 2
    return total

test1 = sum_squares_1(3)
test2 = sum_squares_1(10)

print(test1)
print(test2)

'''R-1.5 Give a single command that computes the sum from Exercise R-1.4, relying
on Python’s comprehension syntax and the built-in sum function.'''

def sum_squares_2(n):
    return sum([k*k for k in range(1,n)])

test1 = sum_squares_2(3)
test2 = sum_squares_2(10)

print(test1)
print(test2)

'''R-1.6 Write a short Python function that takes a positive integer n and returns
the sum of the squares of all the odd positive integers smaller than n.'''

'''R-1.7 Give a single command that computes the sum from Exercise R-1.6, relying
on Python’s comprehension syntax and the built-in sum function.'''

def sum_squares_3(n):
    return sum([k*k for k in range(1,n,2)])

test1 = sum_squares_3(3)
test2 = sum_squares_3(10)

print(test1)
print(test2)


# In[17]:


'''R-1.8 Python allows negative integers to be used as indices into a sequence,
such as a string. If string s has length n, and expression s[k] is used for index
−n≤k<0, what is the equivalent index j ≥0 such that s[j] references
the same element?'''

def test(test_string,k):
    if k < 0 and k >= -len(test_string):
        j = len(test_string) + k
        return test_string[k] == test_string[j]
    else:
        return 'k is out of range!'

test1 = test('abcdefghijklmn',-6)
test2 = test('abcdefghijklmn',-20)

print(test1)
print(test2)


# In[24]:


'''R-1.9 What parameters should be sent to the range constructor, to produce a
range with values 50, 60, 70, 80?'''

print(list(range(50,81,10)))

'''R-1.10 What parameters should be sent to the range constructor, to produce a
range with values 8, 6, 4, 2, 0, −2, −4, −6, −8?'''

print(list(range(8,-9,-2)))


# In[26]:


'''R-1.11 Demonstrate how to use Python’s list comprehension syntax to produce
the list [1, 2, 4, 8, 16, 32, 64, 128, 256].'''

[2 ** i for i in range(9)]


# In[28]:


'''R-1.12 Python’s random module includes a function choice(data) that returns a
random element from a non-empty sequence. The random module includes
a more basic function randrange, with parameterization similar to
the built-in range function, that return a random choice from the given
range. Using only the randrange function, implement your own version
of the choice function.'''

from random import randrange

def choice_function(data):
    return data[randrange(0,len(data))]

test1 = choice_function([1,2,3,4,5,6,7,8,9])
test2 = choice_function([1,2,3,4,5,6,7,8,9])

print(test1)
print(test2)


# In[37]:


'''C-1.13 Write a pseudo-code description of a function that reverses a list of n
integers, so that the numbers are listed in the opposite order than they
were before, and compare this method to an equivalent Python function
for doing the same thing.'''

def reverse_list(data):
    return data[::-1]

data1 = [1,2,3,4,5,6,7,8,9]
data2 = [100,238,23,1,2]

test1 = reverse_list(data1)
test2 = reverse_list(data2)
data1.reverse()
data2.reverse()

print(test1)
print(test2)
print(data1)
print(data2)


# In[39]:


'''C-1.14 Write a short Python function that takes a sequence of integer values and
determines if there is a distinct pair of numbers in the sequence whose
product is odd.'''

def find_pair(data):
    count_odd = 0
    for num in data:
        if num % 2 == 1:
            count_odd += 1
        if count_odd == 2:
            return True
    return False

test1 = find_pair([1,2,3,4,5,8,10])
test2 = find_pair([1,2,4,6,8,10])

print(test1)
print(test2)


# In[40]:


'''C-1.15 Write a Python function that takes a sequence of numbers and determines
if all the numbers are different from each other (that is, they are distinct).'''

def is_different(data):
    return len(data) == len(set(data))

test1 = is_different([1,2,3,4,5,6])
test2 = is_different([1,2,3,4,1,5,6,2])

print(test1)
print(test2)


# In[41]:


'''C-1.16 In our implementation of the scale function (page 25), the body of the loop
executes the command data[j] = factor. We have discussed that numeric
types are immutable, and that use of the = operator in this context causes
the creation of a new instance (not the mutation of an existing instance).
How is it still possible, then, that our implementation of scale changes the
actual parameter sent by the caller?'''

'''C-1.17 Had we implemented the scale function (page 25) as follows, does it work
properly?
def scale(data, factor):
    for val in data:
        val *= factor
Explain why or why not.'''

def scale_1(data,factor):
    for i in range(len(data)):
        data[i] *= factor
    return data

def scale_2(data,factor):
    for i in range(len(data)):
        data[i] = data[i] * factor
    return data

def scale_3(data,factor):
    for val in data:
        val *= factor
    return data

def scale_4(data,factor):
    for val in data:
        val = val * factor
    return data

print(scale_1([1,2,3,4,5,6,7],3))
print(scale_2([1,2,3,4,5,6,7],3))
print(scale_3([1,2,3,4,5,6,7],3))
print(scale_4([1,2,3,4,5,6,7],3))


# In[42]:


'''C-1.18 Demonstrate how to use Python’s list comprehension syntax to produce
the list [0, 2, 6, 12, 20, 30, 42, 56, 72, 90].'''

[i*(i+1) for i in range(10)]


# In[46]:


'''C-1.19 Demonstrate how to use Python’s list comprehension syntax to produce
the list [ a , b , c , ..., z ], but without having to type all 26 such
characters literally.'''

[chr(i) for i in range(ord('a'),ord('a')+26)]


# In[53]:


'''C-1.20 Python’s random module includes a function shuffle(data) that accepts a
list of elements and randomly reorders the elements so that each possible
order occurs with equal probability. The random module includes a
more basic function randint(a, b) that returns a uniformly random integer
from a to b (including both endpoints). Using only the randint function,
implement your own version of the shuffle function.'''

from random import randint

def shuffle_function(data):
    new_data = []
    while len(data) > 0:
        j = randint(0,len(data)-1)
        new_data.append(data.pop(j))
    return new_data

test1 = shuffle_function([1,2,3,4,5,6,7,8,9,10])

print(test1)


# In[57]:


'''C-1.22 Write a short Python program that takes two arrays a and b of length n
storing int values, and returns the dot product of a and b. That is, it returns
an array c of length n such that c[i] = a[i] · b[i], for i = 0, . . . ,n−1.'''

def dot(data1,data2):
    if len(data1) != len(data2) or len(data1) * len(data2) == 0:
        return 'wrong input'
    else:
        dot_list = []
        for i in range(len(data1)):
            dot_list.append(data1[i] * data2[i])
        return dot_list
    
        
test1 = dot([1,2,3,4,5],[5,4,3,2,1])
test2 = dot([1,2,3],[1,2,3,4,5])

print(test1)
print(test2)


# In[72]:


'''C-1.24 Write a short Python function that counts the number of vowels in a given
character string.'''

def count_vowels(s):
    count = 0
    for c in s:
        if c in ['a','e','i','o','u']:
            count += 1
    return count

test1 = count_vowels('asjflkjwefndsa')
test2 = count_vowels('weiursnflsaf')

print(test1)
print(test2)


# In[76]:


'''C-1.25 Write a short Python function that takes a string s, representing a sentence,
and returns a copy of the string with all punctuation removed. For example,
if given the string "Let's try, Mike.", this function would return
"Lets try Mike".'''

import string

def del_punctuation(s):
    return ''.join(c for c in s if c not in string.punctuation)

test1 = del_punctuation("Let's try, Mike.")
print(test1)

