import os
import numpy as np
import rebound

class Simulator:
    def __init__(self, timestep_num=10000, dt=3600):
        self.timestep_num = timestep_num
        self.dt = dt
        self.DEG = np.pi/180

    def _build_add_kwargs(self, body, particle_lookup):
        """
        Convert a Body object into kwargs for rebound.Simulation.add().
        Only include fields that are not None.
        """
        kwargs = {
            "m": body.mass,
            "r": body.body_radius
        }
        # Mode 1: Cartesian state vectors
        if body.position is not None or body.velocity is not None:
            if body.position is None or body.velocity is None:
                raise ValueError(
                    f"{body.name}: position and velocity must both be provided "
                    f"for Cartesian initialization."
                )

            if len(body.position) != 3 or len(body.velocity) != 3:
                raise ValueError(f"{body.name}: position/velocity must be 3-tuples.")

            kwargs["x"], kwargs["y"], kwargs["z"] = body.position
            kwargs["vx"], kwargs["vy"], kwargs["vz"] = body.velocity
            return kwargs

        # Mode 2: Orbital elements
        if body.semi_major_axis is not None:
            kwargs["a"] = body.semi_major_axis

            if body.eccentricity is not None:
                kwargs["e"] = body.eccentricity
            if body.orbital_tilt is not None:
                kwargs["inc"] = body.orbital_tilt * self.DEG
            if body.longitude_ascending_node is not None:
                kwargs["Omega"] = body.longitude_ascending_node * self.DEG
            if body.perihelion is not None:
                kwargs["omega"] = body.perihelion * self.DEG
            if body.true_anomaly is not None:
                kwargs["f"] = body.true_anomaly * self.DEG

            if body.primary is not None:
                if body.primary not in particle_lookup:
                    raise ValueError(
                        f"{body.name}: primary '{body.primary}' has not been created yet."
                    )
                kwargs["primary"] = particle_lookup[body.primary]

            return kwargs

        """"# Mode 3: Mass-radius only, defaults to origin if no position/orbit given
        kwargs["x"] = 0.0
        kwargs["y"] = 0.0
        kwargs["z"] = 0.0
        kwargs["vx"] = 0.0
        kwargs["vy"] = 0.0
        kwargs["vz"] = 0.0
        return kwargs
    currently not usefull, but could be for user freedom
    """

    def simulate(self, bodies, output_dir="Sim_data"):
        if not bodies:
            raise ValueError("bodies list is empty.")

        sim = rebound.Simulation()
        sim.integrator = "whfast"
        sim.G = 6.67443e-11
        sim.dt = self.dt
        sim.ri_whfast.corrector = 17
        sim.ri_whfast.safe_mode = 0

        os.makedirs(output_dir, exist_ok=True)

        # Maps body name -> rebound particle
        particle_lookup = {}
        ordered_names = []

        # Create all particles
        for body in bodies:
            kwargs = self._build_add_kwargs(body, particle_lookup)
            sim.add(**kwargs)

            particle_lookup[body.name] = sim.particles[-1]
            ordered_names.append(body.name)

        n_bodies = len(bodies)
        pos = np.zeros((n_bodies, self.timestep_num, 3), dtype=np.float64)
        vel = np.zeros((n_bodies, self.timestep_num, 3), dtype=np.float64)

        # Store initial state
        for i in range(n_bodies):
            p = sim.particles[i]
            pos[i, 0] = (p.x, p.y, p.z)
            vel[i, 0] = (p.vx, p.vy, p.vz)

        # Integrate
        for t in range(1, self.timestep_num):
            sim.integrate(t * sim.dt)
            for i in range(n_bodies):
                p = sim.particles[i]
                pos[i, t] = (p.x, p.y, p.z)
                vel[i, t] = (p.vx, p.vy, p.vz)

        # Save output
        for i, name in enumerate(ordered_names):
            pos_path = os.path.join(output_dir, f"{name}_pos.csv")
            vel_path = os.path.join(output_dir, f"{name}_vel.csv")
            np.savetxt(pos_path, pos[i], delimiter=",")
            np.savetxt(vel_path, vel[i], delimiter=",")

        return pos, vel
    """def simulate(self, bodies):
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
            inc=0.0 * self.DEG,
            Omega=0.0 * self.DEG,  # longitude of ascending node
            omega=102.9372 * self.DEG,  # argument of perihelion (rough)
            f=0.0 * self.DEG,  # true anomaly; 0 = perihelion
            primary=sun,
            r=6.378e6
        )
        earth = solar.particles[1]
        # Moon (Earth-centered at perigee, then shifted to heliocentric by adding Earth's state)
        solar.add(m=7.34767309e22,
            a=3.844e8,             # semi-major axis (m)
            e=0.0549,
            inc=5.145 * self.DEG,
            Omega=125.08 * self.DEG,    # rough; sets node direction
            omega=318.15 * self.DEG,    # rough; sets perigee direction
            f=0.0 * self.DEG,           # perigee
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
            """
