#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 12:01:07 2020

@author: Dane Campbell
"""
import pandas as pd
import matplotlib.pyplot as plt

class mass(object):
    """Mass"""
    def __init__(self, mass, position, momentum):

        self.mass = mass
        self.position = position
        self.momentum = momentum

    def update(self, timestep):
        #Dane's super secret patent pending aproximation technique
        import random
        self.momentum = tuple([x+random.uniform(-1, 1) for x in self.momentum]) 
        self.position = tuple([y+ (x/self.mass*timestep) for (x,y) in zip(self.momentum, self.position)])

#Gather input from user
print("For the below prompts, entering no value will enter default values.")
time_init = eval("(" + input("Please enter inital conditions for time (timestep, totalsteps).") + ")")
m1_init = eval("(" + input("Please enter intial conditions for mass1 (mass, position, momentum).") + ")")
m2_init = eval("(" + input("Please enter intial conditions for mass2 (mass, position, momentum).") + ")")

#default inits if no value provided
if time_init == ():

    time_init = (0.01,10000)

if m1_init == ():

    m1_init = (1,(1,1,1),(1,0,0))

if m2_init == ():

    m2_init = (10,(0,0,0),(0,0,0))

#create pandas dataframes
df1 = pd.DataFrame({"mass":[m1_init[0]],"position":[m1_init[1]],"momentum":[m1_init[2]]})
df2 = pd.DataFrame({"mass":[m2_init[0]],"position":[m2_init[1]],"momentum":[m2_init[2]]})
m1 = mass(*m1_init)
m2 = mass(*m2_init)

#loop over each time step
for i in range(time_init[1]):
    #update
    m1.update(time_init[0])
    m2.update(time_init[0])
    #append new time step data to dataframes
    df1 = df1.append(pd.DataFrame({"mass":[m1.mass], "position":[m1.position], "momentum":[m1.momentum]}), ignore_index=True)
    df2 = df2.append(pd.DataFrame({"mass":[m2.mass], "position":[m2.position], "momentum":[m2.momentum]}), ignore_index=True)
#debugging
print(df1)
print(df2)
df1.to_csv("df1.csv",index=False)
df2.to_csv("df2.csv",index=False)