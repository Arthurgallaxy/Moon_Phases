from dataclasses import dataclass, field

@dataclass
class Body:
    name:str
    mass:float #m
    body_radius:float#r
    position:tuple = field(default=None) #(x, y, z)
    velocity:tuple = field(default=None) #(vx, vy,vz)
    semi_major_axis:float = field(default=None) #a
    eccentricity:float = field(default=None) #e
    orbital_tilt:float = field(default=None) #inc
    longitude_ascending_node:str = field(default=None) #Omega
    perihelion:str = field(default=None)#omega
    true_anomaly:str = field(default=None) #f
    primary:str = field(default=None)#primary

