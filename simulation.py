import os
import numpy as np
import rebound
import Bodies


class Simulator:
    #timestep_num and dt will have to be user inputs as well so the user can control both the accuracy and the duration of the simulation
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
        if isinstance(body, Bodies.Star):
#        if body.position is not None or body.velocity is not None:
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
        elif isinstance(body, Bodies.PlanetsAndMoons):
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
