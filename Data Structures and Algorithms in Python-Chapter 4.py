#!/usr/bin/env python
# coding: utf-8

# In[3]:


'''R-4.1 Describe a recursive algorithm for finding the maximum element in a sequence,
S, of n elements. What is your running time and space usage?'''

def find_max_1(s):
    if len(s) == 1:
        max_element = s[0]
    else:
        n = len(s)
        new_one = s[n-1]
        s = s[:n-1]
        if find_max_1(s) >= new_one:
            max_element = find_max_1(s)
        else:
            max_element = new_one
    return max_element

s1 = [1,2,3,4,5,6,7]
s2 = [7,6,5,4,3,2,1]
s3 = [1]
s4 = [1,3,2,4,5,6,10,2,1,3]

print(find_max_1(s1))
print(find_max_1(s2))
print(find_max_1(s3))
print(find_max_1(s4))


def find_max_2(s,n):
    if n == 1:
        return s[n-1]
    else:
        max_element = find_max_2(s,n-1)
        return max_element if max_element >= s[n-1] else s[n-1]

print(find_max_2(s1,len(s1)))
print(find_max_2(s2,len(s2)))
print(find_max_2(s3,len(s3)))
print(find_max_2(s4,len(s4)))


# In[5]:


'''R-4.2 Draw the recursion trace for the computation of power(2,5), using the
traditional function implemented in Code Fragment 4.11.'''

def power_1(m,n):
    if n == 1:
        return m
    else:
        return m * power_1(m,n-1)

print(power_1(2,5))
print(power_1(2,13))


'''R-4.3 Draw the recursion trace for the computation of power(2,18), using the
repeated squaring algorithm, as implemented in Code Fragment 4.12.'''

def power_2(m,n):
    if n == 1:
        return m
    else:
        part = power_2(m,n//2) ** 2
        if n % 2 == 1:
            part = part * m
        return part

print(power_2(2,5))
print(power_2(2,13))


# In[11]:


'''R-4.4 Draw the recursion trace for the execution of function reverse(S, 0, 5)
(Code Fragment 4.10) on S = [4, 3, 6, 2, 6].'''

def reverse_list(s,start,end):
    if start >= end:
        return s
    else:
        s[start],s[end] = s[end],s[start]
        return reverse_list(s,start+1,end-1)

print(reverse_list([4,3,6,2,6],0,4))
print(reverse_list([1,2,3,4,5,6,7,8,9,10],0,9))


# In[13]:


'''R-4.6 Describe a recursive function for computing the nth Harmonic number, Hn=1/1+1/2+1/3+...+1/n'''

def harmonic_num(n):
    if n == 1:
        return 1
    else:
        return harmonic_num(n-1)+1/n

print(harmonic_num(4))


# In[15]:


'''R-4.7 Describe a recursive function for converting a string of digits into the integer
it represents. For example, 13531 represents the integer 13,531.'''

def convert_string_to_int(s):
    if len(s) == 1:
        return int(s)
    else:
        last_dig = int(s[-1])
        s = s[:-1]
        return convert_string_to_int(s) * 10 + last_dig

print(convert_string_to_int('13531'))
print(convert_string_to_int('1342231231'))


# In[21]:


'''C-4.9 Write a short recursive Python function that finds the minimum and maximum
values in a sequence without using any loops.'''

def find_max_min(s,n):
    if n == 1:
        return s[n-1],s[n-1]
    else:
        max_num = find_max_min(s,n-1)[0]
        min_num = find_max_min(s,n-1)[1]
        if s[n-1] >= max_num:
            return s[n-1],min_num
        elif s[n-1] <= min_num:
            return max_num,s[n-1]
        else:
            return max_num,min_num

s1 = [1,2,3,4,5,6,7]
s2 = [7,6,5,4,3,2,1]
s3 = [1]
s4 = [1,3,2,4,5,6,10,2,1,3]

print(find_max_min(s1,len(s1)))
print(find_max_min(s2,len(s2)))
print(find_max_min(s3,len(s3)))
print(find_max_min(s4,len(s4)))


# In[16]:


'''C-4.10 Describe a recursive algorithm to compute the integer part of the base-two
logarithm of n using only addition and integer division.'''

# find t thus 2**t<=n and 2**(t+1)>n

def int_part_log(n):
    if n <= 0:
        return 'n must be positive.'
    if 0 < n < 2:
        return 0
    else:
        return int_part_log(n//2) + 1

print(int_part_log(10))


# In[18]:


'''C-4.11 Describe an efficient recursive function for solving the element uniqueness
problem, which runs in time that is at most O(n2) in the worst case
without using sorting.'''

def is_unique(s,n):
    if n == 1:
        return True
    else:
        if is_unique(s,n-1) and s[n-1] not in s[:n-1]:
            return True
        else:
            return False

print(is_unique([1,3,4,5,2,6],6))
print(is_unique([1],1))
print(is_unique([1,2,3,4,5,6,2],7))


# In[22]:


'''C-4.12 Give a recursive algorithm to compute the product of two positive integers,
m and n, using only addition and subtraction.'''

def product(m,n):
    if m < n:
        m,n = n,m
    if n == 1:
        return m
    else:
        return product(m,n-1)+m
    
print(product(10,3))
print(product(10,1))
print(product(1,12))
print(product(11,12))


# In[29]:


'''C-4.14 In the Towers of Hanoi puzzle, we are given a platform with three pegs, a,
b, and c, sticking out of it. On peg a is a stack of n disks, each larger than
the next, so that the smallest is on the top and the largest is on the bottom.
The puzzle is to move all the disks from peg a to peg c, moving one disk
at a time, so that we never place a larger disk on top of a smaller one.
See Figure 4.15 for an example of the case n = 4. Describe a recursive
algorithm for solving the Towers of Hanoi puzzle for arbitrary n. (Hint:
Consider first the subproblem of moving all but the nth disk from peg a to
another peg using the third as “temporary storage.”)'''

# In fact, moving times of hanoi(n) = moving times of hanoi(n-1) * 2 + 1 (n-1 to b, then last one to c, then n-1 to c)

def hanoi(n,a,b,c):
    count = 0
    if n == 1:
        print(a,'-->',c)
        return 1
    else:
        count = count + hanoi(n-1,a,c,b)
        count = count + hanoi(1,a,b,c)
        count = count + hanoi(n-1,b,a,c)
        return count

hanoi(4,'a','b','c')


# In[70]:


'''C-4.15 Write a recursive function that will output all the subsets of a set of n
elements (without repeating any subsets).'''

def get_subsets(s,n):
    if n == 1:
        return [[],[s[n-1]]]
    else:
        result = get_subsets(s,n-1) * 2
        for i in range(2**(n-1)):
            result[i] = result[i] + [s[n-1]]
        return result

print(get_subsets([1,2,3],3))


def get_subsets_2(data,seq=[]):
    if data == []:
        return [seq]
    else:
        return get_subsets_2(data[1:],seq)+get_subsets_2(data[1:],seq+[data[0]])

print(get_subsets_2([1,2,3],[]))


# In[80]:


'''C-4.16 Write a short recursive Python function that takes a character string s and
outputs its reverse. For example, the reverse of pots&pans would be
snap&stop'''

def reverse_str(s,left='',right=''):
    if len(s) <= 1:
        return left + s + right
    else:
        left_c = s[0]
        right_c = s[-1]
        return reverse_str(s[1:-1],left+right_c,left_c+right)
    
        
print(reverse_str('pots&pans','',''))
print(reverse_str('sadureiwfd','',''))


# In[81]:


'''C-4.17 Write a short recursive Python function that determines if a string s is a
palindrome, that is, it is equal to its reverse. For example, racecar and
gohangasalamiimalasagnahog are palindromes.'''

def is_palindrome(s):
    if len(s) <= 1:
        return True
    else:
        return s[0] == s[-1] and is_palindrome(s[1:-1])

print(is_palindrome('l'))
print(is_palindrome('lol'))
print(is_palindrome('liiiil'))
print(is_palindrome('abcdefedcba'))
print(is_palindrome('dkalfjei'))


# In[95]:


'''C-4.18 Use recursion to write a Python function for determining if a string s has
more vowels than consonants.'''

def compare_vowels_consonants(s):
    if len(s) == 1:
        return (1,0) if s[0] in ['a','e','i','o','u'] else (0,1)
    else:
        (vowels,consonants) = compare_vowels_consonants(s[:-1])
        return (vowels+1,consonants) if s[-1] in ['a','e','i','o','u'] else (vowels,consonants+1)


compare_vowels_consonants('alandakjfe')[0] > compare_vowels_consonants('alandakjfe')[1]


# In[107]:


'''C-4.19 Write a short recursive Python function that rearranges a sequence of integer
values so that all the even values appear before all the odd values.'''

def rearrange_even_odd(data,even=[],odd=[]):
    if data == []:
        return even + odd
    else:
        return rearrange_even_odd(data[1:],even+[data[0]],odd) if data[0] % 2 == 0 else rearrange_even_odd(data[1:],even,odd+[data[0]])

rearrange_even_odd([1,3,5,7],[],[])


# In[118]:


'''C-4.20 Given an unsorted sequence, S, of integers and an integer k, describe a
recursive algorithm for rearranging the elements in S so that all elements
less than or equal to k come before any elements larger than k. What is
the running time of your algorithm on a sequence of n values?'''

def rearrange_by_k(data,k,less=[],more=[]):
    if data == []:
        return less + more
    else:
        return rearrange_by_k(data[1:],k,less+[data[0]],more) if data[0] <= k else rearrange_by_k(data[1:],k,less,more+[data[0]])

rearrange_by_k([5,4,12,1,2,3,5,3,2],4,[],[])


# In[144]:


'''C-4.21 Suppose you are given an n-element sequence, S, containing distinct integers
that are listed in increasing order. Given a number k, describe a
recursive algorithm to find two integers in S that sum to k, if such a pair
exists. What is the running time of your algorithm?'''

def find_add_pair(s,k,start,end):
    if start == end-1:
        return False
    else:
        if s[start] + s[end-1] > k:
            return find_add_pair(s,k,start,end-1)
        elif s[start] + s[end-1] < k:
            return find_add_pair(s,k,start+1,end)
        elif s[start] + s[end-1] == k:
            return True
        

k=10
s1=[-1,2,3,4,5,7,9]
s2=[-3,-2,1,3,6,8,14]

print(find_add_pair(s1,10,0,len(s1)))
print(find_add_pair(s2,10,0,len(s2)))


# In[7]:


import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
 
x1 = np.linspace(-2000,4000,100)
yn = np.linspace(-2000,4000,100)
xn = np.array([200]*100)
 
y1 = 2000-x1
y2 = 0*x1+1500 # y=1500
y3 = 0*xn+yn  # x=200
 
# Make plot
plt.plot(x1, y1, label=r'$x+y=2000$')
plt.plot(x1, y2, label=r'$y=1500$')
plt.plot(xn, y3, label=r'$x=200$')

 
plt.xlim((-2000, 4000))
plt.ylim((-2000,4000))
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
 
# Fill feasible region
y4 = np.maximum(y1,y2)
plt.fill_between(x, y3, y4, where=y3>=y4, color='grey', alpha=0.5)
 
 
plt.grid(True, linestyle='-.')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
 
#plt.savefig('ordering_constraints.eps',dpi=600,bbox_inches='tight')
plt.show()


# In[16]:


import numpy as np
import matplotlib.pyplot as plt
import math
get_ipython().run_line_magic('matplotlib', 'inline')

import mpl_toolkits.axisartist as axisartist
fig = plt.figure(figsize=(8,8))
ax = axisartist.Subplot(fig,111)
fig.add_axes(ax)
ax.axis[:].set_visible(False)
ax.axis["x"] = ax.new_floating_axis(0,0)
ax.axis["x"].set_axisline_style("->", size = 1.0)
ax.axis["y"] = ax.new_floating_axis(1,0)
ax.axis["y"].set_axisline_style("-|>", size = 1.0)
ax.axis["x"].set_axis_direction("top")
ax.axis["y"].set_axis_direction("right")
 
x1 = [0.1*i for i in range(1,100)]
y1 = [num**0 for num in x1]
y2 = [num**(-1) for num in x1]
y3 = [num**(-2) for num in x1]


plt.plot(x1, y1, label=r'$y=x^a,a=0$')
plt.plot(x1, y2, label=r'$y=x^a,a=-1$')
plt.plot(x1, y3, label=r'$y=x^a,a=-2$')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[19]:


import numpy as np
import matplotlib.pyplot as plt
import math
get_ipython().run_line_magic('matplotlib', 'inline')
import mpl_toolkits.axisartist as axisartist
fig = plt.figure(figsize=(8,8))
ax = axisartist.Subplot(fig,111)
fig.add_axes(ax)
ax.axis[:].set_visible(False)
ax.axis["x"] = ax.new_floating_axis(0,0)
ax.axis["x"].set_axisline_style("->", size = 1.0)
ax.axis["y"] = ax.new_floating_axis(1,0)
ax.axis["y"].set_axisline_style("-|>", size = 1.0)
ax.axis["x"].set_axis_direction("top")
ax.axis["y"].set_axis_direction("right")
 
x1 = [0.1*i for i in range(1,100)]
y1 = [math.log(num)*num for num in x1]


plt.plot(x1, y1, label=r'$y=xlog(x)$')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[23]:


from mpl_toolkits import mplot3d
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np

def f(x, y):
    return (x**2)/y
x = np.linspace(-5,5,100)
y = np.linspace(1,11,100)
X, Y = np.meshgrid(x, y)
Z = f(X,Y)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
#ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.view_init(60, 35)

