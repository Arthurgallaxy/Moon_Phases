#This file was created on the 05/02/26.
import math

class Orbits:
    """Class representing the orbit of a body."""
    def __init__(self, satellite:str, center:str, major_axis:float, minor_axis:float, o_tilt:float):
        self.satellite = satellite #name of satellite, str
        self.center = center #name of center, str
        self.major_axis = major_axis #major axis of the orbit
        self.minor_axis = minor_axis #minor axis of the orbit
        self.o_tilt = o_tilt #tilt, to be given in degrees
        self._all_orbits[self] = {"satellite" : self.satellite, "center" : self.center}#adds the combination of bodies to a dictionary

    @staticmethod
    def orbit_check(body1, body2):
        """loops through the different orbits, to see which orbit belongs to these planet (if there is one) and returns the radius"""
        for key in Orbits._all_orbits:
            if Orbits._all_orbits[key]["satellite"] == body1 and Orbits._all_orbits[key]["center"] == body2:
                print(f"{body1} is the satellite and {body2} is the center")
                return key.o_radius
            elif Orbits._all_orbits[key]["satellite"] == body2 and Orbits._all_orbits[key]["center"] == body1:
                print(f"{body2} is the satellite and {body1} is the center")
                return key.o_radius#returns the radius
        print("there is no body/orbit combination available for these bodies") #value error or different type of error?

        #loop over all instances of a class


#Create class bodies
class Bodies:
    """Class representing the different celestial bodies (sun, planet, moon)"""
    G = 6.674e-11 #Newtons gravitational constant
    def __init__(self, name, type, p_radius, mass, x, y, z, vx, vy, vz, p_tilt):
        self.type = type.upper()#type can be sun, planet or moon
        self.name = name
        self.p_radius = p_radius #radius of the planet
        self.mass = mass
        self.position = (x, y, z)#tuple containing position information
        self.velocity = (vx, vy, vz) #tuple containing velocity information
        self.p_tilt = p_tilt

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        if type != "SUN" or "PLANET" or "MOON":
            ValueError("The body must be a sun, planet, or moon")
        self._type = type

    #setting and checking p_radius
    @property
    def p_radius(self):
        return self._p_radius

    @p_radius.setter
    def p_radius(self, radius):
        """sets the radius of the body and check if it is a valid radius"""
        if radius <= 0:
            raise ValueError("radius must be positive")
        else:
            self._p_radius = radius

    #setting and checking mass
    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, mass):
        """sets the mass of the body and check if it is a valid mass (larger than 0)"""
        if mass <= 0:
            raise ValueError("mass must be positive")
        else:
            self._mass = mass


#question: is this one nesesarry? we do not do a check for it...
    #setting and checking position
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        x, y, z = position
        self._position = (x, y, z)

    #setting and checking the velocity
    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        vx, vy, vz = velocity
        if self.type == "SUN" :
            if vx != 0 or vy != 0 or vz != 0:
                raise ValueError("The velocity of the sun must be 0")
            self._velocity = (0, 0, 0)
        elif vx == 0 and vy == 0 and vz == 0:
            raise ValueError("The velocity must be positive")
        self._velocity = (vx, vy, vz)

    #compiling the data to be read for the simulation:
    def data_maker(self):
        return [self.mass, self.position, self.velocity]

    #calculate the gravitational force between 2 bodies
#    @staticmethod
#    def Gravity(Body1, Body2):
#        distance = Orbits.orbit_check(Body1.name, Body2.name)
#        Fg = Bodies.G * Body1.mass * Body2.mass / (distance ** 2) #Fg = G*m_1*m_2/(r^2)
#        return Fg
