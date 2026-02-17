import numpy as np
import rebound

DEG = np.pi / 180.0
def simulate():
    timestep_num = 10000
    solar = rebound.Simulation()
    solar.integrator = "whfast"
    solar.G = 6.67443e-11
    solar.dt = 3600 #1 hour
    solar.ri_whfast.corrector = 17
    solar.ri_whfast.safe_mode = 0

    # Sun
    solar.add(m=1.9891e30,
              x=0.0, y=0.0, z=0.0,
              vx=0.0, vy=0.0, vz=0.0,
              r=6.957e8)

    sun = solar.particles[0]

    # Earth (heliocentric ecliptic J2000, derived from mean elements -> elliptical)
    solar.add(
        m=5.9722e24,
        a=1.495978707e11,  # 1 AU (m)
        e=0.0167086,
        inc=0.0 * DEG,
        Omega=0.0 * DEG,  # longitude of ascending node
        omega=102.9372 * DEG,  # argument of perihelion (rough)
        f=0.0 * DEG,  # true anomaly; 0 = perihelion
        primary=sun,
        r=6.378e6
    )
    earth = solar.particles[1]
    # Moon (Earth-centered at perigee, then shifted to heliocentric by adding Earth's state)
    solar.add(m=7.34767309e22,
        a=3.844e8,             # semi-major axis (m)
        e=0.0549,
        inc=5.145 * DEG,
        Omega=125.08 * DEG,    # rough; sets node direction
        omega=318.15 * DEG,    # rough; sets perigee direction
        f=0.0 * DEG,           # perigee
        primary=earth,
        r=1.737e6)
    moon = solar.particles[2]
    ##CONFIGURATIONS FOR THE SOLAR SYSTEM WERE CALCULATED AND SEARCHED FOR BY chatGPT


    pos = np.zeros((3, timestep_num, 3), dtype=np.float64)
    vel = np.zeros((3, timestep_num, 3), dtype=np.float64)

    # store initial pos/vel
    for b in range(3):
        pos[b, 0] = (solar.particles[b].x, solar.particles[b].y, solar.particles[b].z)
        vel[b, 0] = (solar.particles[b].vx, solar.particles[b].vy, solar.particles[b].vz)

    # main loop
    for t in range(1, timestep_num):  # Start from 1 since t=0 is already stored
        solar.integrate(t * solar.dt)
        for b in range(3):
            pos[b, t] = (
                solar.particles[b].x,
                solar.particles[b].y,
                solar.particles[b].z
            )
            vel[b, t] = (
                solar.particles[b].vx,
                solar.particles[b].vy,
                solar.particles[b].vz
            )

    for i in range(3):
        path = "Sim_data/" f"body{i}.csv"
        np.savetxt(path, pos[i], delimiter=",")

simulate()