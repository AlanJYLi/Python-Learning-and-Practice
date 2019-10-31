# Diet Problem
# Data set please refer to 'resources' file

import numpy as np
import pandas as pd
import math
from pulp import *

'''
1. Formulate an optimization model (a linear program) to find the cheapest diet that satisfies the maximum and minimum daily nutrition constraints, 
and solve it using PuLP.
Data set 'diet.xls' is in the 'resources' file.
'''

d = pd.read_excel(r'C:\Users\alanl\Desktop\Gatech MSiA\Courses\ISyE 6501 Introduction to Analytics Modeling\hw11\data 15.2\diet.xls')
d_c = d.iloc[65:67, :].dropna(axis=1) # Dataframe of constraint values
d_n = d.iloc[:64, :]

# create variables
def food(data):
    food_volume = {}
    nrow = data.shape[0]
    for i in range(nrow):
        foodname = data.iloc[i,]['Foods']
        food_volume[foodname] = LpVariable(foodname, 0, None, LpContinuous)
    return food_volume

# add constraints
def nutrition_constraints(problem, nutritionlist, food_volume, data, data_constraint):
    for nutrition in nutritionlist:
        minimum = data_constraint[nutrition].iloc[0]
        maximum = data_constraint[nutrition].iloc[1]
        total = 0
        for foodname in food_volume:
            n = data.loc[data['Foods']==foodname, nutrition].to_list()[0]
            total += n * food_volume[foodname]
        problem += total <= maximum
        problem += total >= minimum
    return problem

prob = LpProblem('p1', LpMinimize)
food_volume = food(d_n)
nutritionlist = d_n.columns.to_list()[3:]
cost = 0
for foodname in food_volume:
    cost += food_volume[foodname] * d_n.loc[d_n['Foods']==foodname, 'Price/ Serving'].to_list()[0]
prob += cost
prob = nutrition_constraints(prob, nutritionlist, food_volume, d_n, d_c)
status = prob.solve()

# print optimal solution
for foodname in food_volume:
    need = value(food_volume[foodname])
    if need > 0:
        print('{} = {:.3f}'.format(foodname,need))
print('\nObj = {:.3f}'.format(value(prob.objective)))


'''
2. Please add to your model the following constraints (which might require adding more variables) and solve the new model:   
a.If a food is selected, then a minimum of 1/10 serving must be chosen.  
b.Many people dislike celery and frozen broccoli. So at most one, but not both, can be selected.  
c.To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be selected.  
'''

# create variables to indicate whether a food is chosen or not (binary)
def select(data):
    food_select = {}
    nrow = data.shape[0]
    for i in range(nrow):
        foodname = data.iloc[i,]['Foods']
        food_select[foodname] = LpVariable(foodname+'_s', 0, 1, LpBinary)
    return food_select

'''
For new constraints a: If a food is selected, then a minimum of 1/10 serving must be chosen. 
The best way to connect the binary variable of a food being chosen or not and the continuous varible of the volume of a food here is 
two contraints combinations:  

1). volume = volume * chosen    
2). volume >= 1/10 * chosen  
  
These two constraints mean that if chosen = 0, then volume should be 0, and if chosen = 1, then volume should be at least 1/10 serving.  
 But the problem here is that the first constraint is quadratic. 
 One way to solve it is that we can change the first constraint into volume <= C * chosen, 
 in which C is an extremely large number so that volume will not equal to C in optimal solution (chosen=1). 
 But when chosen = 0, the this new constraint will become volume <= 0. Combining with volume >= 0, we can get volume = 0.
'''

# new constraints a
def minimum_volume(problem, food_volume, food_select):
    for foodname in food_volume:
        problem += food_volume[foodname] <= food_select[foodname] * 10000000
            # ensure if a food is not selected, the volume will be zero
        problem += food_volume[foodname] >= 1/10 * food_select[foodname]
            # ensure if a food is selected, the volume will be at least 1/10 units
    return problem

# new constraints b
def celery_broccoli(problem, food_select):
    problem += food_select['Frozen Broccoli']+food_select['Celery, Raw'] <= 1
    return problem

# new constraints c
def meat_kind(problem, food_select, meat_list):
    total = 0
    for meat in meat_list:
        total += food_select[meat]
    problem += total >= 3
    return problem


# Following is a list of foods that are classified as meat/poultry/fish/eggs. And we build the model.
meat_list = ['Roasted Chicken', 'Poached Eggs', 'Scrambled Eggs', 'Bologna,Turkey', 'Frankfurter, Beef', 
             'Ham,Sliced,Extralean', 'Kielbasa,Prk', 'Pizza W/Pepperoni', 'Taco', 'Hamburger W/Toppings', 
             'Hotdog, Plain', 'Pork', 'Sardines in Oil', 'White Tuna in Water', 'Chicknoodl Soup', 
             'Splt Pea&Hamsoup', 'Vegetbeef Soup', 'Neweng Clamchwd', 'New E Clamchwd,W/Mlk', 'Beanbacn Soup,W/Watr']


prob = LpProblem('p2', LpMinimize)
food_volume = food(d_n)
food_select = select(d_n)
nutritionlist = d_n.columns.to_list()[3:]
cost = 0
for foodname in food_volume:
    cost += food_volume[foodname] * d_n.loc[d_n['Foods']==foodname, 'Price/ Serving'].to_list()[0]
prob += cost
prob = nutrition_constraints(prob, nutritionlist, food_volume, d_n, d_c)
prob = minimum_volume(prob, food_volume, food_select)
prob = celery_broccoli(prob, food_select)
prob = meat_kind(prob, food_select, meat_list)
status = prob.solve()

# print optimal solution
for foodname in food_volume:
    choose = value(food_select[foodname])
    if choose > 0:
        print(foodname+' is selected:')
    need = value(food_volume[foodname])
    if need > 0:
        print('volume = {:.3f}\n'.format(need))
print('Obj = {:.3f}'.format(value(prob.objective)))


'''
3. If you want to see what a more full-sized problem would look like, 
try solving your models for the file diet_large.xls, which is a low-cholesterol diet model 
(rather than minimizing cost, the goal is to minimize cholesterol intake).
Data set 'diet_large.xls' is in the 'resources' file.
'''

dl = pd.read_excel(r'C:\Users\alanl\Desktop\Gatech MSiA\Courses\ISyE 6501 Introduction to Analytics Modeling\hw11\data 15.2\diet_large.xls')
dl_c = dl.iloc[[7147,7149], :].dropna(axis=1) # Dataframe of constraint values
dl_n = dl.iloc[:7146, :].drop(['Fatty acids, total trans', 'Fatty acids, total saturated'], axis=1)
dl_n.fillna(0, inplace=True)

def food_large(data):
    food_volume = {}
    nrow = data.shape[0]
    for i in range(nrow):
        foodname = data.iloc[i,]['Long_Desc']
        food_volume[foodname] = LpVariable(foodname, 0, None, LpContinuous)
    return food_volume

def nutrition_constraints_large(problem, nutritionlist, food_volume, data, data_constraint):
    for nutrition in nutritionlist:
        minimum = data_constraint[nutrition].iloc[0]
        maximum = data_constraint[nutrition].iloc[1]
        total = 0
        for foodname in food_volume:
            n = data.loc[data['Long_Desc']==foodname, nutrition].to_list()[0]
            total += n * food_volume[foodname]
        problem += total <= maximum
        problem += total >= minimum
    return problem

prob = LpProblem('p3', LpMinimize)
food_volume = food_large(dl_n)
nutritionlist = dl_n.columns.to_list()[1:-1]
cholesterol = 0
for foodname in food_volume:
    cholesterol += food_volume[foodname] * dl_n.loc[dl_n['Long_Desc']==foodname, 'Cholesterol'].to_list()[0]
prob += cholesterol
prob = nutrition_constraints_large(prob, nutritionlist, food_volume, dl_n, dl_c)
status = prob.solve()

for foodname in food_volume:
    need = value(food_volume[foodname])
    if need > 0:
        print('{} = {:.3f}'.format(foodname,need))
print('\nObj = {:.3f}'.format(value(prob.objective)))