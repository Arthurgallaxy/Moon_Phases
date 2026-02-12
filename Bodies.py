#This file was created on the 05/02/26.
import math
class Orbits:
    def __init__(self, satellite, O_radius, centre):
        self.satellite = satellite
        self.O_radius = O_radius
        self.centre = centre


class Bodies:
    G = 6.674e-11
    def __init__(self, name, P_radius, mass):
        self.name = name
        self.P_radius = P_radius
        self.mass = mass

    def density(self):
        density = self.mass / (4 / 3 * math.pi * (self.P_radius ** 3))
        return density

    @staticmethod
    def Gravity(Body1, Body2):
        Fg = Bodies.G * Body1.mass * Body2.mass *
        return Fg


Earth = Bodies("Earth", 6378000, 5.9722e24)
print(Earth.density())
Moon = Bodies("Moon", 1738000, 7.35e22)
print(Bodies.Gravity(Earth, Moon))