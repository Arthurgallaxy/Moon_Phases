from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Body:
    """Body class, containing all the information a body might have""" #comment behind each attribute is the name for it in rebound
    name:str
    mass:float #m
    body_radius:float #r

    #perimeters for the sun
    position: Optional[tuple[float,float,float]] = field(default=None) #(x, y, z)
    velocity: Optional[tuple[float,float,float]] = field(default=None) #(vx, vy,vz)

    #perimeters for the other bodies
    semi_major_axis: Optional[float] = field(default=None) #a
    eccentricity: Optional[float] = field(default=None) #e
    orbital_tilt: Optional[float] = field(default=None) #inc
    longitude_ascending_node: Optional[float] = field(default=None) #Omega
    perihelion: Optional[float] = field(default=None) #omega
    true_anomaly: Optional[float] = field(default=None) #f
    primary: Optional[str] = field(default=None) #primary

    #making sure certain inputs can be checked
    def __setattr__(self, name, value):
        """This magic method makes sure certain inputs can be checked for validity, after which it sets them like normal

            In this case, the inputs for the attributes "mass," "body_radius," and "semi_major_axis."

            For the setting of these attributes, the _check_larger_than_zero method is called"""
        if name == 'mass' or name == 'body_radius' or name == 'semi_major_axis' and value is not None:
            #must include is not None, otherwise None is compared to <= 0 in the _check_larger_than_zero
            #function when the property is not set (as default = None), which gives a SyntaxError
            self._check_larger_than_zero(value)
        super().__setattr__(name, value) #sets the attribute name with corresponding value, as normal

    #checks if input is >0, and raises a value error if this is not the case
    @staticmethod
    def _check_larger_than_zero(value):
        """ This static method checks if a value is larger than zero.

            It returns a ValueError if it is not the case."""
        if not value > 0:
            raise ValueError("The mass of the body must be greater than 0.")

