#!/usr/bin/env python
"""Gravity Waves."""
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants


class Mass:
    """Mass."""

    def __init__(self, init):
        self.mass = init["mass"]
        self.position = init["position"]
        self.momentum = init["momentum"]
        # Initialize the dataframe
        self.df = pd.DataFrame({"mass": [self.mass],
                                "position": [self.position],
                                "momentum": [self.momentum],
                                "time": [0]})

    def update(self, time_init, mass):
        """Update position and momentum for a time step."""
        # Update the momentum for Newtonian gravity
        self.momentum = np.add(self.momentum, np.multiply(np.subtract(mass.position, self.position),
                                                          scipy.constants.G * self.mass * mass.mass / (np.linalg.norm(
                                                              np.subtract(self.position, mass.position)) ** 3)))
        # Update the position due to momentum
        self.position = np.add(self.position, np.multiply(self.momentum, time_init["time_step"] / self.mass))
        # Update the dataframe
        self.update_df()

    def update_df(self):
        """Add new row to the mass's dataframe with mass's current values."""
        self.df = self.df.append(pd.DataFrame({"mass": [self.mass],
                                               "position": [self.position],
                                               "momentum": [self.momentum]}),
                                 ignore_index=True)

    @property
    def inertia_tensor(self):
        """Calculate the inertia tensor."""
        # Inertia tensor is calculated using a "pre-baked" formula
        return self.mass * np.array([[self.position[1] ** 2 + self.position[2] ** 2,
                                    -self.position[0] * self.position[1],
                                    -self.position[0] * self.position[2]],
                                    [-self.position[0] * self.position[1],
                                    self.position[0] ** 2 + self.position[2] ** 2,
                                    -self.position[1] * self.position[2]],
                                    [-self.position[0] * self.position[2],
                                    -self.position[0] * self.position[1],
                                    self.position[0] ** 2 + self.position[1] ** 2]])

    @property
    def quadrupole_tensor(self):
        """Calculate the quadrupole tensor."""
        # Quadrupole tensor is calculated using a "pre-baked" formula using the trace of the inertia tensor
        return self.mass * np.array([[-(self.position[1] ** 2 + self.position[2] ** 2) + np.trace(
                                        self.inertia_tensor) / 3, self.position[0] * self.position[1], self.position[0] * self.position[2]],
                                    [self.position[0] * self.position[1],
                                        -(self.position[0] ** 2 + self.position[2] ** 2) + np.trace(
                                        self.inertia_tensor) / 3, self.position[1] * self.position[2]],
                                     [self.position[0] * self.position[2], self.position[0] * self.position[1],
                                      -(self.position[0] ** 2 + self.position[1] ** 2) + np.trace(
                                        self.inertia_tensor) / 3]])


def get_init():
    """Read initial conditions from inits.json."""
    init = open("inits.json", "r")
    return eval(init.read())


def gravity_wave_power(mass, time_init):
    """Calculate the gravity wave power."""
    # Definitely not ready yet
    return scipy.constants.G * (numerical_derivative(mass.quadrupole_tensor, 3, time_init["time_step"]) ** 2) / (
                5 * scipy.constants.c ** 5)


def numerical_derivative(f, n, time_step):
    """Numerically calculate the derivative."""
    # Definitely not ready yet
    return np.diff(f, n=n) / time_step


def main():
    """Main."""
    # Grab the initial conditions
    init = get_init()
    # Split the initial conditions
    time_init, m1_init, m2_init = init["time_init"], init["m1_init"], init["m2_init"]
    # Create the masses
    m1 = Mass(m1_init)
    m2 = Mass(m2_init)
    # Warn the user that the computation may take a while
    print("Approximating for each time step. This may take a while.")
    # Get the starting time
    start = time.time()
    for i in range(time_init["total_steps"]):
        # Give the user an idea of where the computation currently is
        if i % 1000 == 0:
            print(
                str(i) + " computations have been made. " + str(100.0 * i / time_init["total_steps"]) + "% completed.")
        # Update each mass
        m1.update(time_init, m2)
        m2.update(time_init, m1)
    # Get the ending time
    end = time.time()
    # Debugging
    # Export the dataframes to csv files
    m1.df.to_csv("m1.csv", index=False)
    m2.df.to_csv("m2.csv", index=False)
    # Tell the user that the computation is done and give computation statistics
    print("Finished computation of " + str(time_init["total_steps"]) + " time steps of " + str(
        time_init["time_step"]) + " seconds each.")
    print("Total runtime: " + str((end - start)) + " seconds.")
    print("Average time per time step: " + str((end - start) / time_init["total_steps"]) + " seconds.")
    print("Data for masses has been exported to csv. Please check the files for results.")
    # Plot the data
    plt.plot([x[0] for x in m1.df["position"]], [x[1] for x in m1.df["position"]])


# Run main
if __name__ == "__main__":
    main()
