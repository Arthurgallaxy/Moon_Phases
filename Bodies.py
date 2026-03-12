from dataclasses import dataclass, field
from typing import Optional

#parent class
@dataclass
class Bodies:#comment behind each attribute is the name for it in rebound
    """Body class, containing the information all bodies must have"""
    name:str
    mass:float #m
    body_radius:float #r

    #making sure certain inputs can be checked
    def __setattr__(self, name, value):
        """This magic method makes sure certain inputs can be checked for validity, after which it sets them like normal

            In this case, the inputs for the attributes mass and body_radius are checked.

            Before the setting of these attributes, the _check_larger_than_zero method is called"""
        if name == 'mass' or name == 'body_radius':
            self._check_larger_than_zero(value)
        super().__setattr__(name, value) #sets the attribute name with corresponding value, as normal

    #checks if input is >0, and raises a value error if this is not the case
    @staticmethod
    def _check_larger_than_zero(value):
        """ This static method checks if a value is larger than zero.

            It returns a ValueError if it is not the case."""
        if not value > 0:
            raise ValueError("The mass and radius of the body, and the semi_major_axis (if applicable) must be greater than 0.")



#child class 1, Stars
@dataclass
class Star(Bodies): #comment behind each attribute is the name for it in rebound
    """Child dataclass of bodies, containing the additional attributes only relevant for a star"""
    position: tuple[float,float,float] #(x, y, z)
    velocity: tuple[float,float,float] #(vx, vy,vz)



#child class 2, Planets and Moons
@dataclass(kw_only = True) #kw_only = True allows optional attributes and non-optional attributes to be in any order
class PlanetsAndMoons(Bodies): #comment behind each attribute is the name for it in rebound
    """Child dataclass of bodies, containing the additional attributes only relevant for the planets and moons"""
    semi_major_axis: float #a
    eccentricity: Optional[float] = field(default=0) #e
    orbital_tilt: Optional[float] = field(default=0) #inc
    longitude_ascending_node: Optional[float] = field(default=0) #Omega
    perihelion: Optional[float] = field(default=0) #omega
    true_anomaly: Optional[float] = field(default=0) #f
    primary: str # primary


    def __setattr__(self, name, value):
        """This magic method makes sure certain inputs can be checked for validity, after which it sets them like normal

            In this case, the input for the "semi_major_axis."

            For the setting of this attribute, the _check_larger_than_zero method is called"""
        if name == "semi_major_axis":
            self._check_larger_than_zero(value)
        super().__setattr__(name, value) #sets the attribute name with corresponding value, as normal

