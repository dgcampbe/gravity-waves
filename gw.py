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

def get_init():
    #Read initial conditions from inits.json
    init = open("inits.json","r")
    return eval(init.read())

def inertia_tensor(mass):
    #Calulates the inertia tensor
    inertia = np.array([[mass.position[1]**2 + mass.position[2]**2, -mass.position[0]*mass.position[1], -mass.position[0]*mass.position[2]],
                        [-mass.position[0]*mass.position[1], mass.position[0]**2 + mass.position[2]**2, -mass.position[1]*mass.position[2]],
                        [-mass.position[0]*mass.position[2], -mass.position[0]*mass.position[1], mass.position[0]**2 + mass.position[1]**2]])
    return inertia
    
def quadrupole_tensor(mass):
    #Calulates the quadrupole tensor
    quadrupole = np.array([[-(mass.position[1]**2 + mass.position[2]**2) + np.trace(inertia_tensor(mass))/3, mass.position[0]*mass.position[1], mass.position[0]*mass.position[2]],
                           [mass.position[0]*mass.position[1], -(mass.position[0]**2 + mass.position[2]**2) + np.trace(inertia_tensor(mass))/3, mass.position[1]*mass.position[2]],
                           [mass.position[0]*mass.position[2], mass.position[0]*mass.position[1], -(mass.position[0]**2 + mass.position[1]**2) + np.trace(inertia_tensor(mass))/3]])
    return quadrupole

def gravity_wave_power(mass):
    #Calulates the gravity wave power
    pass
    
def main():
    #Main
    init = get_init()
    time_init, m1_init, m2_init = init["time_init"], init["m1_init"], init["m2_init"]
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