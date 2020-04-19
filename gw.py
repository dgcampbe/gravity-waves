#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 12:01:07 2020

@author: Dane Campbell
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class mass(object):
    """Mass"""
    def __init__(self, init):
        #Initialize mass
        self.mass = init["mass"]
        self.position = init["position"]
        self.momentum = init["momentum"]
        self.df = pd.DataFrame({"mass":[self.mass],"position":[self.position],"momentum":[self.momentum],"time":[0]})

    def update(self, time_init):
        #Update position and momentum for a time step
        self.momentum = np.multiply(self.momentum,0.99) 
        self.position = np.add(self.position, np.multiply(self.momentum, time_init["time_step"]/self.mass))
        self.update_df()
        
    def update_df(self):
        #Add new row to df with current values
        self.df = self.df.append(pd.DataFrame({"mass":[self.mass], "position":[self.position], "momentum":[self.momentum]}), ignore_index=True)

def get_inits():
    #Read initial conditions from inits.txt
    inits = open("inits.txt","r")
    time_init = eval(inits.readline())
    m1_init = eval(inits.readline())
    m2_init = eval(inits.readline())
    return (time_init, m1_init, m2_init)
    
def main():
    #Main
    (time_init,m1_init,m2_init) = get_inits()
    #Create masses
    m1 = mass(m1_init)
    m2 = mass(m2_init)
    print("Aproximating for each time step. This may take a few seconds.")
    for i in range(time_init["total_steps"]):
        #Update
        m1.update(time_init)
        m2.update(time_init)
    #Debugging
    m1.df.to_csv("m1.csv",index=False)
    m2.df.to_csv("m2.csv",index=False)
    print("Data for masses has been exported to csv. Please check the files for results.")
#Run main
main()