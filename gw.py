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
        self.df = pd.DataFrame({"mass":[self.mass],"position":[self.position],"momentum":[self.momentum]})

    def update(self, timestep):
        #Dane's super secret patent pending aproximation technique
        self.momentum = tuple([x*0.99 for x in self.momentum]) 
        self.position = tuple([y+ (x/self.mass*timestep) for (x,y) in zip(self.momentum, self.position)])
        self.update_df()
        
    def update_df(self):
        
        self.df = self.df.append(pd.DataFrame({"mass":[self.mass], "position":[self.position], "momentum":[self.momentum]}), ignore_index=True)

def prompt():
    
    #Gather input from user
    print("For the below prompts, entering no value will enter default values.")
    time_init = eval("(" + input("Please enter inital conditions for time (timestep, totalsteps).") + ")")
    m1_init = eval("(" + input("Please enter intial conditions for mass1 (mass, position, momentum).") + ")")
    m2_init = eval("(" + input("Please enter intial conditions for mass2 (mass, position, momentum).") + ")")
    return [time_init,m1_init,m2_init]

def empty_to_default(inits):
    #default inits if no value provided
    defaults = [(0.01,10000),(1,(1,1,1),(1,0,0)),(10,(0,0,0),(0,0,0))]
    for i in range(len(inits)):
        if inits[i] == ():
            inits[i]=defaults[i]
    return inits

def main():
    [time_init,m1_init,m2_init] = empty_to_default(prompt())
    #create masses
    m1 = mass(*m1_init)
    m2 = mass(*m2_init)
    print("Aproximating for each time step. This may take a few seconds.")
    for i in range(time_init[1]):
        #update
        m1.update(time_init[0])
        m2.update(time_init[0])
    #debugging
    m1.df.to_csv("m1.csv",index=False)
    m2.df.to_csv("m2.csv",index=False)

main()