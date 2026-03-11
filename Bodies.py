from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Body:
    name:str
    mass:float #m
    body_radius:float#r

    position: Optional[tuple[float,float,float]] = field(default=None) #(x, y, z)
    velocity: Optional[tuple[float,float,float]] = field(default=None) #(vx, vy,vz)

    semi_major_axis: Optional[float] = field(default=None) #a
    eccentricity: Optional[float] = field(default=None) #e
    orbital_tilt: Optional[float] = field(default=None) #inc
    longitude_ascending_node: Optional[float] = field(default=None) #Omega
    perihelion: Optional[float] = field(default=None)#omega
    true_anomaly: Optional[float] = field(default=None) #f
    primary: Optional[str] = field(default=None)#primary

