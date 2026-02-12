import numpy as np
import rebound

def simulate():
    timestep_num = 10000
    solar = rebound.Simulation()
    solar.integrator = "whfast"
    solar.G = 6.67443e-11
    solar.dt = 10000
    solar.ri_whfast.corrector = 17
    solar.ri_whfast.safe_mode = 0

    # Sun
    solar.add(m=1.9891e30,
              x=0.0, y=0.0, z=0.0,
              vx=0.0, vy=0.0, vz=0.0,
              r=6.957e8)

    # Earth (heliocentric ecliptic J2000, derived from mean elements -> elliptical)
    solar.add(m=5.9722e24,
              x=-2.65030215e10, y=1.44693286e11, z=1.19321608e5,
              vx=-2.97919995e4, vy=-5.47958267e3, vz=-9.76655903e-3,
              r=6.378e6)

    # Moon (Earth-centered at perigee, then shifted to heliocentric by adding Earth's state)
    solar.add(m=7.34767309e22,
              x=-2.61397251e10, y=1.44693286e11, z=1.19321608e5,
              vx=-2.97919995e4, vy=-4.39714069e3, vz=-9.76655903e-3,
              r=1.737e6)
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