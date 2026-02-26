#This file was created on the 05/02/26.
import math
class Orbits:
    """Class representing the orbit of a body."""
    _all_orbits = {}
    def __init__(self, satellite, o_radius, center, o_tilt):
        self.satellite = satellite #name of satellite, str
        self.o_radius = o_radius #radius of the orbit
        self.center = center #name of center, str
        self.o_tilt = o_tilt #tilt, to be given in degrees
        self._all_orbits[self] = {"satellite" : self.satellite, "center" : self.center}#adds the combination of bodies to a dictionary

    @staticmethod
    def orbit_check(body1, body2):
        """loops through the different orbits, to see which orbit belongs to these planet (if there is one)"""
        for key in Orbits._all_orbits:
            if Orbits._all_orbits[key]["satellite"] == body1 and Orbits._all_orbits[key]["center"] == body2:
                print(f"{body1} is the satellite and {body2} is the center")
                return key.O_radius
            elif Orbits._all_orbits[key]["satellite"] == body2 and Orbits._all_orbits[key]["center"] == body1:
                print(f"{body2} is the satellite and {body1} is the center")
                return key.O_radius
            else:
                print("Nothing yet...")
        print("there is no body/orbit combination available for these bodies") #value error or different type of error?

        #loop over all instances of a class


#testing:
#sun_orbit = Orbits("Sun", 0, "Sun", 0)
#earth_orbit = Orbits("Earth", 1.496e11, "Sun", 0)
#moon_orbit = Orbits("Moon", 3.844e5, "Earth", 5)
#bloop_orbit = Orbits("Bloop", 3.844e5, "Earth", 5)#testing
#Orbits.orbit_check("Moon", "Bloop") #testing


#Create class bodies
class Bodies:
    """Class representing the different celestial bodies (sun, planet, moon)"""
    G = 6.674e-11 #Newtons gravitational constant
    def __init__(self, name, p_radius, mass, x, y, z, vx, vy, vz, p_tilt):
        self.name = name
        self.p_radius = p_radius #radius of the planet
        self.mass = mass
        self.position = (x, y, z)#tuple containing position information
        self.velocity = (vx, vy, vz) #tuple containing velocity information
        self.p_tilt = p_tilt

    #calculate density of the planet
    def density(self):
        density = self.mass / (4 / 3 * math.pi * (self.P_radius ** 3))
        return density

    #calculate the gravitational force between 2 bodies
    @staticmethod
    def Gravity(Body1, Body2):
        distance = Orbits.orbit_check(Body1.name, Body2.name)
        Fg = Bodies.G * Body1.mass * Body2.mass / (distance ** 2) #Fg = G*m_1*m_2/(r^2)
        return Fg


#testing:
Earth = Bodies("Earth", 6378000, 5.9722e24, 1, 2, 3, 4, 5,6,0)
#print(Earth.density())
#Moon = Bodies("Moon", 1738000, 7.35e22)
#print(Bodies.Gravity(Earth, Moon))
